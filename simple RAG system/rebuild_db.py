"""
rebuild_db.py
─────────────────────────────────────────────────────────────────────────────
OrganicAI – Vector Database Rebuild Script

Standalone utility to ingest all PDF documents from the Docs/ directory,
split text into chunks, generate HuggingFace embeddings, and rebuild the
FAISS vector store index.

Usage:
    python rebuild_db.py           # Rebuilds database (forces refresh)
    python rebuild_db.py --force   # Force rebuild vector database
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from src.ingest import (
    DOCS_DIR,
    VECTORSTORE_DIR,
    load_documents,
    split_documents,
    build_vectorstore,
    save_vectorstore,
    run_ingestion,
)
from src.utils import get_logger

logger = get_logger(__name__)


def rebuild_database(
    docs_dir: Path = DOCS_DIR,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    force: bool = True,
) -> None:
    """
    Rebuild the FAISS vector database from PDF documents.

    Pipeline Steps:
      1. load_documents(docs_dir)       : Reads all PDF files using PyPDFLoader.
      2. split_documents(documents)     : Chunks pages into overlapping segments.
      3. build_vectorstore(chunks)      : Embeds text with HuggingFace MiniLM-L6-v2.
      4. save_vectorstore(vs, dir)      : Persists index files to disk.

    Parameters
    ----------
    docs_dir : Path
        Directory containing source PDF files (default: Docs/).
    vectorstore_dir : Path
        Directory where FAISS index files will be stored (default: vectorstore/).
    force : bool
        If True, overwrites existing vectorstore files.
    """
    logger.info("Starting FAISS Vector Database Rebuild...")
    run_ingestion(
        docs_dir=docs_dir,
        vectorstore_dir=vectorstore_dir,
        force=force,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild the OrganicAI FAISS vector store database from PDF documents."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=True,
        help="Force rebuild the FAISS vector database index",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DOCS_DIR,
        help="Path to documents folder (default: Docs/)",
    )
    parser.add_argument(
        "--vectorstore-dir",
        type=Path,
        default=VECTORSTORE_DIR,
        help="Path to save FAISS vector index (default: vectorstore/)",
    )
    args = parser.parse_args()

    rebuild_database(
        docs_dir=args.docs_dir,
        vectorstore_dir=args.vectorstore_dir,
        force=args.force,
    )


if __name__ == "__main__":
    main()
