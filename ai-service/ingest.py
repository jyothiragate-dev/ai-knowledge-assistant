from app.ingestion.document_loader import load_pdf
from app.ingestion.text_splitter import split_documents
from app.embeddings.embedding_model import get_embedding_model
from app.vectorstore.vector_store import create_vector_store

file_path = "data/documents/rag_test_dataset.pdf"

documents = load_pdf(file_path)
chunks = split_documents(documents)

print(f"Loaded {len(documents)} pages.")
print(f"Created {len(chunks)} chunks.")

embedding_model = get_embedding_model()
vector_store = create_vector_store(chunks, embedding_model)
print("Vector store created successfully.")