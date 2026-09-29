from app.retrieval.retriever import retrieve_documents


query = "Where is NovaTech headquartered?"

results = retrieve_documents(query, k=3)

print(f"\nQuery: {query}")
print(f"Retrieved {len(results)} chunks.")

for index, document in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print(document.page_content)
    print("Source:", document.metadata.get("source"))
    print("Page:", document.metadata.get("page_label"))