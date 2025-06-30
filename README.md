# Pokémon HGSS Data + LLM QA Assistant

This project is an exploration into building a structured knowledge base of Pokémon HeartGold and SoulSilver (HGSS) and enabling question-answering using a pretrained large language model (LLM). The goal is to create a system that can answer questions like:

- "Where can I find Dragon Claw?"
- "What TM does Jasmine give you?"
- "Which Pokémon can be found in Route 32 at night?"

--- 
## 📦 Project Structure

### 🕸️ Web Scraping Scripts

We have implemented custom scrapers using `requests` and `BeautifulSoup` to collect and store Pokémon HGSS data into structured CSV files.

#### ✔️ Modules:
- `hgss-gyms.py`: Extracts gym leader information including name, location, type specialty, team, badge, TMs given, and obedience level.
- `hgss-items.py`: (planned or in progress) Scrapes item data such as TMs, HMs, and key items.
- `hgss-moves.py`: Extracts move information including type, category, power, accuracy, and effect.
- `hgss-pokelocs.py`: Collects wild encounter data — which Pokémon can be found in which location, at what level, time of day, and method.
- `hgss-pokemon.py`: Retrieves individual Pokémon stats and typing.

All output is stored in the `data/` directory in CSV format for easy loading.

---

### 🤖 LLM Integration

#### Model Used
- [Microsoft's Phi-2](https://huggingface.co/microsoft/phi-2) – a small, powerful transformer-based language model.

#### What’s Been Done:
- Loaded `phi-2` using the Hugging Face `transformers` library.
- Prompt-engineered basic queries using structured Pokémon CSV data.
- Manual prompting has been tested for questions like:
  - `"Where can I find Pidgey?"`
  - `"What TM does Falkner give?"`

---

## 📊 Sample Data

Examples of structured data CSVs produced:
- `hgss-gyms.csv`
- `hgss-items.csv`
- `hgss-moves.csv`
- `hgss-pokemon.csv`
- `hgss-pokemon_locations.csv`

Each file contains clearly labeled columns and can be loaded with `pandas` or converted to JSON for further use in retrieval pipelines.

---

## 🛠️ Planned Next Steps

- [ ] Implement Retrieval-Augmented Generation (RAG) using tools like LangChain or Haystack.
- [ ] Index CSV data into a vector store (e.g., FAISS or Chroma).
- [ ] Automatically generate QA pairs for fine-tuning or eval.
- [ ] Optionally fine-tune a small model on curated examples.
- [ ] Deploy a QA chatbot frontend via Streamlit or Gradio.

---
## 👤 Team Members

- Ali Hussain — *(ECE M.S. in Machine Learning and Data Science @ UCSD)*    
- Umar Khan — *(CSE B.S./M.S. @ UCSD)*   



---

## 🙏 Credits

- **Serebii.net** — for detailed and structured information on gym leaders, items, and in-game mechanics.  
  Website: [https://www.serebii.net/](https://www.serebii.net/)

- **Pokémon Database (pokemondb.net)** — for accurate data on Pokémon locations, stats, and moves.  
  Website: [https://pokemondb.net/](https://pokemondb.net/)


---