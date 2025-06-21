# Shalev Assist 🧠💻

**Shalev Assist** is a local command-line chatbot powered by OpenAI's GPT-3.5-turbo with smart tool usage.  
It can search the web, read and edit local files, execute Python code, install packages, and even run shell commands — all from natural language input.

---

## 💡 Project Idea

The goal of Shalev Assist is to create a command-line-based AI assistant that acts like a trimmed-down ChatGPT with actual power to:
- Interact with your local file system
- Run Python scripts
- Modify files
- Search the web
- Install Python packages
- Execute commands (with confirmation)

This makes it perfect for developers and power users who want intelligent automation — while keeping everything **local and scriptable**.

---

## 🔐 Secure API Key Setup

To use this project, you need an OpenAI API key.  
Instead of hardcoding it (which is unsafe and should never be pushed to GitHub), we store it securely using environment variables.

### ✅ Steps:

1. **Install `python-dotenv`** (if you haven't already):
   ```bash
   pip install python-dotenv
   ```

2. **Create a `.env` file** in the root directory of the project:
   ```
   OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

3. Make sure the code loads it properly (already handled in `config.py`):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

4. Ensure `.env` is **ignored by Git** by adding this line to your `.gitignore`:
   ```
   .env
   ```

---

## 🚀 How to Use

1. **Clone the repository**:
   ```bash
   git clone https://github.com/iftachshalev/shalev-assist.git
   cd shalev-assist
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the `.env` file** with your API key (as shown above).

4. **Run the assistant**:
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
shalev-assist/
├── main.py          # Main chat loop, OpenAI tool handling
├── config.py        # API key loading and global constants
├── .env             # Your OpenAI API key (excluded from Git)
├── .gitignore       # Prevents sensitive files from being tracked
└── README.md        # You’re reading it!
```

---

## 🧰 Features

- ✅ GPT-3.5 Turbo backend
- 🔧 Tool usage: web search, file reading/editing, code execution
- 🐍 Local Python execution
- 🖥️ Shell commands with user confirmation
- 📦 Python package installation
- 💬 Command-line interface with memory across turns

---

## ⚠️ Caution

This tool can:
- **Run Python code**
- **Modify local files**
- **Run terminal commands (with prompt)**

Always **read prompts and outputs carefully**. You’re in control, but with great power comes great responsibility 🧨

---

## 📦 Requirements

Create a file named `requirements.txt` and add:

```
openai
duckduckgo-search
python-dotenv
```

Install it with:

```bash
pip install -r requirements.txt
```

---

## 📜 License

MIT License.  
Use freely and modify for your needs.

---

## ✍️ Author

Built by [@iftachshalev](https://github.com/iftachshalev)
```
