# Pokémon HeartGold and Soulsilver QA Assistant

<p align="center">
  <img src="https://www.pokemon.com/static-assets/content-assets/cms2/img/video-games/video-games/pokemon_heart_gold_soul_silver/pokemon_heart_gold_soul_silver_main_169.jpg">
  <br>
  <sub>Image © Nintendo / Game Freak / The Pokémon Company. Source: <a href="https://www.pokemon.com/">pokemon.com</a></sub>
</p>


This project is an exploration into building a structured knowledge base of Pokémon HeartGold and SoulSilver (HGSS) and enabling question-answering using a small pretrained large language model (LLM). The goal is to create a system that can answer questions like:

- "Where can I find Dragon Claw?"
- "What TM does Jasmine give you?"
- "Which Pokémon can be found in Route 32 at night?"

## 🗂️ Project Structure
```
data/
  RAG/
    faiss_index.index        ← FAISS vector index
    metadata.pkl             ← Metadata (e.g., source chunks)
  scraped/
    *.csv / *.json           ← Scraped and structured HGSS game data

src/
  *.py                       ← Individual scrapers for each data type
  RAG-setup.py               ← Index building and RAG pipeline logic

main.ipynb                   ← Demo notebook using Phi-2 and basic RAG
README.md
requirements.txt
```
---
## 🕸️ Scraped Pokémon HGSS Dataset

We implemented custom scrapers using `requests` and `BeautifulSoup`  to gather structured data from HGSS-related sources. 


### 📁 Datasets include:
- `hgss-gyms.csv`: Gym leader names, badges, TM rewards, trade obedience levels, etc. 
- `hgss-items.csv`: In-game items like evolutionary items, held items, healing items, etc.
- `hgss-moves.csv`: Move properties –– power, accuracy, type, category.
- `hgss-pokemon.csv`: Pokémon base stats, types, abilties.
- `hgss-pokelocs.csv`: Pokémon wild encounter locations and conditions. 
- `hgss-abilities.csv`: Descriptions of each ability.
- `hgss-egg_group.csv`: Contains list of Pokémon in each egg group. 
- `hgss-evolutions.csv`: Contains each Pokémon's evolution and condition. 
- `hgss-learnables.json`: Contains all moves and the method(s) they can be learned, with a list of Pokémon for each method. 

---

## 🤖 LLM + RAG Integration
### ✅ Current Status
- Implemented <b> basic RAG </b> pipeline using:
  - `faiss` for vector storage and efficient similarity search.
  - `phi-2` via Hugging Face Transformers for generation.
  - Basic chunking for CSV and JSON data. 
- Created an index of knowledge chunks with FAISS.
- Simple Colab notebook (`main.ipynb`) demonstrates QA with a few structured queries. 

### ⚡ Example Questions
- <i>"Which Pokémon can learn Ice Beam?"</i>
- <i>"What is Falkner's Team?"</i>
- <i>"How much power is Focus Punch?"</i>

### 🚧 Roadmap
#### 🔬 Ongoing + Planned Work
- Expand model support (e.g. Pythia, Mistral, TinyLLama)
- Incorporate better chunking techniques (e.g. semantic, sentence windowing)
- Add evaluation using formal QA benchmarks and hand-crafted QA pairs.
- Curate a RAFT-style dataset for fine-tuning. 
- Improve RAG response formatting (structured citations, avoiding hallucinations.)
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

This project is for <b>research and educational purposes only</b>. All Pokémon names, data, and media are © Nintendo/Game Freak. No copyright infringement is intended.

---