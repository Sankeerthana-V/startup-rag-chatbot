from pathlib import Path
from pypdf import PdfReader
from vector_store import collection

pdf_folder = Path("pdfs")

all_chunks = []

for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"\nReading: {pdf_file.name}")

    reader = PdfReader(pdf_file)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    chunk_size = 1000

    for i in range(0, len(full_text), chunk_size):
        chunk = full_text[i:i + chunk_size]
        all_chunks.append({
            "id": f"{pdf_file.stem}_{i}",
            "source": pdf_file.name,
            "content": chunk
        })

for chunk in all_chunks:
    collection.add(
        ids=[chunk["id"]],
        documents=[chunk["content"]],
        metadatas=[{"source": chunk["source"]}]
    )

print(f"Inserted {len(all_chunks)} chunks into ChromaDB")