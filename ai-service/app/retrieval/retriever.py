from langchain_chroma import Chroma

from app.embeddings.embedding_model import get_embedding_model


def retrieve_documents(query: str, k: int = 3):
    """
    Retrieve the most relevant document chunks for a user query.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    results = vector_store.similarity_search(query, k=k)

    return results