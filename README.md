---
title: Summarize AI - Text Summarization NLP
emoji: ✦
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.40.0
app_file: streamlit_app.py
pinned: false
---

# ✦ Summarize AI - Intelligent Text Summarizer

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://text-summarization-nlp-eprgiuzfrpvfyjbsy5rygy.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Rahulkadam1221/Text--Summarization--NLP-blue?style=for-the-badge&logo=github)](https://github.com/Rahulkadam1221/Text-Summarization-NLP)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🚀 **Live Application:** Access the live deployed app at **[text-summarization-nlp-eprgiuzfrpvfyjbsy5rygy.streamlit.app](https://text-summarization-nlp-eprgiuzfrpvfyjbsy5rygy.streamlit.app/)**

An intelligent NLP text summarization application featuring an extractive word frequency algorithm, high-contrast accessible UI, history management, project folders, and zero-API local execution.

---

## ✨ Features & Capabilities

- 📄 **Dual Input Modes** — Paste raw text or enter any web article URL for automatic HTML stripping and content extraction.
- 🎛️ **Customizable Length & Tone**:
  - **Length Presets:** Short (2-3 sentences), Medium (4-5 sentences), Long (6-8 sentences), or custom sentence counts.
  - **Tone Adaptation:** Casual (concise & easy), Professional (balanced & objective), Academic (comprehensive & formal).
- 📊 **Real-time Analytics Dashboard** — Instant metrics showing original words, summary words, sentence counts, estimated reading time saved, and reduction percentage (typically 80–95%).
- 📚 **Summary Library** — Automatically save summaries with timestamp, length, tone, metrics, and full-text copy capabilities.
- 📁 **Project Workspace** — Organize summaries into dedicated project folders for research, study, or work topics.
- ⚙️ **User Preferences** — Set your custom username, default summary length, and preferred default tone.
- 🎨 **Modern High-Contrast UI** — Sleek dark navigation sidebar paired with a clean, high-contrast content area designed for readability.
- 🚀 **100% Offline & Private** — Runs entirely locally with zero external API dependencies or token costs. All data stays on your machine.
- 💻 **Dual Interface** — Interactive web application powered by Streamlit and a fast command-line CLI tool.

---

## 🧠 How It Works (Extractive Summarization)

```
[Raw Text / Web URL]
        │
        ▼
 1. Text Extraction & Cleaning (BeautifulSoup / Regex)
        │
        ▼
 2. Sentence & Word Tokenization
        │
        ▼
 3. Stopword Removal & Word Frequency Calculation
        │
        ▼
 4. Sentence Scoring (Word Weights + Positional Bias)
        │
        ▼
 5. Length & Tone Filtering (Top-N Sentence Extraction)
        │
        ▼
 [Concise, Hallucination-Free Summary]
```

Unlike generative AI models that can hallucinate or alter facts, **extractive summarization** identifies and extracts the most significant verbatim sentences from the source text based on normalized word importance weights and sentence position scoring.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Rahulkadam1221/Text-Summarization-NLP.git
cd Text-Summarization-NLP
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Web Application
```bash
streamlit run streamlit_app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 💻 Command-Line Interface (CLI)

The project includes `app.py` for terminal-based summarization:

```bash
# From direct piped input
echo "Natural Language Processing is a field of AI..." | python app.py

# From a text file
python app.py --file article.txt --num-sentences 4

# From any article URL
python app.py --url https://en.wikipedia.org/wiki/Natural_language_processing --num-sentences 3
```

CLI options:
- `-f, --file` — Path to input text file
- `-u, --url` — URL to fetch and summarize
- `-n, --num-sentences` — Number of sentences to extract (default: 3)

---

## 🌐 Cloud Deployment Options

### Option 1: Streamlit Community Cloud (Live Production)
- 🔗 **Production App:** [text-summarization-nlp-eprgiuzfrpvfyjbsy5rygy.streamlit.app](https://text-summarization-nlp-eprgiuzfrpvfyjbsy5rygy.streamlit.app/)
- **Auto-deployment:** Connected directly to the `main` branch of this repository; code updates deploy automatically in real-time.

### Option 2: Docker Container
Run anywhere with Docker:
```bash
# Build Docker image
docker build -t text-summarizer-nlp .

# Run container on port 8501
docker run -p 8501:8501 text-summarizer-nlp
```
Then visit `http://localhost:8501`.

### Option 3: Render / Railway / Heroku
The repository contains both [`Procfile`](Procfile) and [`Dockerfile`](Dockerfile) for zero-config PaaS deployment:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### Option 4: Hugging Face Spaces
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space.
2. Select the **Streamlit** SDK.
3. Connect your GitHub repository `Rahulkadam1221/Text-Summarization-NLP`.

---

## 📂 Project Structure

```
├── .streamlit/
│   └── config.toml        # Streamlit production configurations
├── app.py                 # Core extractive algorithm & CLI application
├── streamlit_app.py       # Full-featured Streamlit Web Dashboard
├── Dockerfile             # Production container setup (Python 3.11-slim)
├── Procfile               # PaaS deployment specification
├── requirements.txt       # Production dependencies
├── .dockerignore          # Docker build exclusion rules
├── .gitignore             # Git exclusion rules
├── LICENSE                # MIT License
└── README.md              # Project documentation
```

---

## 👨‍💻 Author

**Rahul Kadam**
- GitHub: [@Rahulkadam1221](https://github.com/Rahulkadam1221)
- Repository: [Text-Summarization-NLP](https://github.com/Rahulkadam1221/Text-Summarization-NLP)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
