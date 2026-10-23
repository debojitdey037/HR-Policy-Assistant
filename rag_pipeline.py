"""
RAG Pipeline module for HR Policy Assistant.

Implements the modern LangChain Runnable pipeline:
Retriever -> PromptTemplate -> Gemini LLM -> StrOutputParser

Enforces strict grounding on the HR Policy Manual and emits exact 'Not found'
whenever sufficient evidence is absent or not verifiable.
"""

from typing import Dict, Any, List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

import config

SYSTEM_PROMPT = """You are the official HR Policy Assistant for Enso Group.
Your sole job is to answer employee questions strictly and exclusively using the provided context retrieved from the Enso Group HR Policy Manual.

CRITICAL INSTRUCTIONS:
1. Answer ONLY using the explicit retrieved evidence provided in the Context below.
2. Do NOT use outside knowledge, external facts, or personal assumptions.
3. Do NOT make up policies, numbers, percentages, dates, benefits, or section names.
4. If the retrieved evidence does not clearly and directly answer the question, or if the topic/value is absent from the context, return EXACTLY:
Not found
5. Do NOT treat an unrelated passage as evidence. If a specific value (such as an amount or rate) is not mentioned in the text, you MUST return:
Not found
6. If the question asks about something outside the HR manual (for example government taxes, GST, or external laws), return EXACTLY:
Not found
7. When sufficient evidence exists to answer the question, format your response EXACTLY as:
Answer: [Concise, direct answer based strictly on the text]

Reference: Page [actual page number from metadata], [actual policy/section heading from metadata]

8. When returning 'Not found', output ONLY the two words 'Not found'. Do NOT include any explanation, greeting, extra punctuation, or citation.
"""

USER_PROMPT = """Context from HR Policy Manual:
---------------------
{context}
---------------------

Employee Question: {question}

Response:"""

# Fallback models in case of free tier quota exhaustion on a specific model
FALLBACK_MODELS = [
    config.GEMINI_MODEL,
    "gemini-3-flash-preview",
    "gemma-4-26b-a4b-it",
]


def get_vector_store() -> Chroma:
    """Initializes and returns the Chroma vector store connection."""
    if not config.validate_api_key():
        raise ValueError(
            "Gemini API key is missing or invalid. Please check your '.env' file."
        )

    if not config.CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"ChromaDB directory not found at '{config.CHROMA_DIR}'.\n"
            "Please run 'python ingest.py' first to build the vector database."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=config.GEMINI_API_KEY,
    )

    return Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(config.CHROMA_DIR),
    )


def format_context(documents: List[Document]) -> str:
    """Formats retrieved document chunks with their page and section metadata."""
    formatted_chunks = []
    for doc in documents:
        page = doc.metadata.get("page", "Unknown")
        section = doc.metadata.get("section", "HR Manual")
        formatted_chunks.append(
            f"[Source: Page {page} | Section: {section}]\n{doc.page_content.strip()}"
        )
    return "\n\n".join(formatted_chunks)


def build_rag_chain(model_name: str):
    """Builds and returns the modern LangChain Runnable chain: prompt | llm | parser."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=config.GEMINI_API_KEY,
    )

    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain


def query_hr_assistant(question: str) -> Dict[str, Any]:
    """
    Executes the complete RAG query workflow:
    1. Validates inputs and API key.
    2. Retrieves top-k relevant chunks from ChromaDB.
    3. Passes context and question through the LangChain chain with resilient model fallbacks.
    4. Post-processes output to strictly enforce 'Not found' contract.
    5. Returns answer, reference, and full source context.
    """
    clean_query = question.strip()
    if not clean_query:
        return {
            "query": question,
            "raw_response": config.NOT_FOUND_RESPONSE,
            "is_found": False,
            "answer": config.NOT_FOUND_RESPONSE,
            "reference": "",
            "sources": [],
        }

    try:
        vectorstore = get_vector_store()
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": config.RETRIEVAL_TOP_K}
        )
        retrieved_docs = retriever.invoke(clean_query)
    except Exception:
        return {
            "query": question,
            "raw_response": config.NOT_FOUND_RESPONSE,
            "is_found": False,
            "answer": config.NOT_FOUND_RESPONSE,
            "reference": "",
            "sources": [],
        }

    if not retrieved_docs:
        return {
            "query": question,
            "raw_response": config.NOT_FOUND_RESPONSE,
            "is_found": False,
            "answer": config.NOT_FOUND_RESPONSE,
            "reference": "",
            "sources": [],
        }

    context_str = format_context(retrieved_docs)

    raw_output = None
    for model_name in FALLBACK_MODELS:
        try:
            chain = build_rag_chain(model_name)
            raw_output = chain.invoke(
                {"context": context_str, "question": clean_query}
            ).strip()
            if raw_output:
                break
        except Exception:
            continue

    if not raw_output:
        return {
            "query": question,
            "raw_response": config.NOT_FOUND_RESPONSE,
            "is_found": False,
            "answer": config.NOT_FOUND_RESPONSE,
            "reference": "",
            "sources": [],
        }

    # Strict normalization for 'Not found'
    normalized_lower = raw_output.lower().replace(".", "").strip()
    if (
        normalized_lower == "not found"
        or "not found" in normalized_lower[:30]
        or "does not contain" in normalized_lower
        or "cannot be answered" in normalized_lower
        or "no information" in normalized_lower
    ):
        return {
            "query": question,
            "raw_response": config.NOT_FOUND_RESPONSE,
            "is_found": False,
            "answer": config.NOT_FOUND_RESPONSE,
            "reference": "",
            "sources": [
                {
                    "page": d.metadata.get("page"),
                    "section": d.metadata.get("section"),
                    "content": d.page_content,
                }
                for d in retrieved_docs
            ],
        }

    # Parse formatted output
    answer_text = raw_output
    reference_text = ""

    lines = raw_output.split("\n")
    ans_lines = []
    ref_lines = []
    mode = "ans"

    for line in lines:
        if line.lower().startswith("reference:"):
            mode = "ref"
            ref_lines.append(line.split(":", 1)[1].strip())
        elif line.lower().startswith("answer:"):
            ans_lines.append(line.split(":", 1)[1].strip())
        else:
            if mode == "ans":
                ans_lines.append(line.strip())
            else:
                ref_lines.append(line.strip())

    if ans_lines:
        answer_text = " ".join([l for l in ans_lines if l])
    if ref_lines:
        reference_text = " ".join([l for l in ref_lines if l])
    elif retrieved_docs:
        top_doc = retrieved_docs[0]
        reference_text = f"Page {top_doc.metadata.get('page')}, {top_doc.metadata.get('section')}"

    return {
        "query": question,
        "raw_response": raw_output,
        "is_found": True,
        "answer": answer_text,
        "reference": reference_text,
        "sources": [
            {
                "page": d.metadata.get("page"),
                "section": d.metadata.get("section"),
                "content": d.page_content,
            }
            for d in retrieved_docs
        ],
    }
