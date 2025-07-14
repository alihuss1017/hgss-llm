import os 
import pandas as pd 
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import json

def load_and_chunk_json(json_path = 'data/scraped/hgss-learnables.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)

    text_chunks = []
    metadata_chunks = []

    for entry in data:
        if not isinstance(entry, dict):
            continue

        name = entry.get('Pokemon', 'Unknown Pokemon')

        def listify(moves):
            if isinstance(moves, list):
                return ", ".join([f"{m['Move']} (Lv {m['Level']})" for m in moves]) if moves and isinstance(moves[0], dict) else ", ".join(moves)
            return str(moves)
        
        chunk = f'Pokemon: {name}\n'

        for key, val in entry.items():
            if key != "pokemon":
                chunk += f"{key.title()} Moves: {listify(val)}\n"

        text_chunks.append(chunk.strip())
        metadata_chunks.append({"Source": "hgss-learnables.json"})

    return text_chunks, metadata_chunks

def load_and_chunk_csvs(dir = 'data/scraped'):
    text_chunks = []
    metadata_chunks = []
    for fname in os.listdir(dir):
        if fname.endswith('csv'):
            fpath = os.path.join(dir, fname)
            df = pd.read_csv(fpath)


            for _, row in df.iterrows():
                chunk = '\n'.join([f'{col}: {row[col]}' for col in df.columns])
                text_chunks.append(chunk)
                metadata_chunks.append({"source": fname})
    
    return text_chunks, metadata_chunks


def load_all_chunks(dir = 'data/scraped', json_path = 'data/scraped/hgss-learnables.json'):
    text_chunks = []
    metadata_chunks = []

    csv_chunks, csv_metadata = load_and_chunk_csvs(dir)
    text_chunks.extend(csv_chunks)
    metadata_chunks.extend(csv_metadata)

    json_chunks, json_metadata = load_and_chunk_json(json_path)
    text_chunks.extend(json_chunks)
    metadata_chunks.extend(json_metadata)

    return text_chunks, metadata_chunks

def build_and_save_index(text_chunks, metadata_chunks, model_name = 'all-MiniLM-L6-v2', index_path = 'data/RAG/faiss_index.index', metadata_path = 'data/RAG/metadata.pkl'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(text_chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))


    faiss.write_index(index, index_path)
    with open(metadata_path, 'wb') as f:
        pickle.dump((text_chunks, metadata_chunks), f)
    
    print(f"[✔] Saved index to '{index_path}' and metadata to '{metadata_path}'")

if __name__ == "__main__":
    chunks, metas = load_all_chunks()
    build_and_save_index(chunks, metas)