# 🤖 Agentic AI Code Generator

A local-first, privacy-focused AI development assistant. This application features a **React** frontend with a split-screen code editor and a **FastAPI** backend that streams responses from a local **Llama 3** model.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

* **Split-Screen Interface:** Chat on the left, live code workspace on the right.
* **Real-Time Streaming:** AI responses appear token-by-token (like ChatGPT).
* **Live Preview:** Instantly render generated HTML/CSS/JS code in a secure sandbox.
* **Syntax Highlighting:** VS Code-style dark theme for code blocks.
* **Local AI Power:** Runs entirely on your machine using **Ollama** (Zero API costs, 100% private).
* **Auto-Healing Backend:** Automatically detects if Ollama is off and starts it for you.

---

## 🛠️ Tech Stack

### **Frontend (User Interface)**
* **React 18:** Core UI library.
* **React Router Dom:** For navigation (Chat, History, Settings).
* **React Markdown & Remark GFM:** To render rich text and tables from the AI.
* **React Syntax Highlighter (Prism):** For beautiful code block formatting.
* **Fetch API:** For handling streaming text data.

### **Backend (API & Logic)**
* **Python 3.10+:** Core language.
* **FastAPI:** High-performance web framework.
* **Uvicorn:** ASGI server for production-grade performance.
* **LangChain (Ollama & Core):** Framework for orchestrating the AI interaction.
* **Subprocess & Requests:** For managing the local Ollama server instance.

### **AI Engine**
* **Ollama:** The local inference server.
* **Llama 3:** The Large Language Model (LLM) by Meta.

---

## 🏗️ Architecture: How it Works

1.  **User Input:** You type a prompt (e.g., "Create a login page") in the **React Frontend**.
2.  **API Request:** React sends a `POST` request to the **FastAPI Backend** (`http://localhost:8000/chat`).
3.  **AI Inference:** FastAPI sends the prompt to **Ollama** running locally on port `11434`.
4.  **Streaming:** Ollama generates tokens. FastAPI intercepts them and streams them chunk-by-chunk to React.
5.  **Rendering:**
    * React Markdown renders text in the Chat Panel.
    * The "Code Extractor" detects code blocks and sends them to the **Workspace Panel** for preview.

---

## 🚀 Installation Guide

### Step 0: Install Ollama (Required)
This project uses **Llama 3**, which runs inside Ollama. You must install this first.

* **macOS / Linux:**
    1.  Download from [ollama.com](https://ollama.com/download).
    2.  Install and run the application once to complete setup.
    3.  Open your terminal and run:
        ```bash
        ollama pull llama3
        ```
* **Windows:**
    1.  Download the Windows Preview from [ollama.com](https://ollama.com/download).
    2.  Run the installer.
    3.  Open PowerShell or Command Prompt and run:
        ```bash
        ollama pull llama3
        ```

> **Verification:** Run `ollama run llama3` in your terminal. If you can chat with the AI, you are ready. Type `/bye` to exit.

---

### Step 1: Backend Setup
The backend is a Python application. We recommend using a virtual environment.

1.  **Navigate to the backend folder:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    
    # Mac/Linux
    python3 -m venv venv
    ```

3.  **Activate the environment:**
    ```bash
    # Windows
    .\venv\Scripts\activate
    
    # Mac/Linux
    source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn langchain-ollama langchain-core requests
    ```

5.  **Start the Server:**
    ```bash
    python main.py
    ```
    *You should see: `✅ Ollama server started successfully!` followed by `Uvicorn running on http://0.0.0.0:8000`*

---

### Step 2: Frontend Setup
The frontend is a React application.

1.  **Open a NEW terminal window** (keep the backend running).

2.  **Navigate to the frontend folder:**
    ```bash
    cd frontend
    ```

3.  **Install Node dependencies:**
    ```bash
    npm install react-router-dom react-markdown remark-gfm react-syntax-highlighter
    ```

4.  **Start the UI:**
    ```bash
    npm start
    ```

5.  **Open your browser:**
    Go to `http://localhost:3000`.

---

## 💡 Usage

1.  **Start Chatting:** In the input box, type: *"Create a landing page for a coffee shop."*
2.  **Watch the Stream:** The AI will explain its plan in the **Left Panel**.
3.  **View the Code:** As the AI writes HTML/CSS, it will appear in the **Right Panel**.
4.  **Switch Tabs:** Click **"👁️ Preview"** in the top right to render the HTML instantly. Click **"💻 Code"** to see the raw syntax.

---

## ❓ Troubleshooting

**Q: I get a "Connection Refused" error.**
* Ensure the backend is running (`python main.py`).
* Ensure the backend port is `8000`.

**Q: The AI is slow.**
* Llama 3 requires about 8GB of RAM. If your computer is older, open `backend/main.py` and change the model to `llama3.2` (a smaller, faster model), then run `ollama pull llama3.2`.

**Q: "Ollama not found" error in backend.**
* Ensure Ollama is installed and added to your system PATH. Try running `ollama` in a fresh terminal to verify.

---

Made with ❤️ by [Your Name]