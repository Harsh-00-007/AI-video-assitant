# AI Video & Meeting Assistant

## 📌 Overview
An intelligent, terminal-based pipeline that transforms long-form YouTube videos and local meeting recordings into structured, actionable intelligence. 

This system handles media downloading, intelligent audio chunking, robust speech-to-text transcription, and utilizes a **Retrieval-Augmented Generation (RAG)** architecture to allow users to semantically "chat" with the video context.

## 🚀 Key Engineering Features
* **Automated Media Pipeline:** Integrates `yt-dlp` and `ffmpeg` to seamlessly extract and process audio from live YouTube URLs or local media files.
* **Resilient API Orchestration:** Implements an exponential backoff and retry mechanism to handle third-party API rate-limiting and connection drops (specifically tailored for Sarvam AI's 30-second payload limits).
* **LLM-Powered Extraction:** Automatically distills hours of audio into:
  * Executive Summaries
  * Action Items
  * Key Decisions
  * Unresolved / Open Questions
* **Conversational RAG Engine:** Leverages **LangChain** and **ChromaDB** to embed transcripts into a local vector space, enabling users to ask highly specific questions about the meeting/video and receive context-aware answers.

## 🛠️ Tech Stack
* **Core Language:** Python 3.11+
* **AI & LLM Frameworks:** LangChain, OpenAI (Embeddings/Chat), Sarvam AI (Transcription)
* **Vector Database:** Chroma (`chromadb`)
* **Media Processing:** `yt-dlp`, `pydub`, `ffmpeg`
* **Architecture:** Modular component design (`core/`, `utils/`)