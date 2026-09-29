from app.generation.rag_service import generate_answer

query = "Who is the CEO of NovaTech?"

result = generate_answer(query)

print(f"\nQuestion: {query}")

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(f"- {source['source']} | Page {source['page']}")