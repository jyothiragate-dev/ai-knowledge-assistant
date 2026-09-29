from langchain_openai import ChatOpenAI

from app.retrieval.retriever import retrieve_documents


def generate_answer(query: str):
    """
    Generate an answer using only the context retrieved from the vector store.
    """

    documents = retrieve_documents(query, k=3)

    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are an AI knowledge assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find that information in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    response = llm.invoke(prompt)

    sources = [
        {
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page_label")
        }
        for document in documents
    ]

    return {
        "answer": response.content,
        "sources": sources
    }