from vector_store import collection

query = "What are the benefits given to startups under Startup India?"

results = collection.query(
    query_texts=[query],
    n_results=3
)

print(results)