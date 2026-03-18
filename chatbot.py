from openai import OpenAI
from dotenv import load_dotenv
import os
from vector_store import collection

SYSTEM_PROMPT = """
You are a chatbot that answers only questions related to Indian startups.

Rules:
1. Answer ONLY using the provided document context.
2. Do NOT add information from your own knowledge.
3. If the answer is not clearly present in the documents, say:
   "I do not have enough information"
4. Do NOT answer unrelated topics such as politics, war, sports, or general world news.
5. If the question is outside Indian startups, say:
   "I can only help with questions related to Indian startups."
6. Keep answers clear, structured.
7. Give answers in bullet points if possible.
"""

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_response(user_input, chat_history):
    results = collection.query(
        query_texts=[user_input],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    context = ""
    for i, doc in enumerate(retrieved_docs):
       context += f"\nDocument {i+1}:\n{doc}\n"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Document context:\n{context}"}
    ]

    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content