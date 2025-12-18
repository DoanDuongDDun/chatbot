import pandas as pd
import faiss, pickle, os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_excel("data/laptops.xlsx")

texts = []
for _, r in df.iterrows():
    texts.append(
        f"Tên:{r['name']} | Hãng:{r['brand']} | CPU:{r['cpu']} | "
        f"RAM:{r['ram']} | SSD:{r['ssd']} | GPU:{r['gpu']} | "
        f"Màn hình:{r['screen']} | Giá:{r['price']} | {r['description']}"
    )

embeddings = model.encode(texts)

index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

os.makedirs("vectorstore", exist_ok=True)
faiss.write_index(index, "vectorstore/faiss.index")
pickle.dump(texts, open("vectorstore/texts.pkl", "wb"))

print("✅ Ingest hoàn tất")
