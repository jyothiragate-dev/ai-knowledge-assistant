from pathlib import Path

from app.embeddings.embedding_model import get_embedding_model
from app.ingestion.document_loader import load_pdf
from app.ingestion.text_splitter import split_documents
from app.vectorstore.vector_store import create_vector_store


DOCUMENTS_DIRECTORY = Path("data/documents")


def ingest_pdf(file_path: str):
    """
    Load, chunk, embed and store a PDF in the vector database.
    """

    # Load the PDF into LangChain Document objects.
    documents = load_pdf(file_path)

    # Split the document pages into smaller chunks.
    chunks = split_documents(documents)

    # Create the embedding model used to convert chunks into vectors.
    embedding_model = get_embedding_model()

    # Store the chunks, embeddings and metadata in Chroma.
    create_vector_store(
        chunks=chunks,
        embedding_model=embedding_model
    )

    return {
        "pages": len(documents),
        "chunks": len(chunks)
    }