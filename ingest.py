"""
PDF Ingestion Pipeline for HR Policy Assistant.

Loads hr_manual.pdf, extracts text page-by-page preserving accurate page numbers
and policy section headings in metadata, splits into overlapping chunks, generates
Google Gemini embeddings, and stores them persistently in ChromaDB.
"""

import sys
import time
import shutil
import re
from pathlib import Path
from typing import List

import pymupdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

import config


def extract_section_header(text: str, current_section: str) -> str:
    """
    Heuristically detect section headings from page text to attach to chunk metadata.
    Preserves existing section if no new heading is discovered.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:8]:
        if re.match(r"^(SECTION\s*[-–—]\s*[IVXLCDM]+)", line, re.IGNORECASE):
            return line
        if re.match(r"^(\[[A-Z]\]\s+[A-Za-z\s]+)", line):
            return line
        if re.match(r"^(Annexure\s*[-–—]?\s*[IVXLCDM]+)", line, re.IGNORECASE):
            return line
        if re.match(r"^\d+\.\d+\s+[A-Za-z\s]+", line):
            return line
        if "policy" in line.lower() and len(line) < 45 and not line.lower().startswith("this"):
            return line
    return current_section


def load_pdf_documents(pdf_path: Path) -> List[Document]:
    """
    Loads text from each page of the PDF file and returns a list of Document objects
    with accurate 1-indexed page numbers and section headers in the metadata.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found at: {pdf_path}\n"
            f"Please ensure 'hr_manual.pdf' is placed inside the 'data/' directory."
        )

    try:
        doc = pymupdf.open(str(pdf_path))
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF file '{pdf_path}': {e}")

    total_pages = len(doc)
    if total_pages == 0:
        raise ValueError(f"The PDF file '{pdf_path}' is empty (0 pages).")

    print(f"📖 Loading PDF '{pdf_path.name}' with {total_pages} pages...")

    documents = []
    current_section = "General HR Policy"

    for page_idx in range(total_pages):
        page = doc[page_idx]
        page_num = page_idx + 1  # 1-indexed page number matching PDF viewer
        text = page.get_text()

        if not text or not text.strip():
            print(f"⚠️  Warning: Page {page_num} contains no extractable text.")
            continue

        current_section = extract_section_header(text, current_section)

        # Create LangChain Document with rich metadata
        doc_obj = Document(
            page_content=text,
            metadata={
                "source": pdf_path.name,
                "page": page_num,
                "section": current_section,
                "total_pages": total_pages,
            },
        )
        documents.append(doc_obj)

    print(f"✅ Extracted text from {len(documents)} pages.")
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into overlapping chunks using RecursiveCharacterTextSplitter.
    Preserves page number and section metadata on every resulting chunk.
    """
    print(
        f"✂️  Splitting documents into chunks (size={config.CHUNK_SIZE}, "
        f"overlap={config.CHUNK_OVERLAP})..."
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", "• ", "-> ", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} document chunks.")
    return chunks


def build_vector_store(chunks: List[Document], rebuild: bool = False) -> Chroma:
    """
    Generates embeddings for document chunks using Google Gemini and stores
    them in persistent ChromaDB with automatic retry and rate-limit pacing.
    """
    if not config.validate_api_key():
        raise ValueError(
            "Gemini API key is missing or invalid.\n"
            "Please configure GEMINI_API_KEY in your '.env' file."
        )

    persist_dir = config.CHROMA_DIR

    if rebuild and persist_dir.exists():
        print(f"🧹 Rebuild flag set: Resetting ChromaDB directory at '{persist_dir}'...")
        for item in persist_dir.iterdir():
            if item.name != ".gitkeep":
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    persist_dir.mkdir(parents=True, exist_ok=True)

    print(f"🧠 Initializing Gemini Embeddings model: {config.EMBEDDING_MODEL}...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY,
    )

    print(f"💾 Ingesting {len(chunks)} chunks into ChromaDB at '{persist_dir}'...")
    
    # Batch ingestion with pacing and retries to gracefully handle Gemini free tier limits
    batch_size = 25
    vectorstore = Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(persist_dir),
    )

    total_batches = (len(chunks) + batch_size - 1) // batch_size
    for b_idx in range(total_batches):
        start = b_idx * batch_size
        batch = chunks[start : start + batch_size]
        print(f"   Processing batch {b_idx + 1}/{total_batches} ({len(batch)} chunks)...")

        max_retries = 5
        for attempt in range(1, max_retries + 1):
            try:
                vectorstore.add_documents(documents=batch)
                break
            except Exception as e:
                err_str = str(e)
                if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                    wait_time = 45 + (attempt * 10)
                    print(f"   ⏳ Rate limit reached (free tier quota). Waiting {wait_time}s before retry (attempt {attempt}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ Unexpected error in batch {b_idx + 1}: {e}")
                    raise e
        else:
            raise RuntimeError(f"Failed to ingest batch {b_idx + 1} after {max_retries} retries.")

        # Gentle pacing between batches
        time.sleep(2)

    print(f"🎉 ChromaDB ingestion complete and persisted to '{persist_dir}'!")
    return vectorstore


def run_ingestion(rebuild: bool = False):
    """Full ingestion workflow."""
    print("=" * 60)
    print("🚀 Starting HR Policy Manual Ingestion Pipeline")
    print("=" * 60)

    try:
        documents = load_pdf_documents(config.PDF_PATH)
        chunks = chunk_documents(documents)
        build_vector_store(chunks, rebuild=rebuild)
        print("=" * 60)
        print("✨ Document Ingestion Pipeline Finished Successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    rebuild_flag = "--rebuild" in sys.argv
    run_ingestion(rebuild=rebuild_flag)
