import faiss, pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vectorstore/faiss.index")
texts = pickle.load(open("vectorstore/texts.pkl", "rb"))

def retrieve(query, k=3):
    q = model.encode([query])
    _, ids = index.search(q, k)
    return [texts[i] for i in ids[0]]
