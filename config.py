"""
Configuration module for the HR Policy Assistant RAG Chatbot.
Centralizes paths, model settings, retrieval parameters, and API configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Gemini API Key configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Model Configurations
# gemini-3.5-flash-lite offers high accuracy, fast generation, and independent daily quota
# models/gemini-embedding-001 generates 3072-dimensional semantic embeddings
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

# File and Directory Paths
DATA_DIR = BASE_DIR / "data"
PDF_PATH = DATA_DIR / "hr_manual.pdf"
CHROMA_DIR = BASE_DIR / "chroma_db"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
COLLECTION_NAME = "hr_policy_collection"

# Text Splitting / Chunking Parameters
# 1000 characters with 150 character overlap preserves full policy clauses and context
# while keeping chunk sizes focused for accurate embedding retrieval.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# Retrieval Configuration
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))

# Fallback string required by specification
NOT_FOUND_RESPONSE = "Not found"


def validate_api_key() -> bool:
    """Check if the Gemini API key is configured and not a placeholder."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return False
    return True
