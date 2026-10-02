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

[![Deploy with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Rahulkadam1221/Text-Summarization-NLP&branch=main&mainModule=streamlit_app.py)
[![GitHub](https://img.shields.io/badge/GitHub-Rahulkadam1221/Text--Summarization--NLP-blue?logo=github)](https://github.com/Rahulkadam1221/Text-Summarization-NLP)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent NLP text summarization application featuring an extractive word frequency algorithm, high-contrast accessible UI, history management, project folders, and zero-API local execution.

---

## ✨ Features

- 📄 **Direct Text & URL Extraction** - Summarize pasted text or fetch and scrape live web articles directly.
- 🎛️ **Length & Tone Customization** - Choose between Short, Medium, Long, or custom sentence counts, plus Casual, Professional, or Academic tones.
- 📚 **Summary Library & Projects** - Organize your past summaries into custom project folders with local persistence.
- 📊 **Real-time Metrics Dashboard** - Instant word count, sentence count, reading time, and percentage reduction stats.
- 🎨 **High Contrast & Accessible UI** - Clean light main content layout with rich dark sidebar navigation and legible typography.
- 🚀 **Zero External APIs Needed** - Works completely offline using Python NLP frequency algorithms.
- 💻 **CLI & Web App** - Run as a modern Streamlit web dashboard or as a terminal CLI tool.

---

## 🚀 Quick Start (Local)

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

### 4. Run the Streamlit Web Application
```bash
streamlit run streamlit_app.py
```
Then visit `http://localhost:8501` in your browser.

---

## 💻 CLI Usage

Summarize text directly from the command line:

```bash
# From direct pipe
echo "Your article text here..." | python app.py

# From a file
python app.py --file document.txt --num-sentences 4

# From a URL
python app.py --url https://en.wikipedia.org/wiki/Natural_language_processing --num-sentences 3
```

---

## 🌐 Cloud Deployment Options

### Option 1: Streamlit Community Cloud (Recommended & Instant)
1. Click the button below:  
   [![Deploy with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Rahulkadam1221/Text-Summarization-NLP&branch=main&mainModule=streamlit_app.py)
2. Sign in with GitHub.
3. Confirm repository `Rahulkadam1221/Text-Summarization-NLP`, branch `main`, and main file path `streamlit_app.py`.
4. Click **Deploy!**. Your application will be live in 1–2 minutes with a free HTTPS URL.

### Option 2: Docker Container
Run the containerized application anywhere:
```bash
# Build the Docker image
docker build -t summarize-ai .

# Run the container
docker run -p 8501:8501 summarize-ai
```
Then open `http://localhost:8501`.

### Option 3: Render / Railway / Heroku
The included [`Procfile`](Procfile) and [`Dockerfile`](Dockerfile) are pre-configured:
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### Option 4: Hugging Face Spaces
1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Choose **Streamlit** SDK.
3. Link your GitHub repository `Rahulkadam1221/Text-Summarization-NLP` or push to the Space's Git remote.

---

## 📂 Project Structure

```
├── .streamlit/
│   └── config.toml        # Streamlit production configurations
├── app.py                 # Extractive NLP algorithm & CLI tool
├── streamlit_app.py       # Full-featured Streamlit Web Dashboard
├── Dockerfile             # Production Docker container configuration
├── Procfile               # PaaS deployment specification (Render/Railway)
├── requirements.txt       # Python dependencies
├── .dockerignore          # Docker build exclusion rules
├── .gitignore             # Git exclusion rules
└── README.md              # Project documentation
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
