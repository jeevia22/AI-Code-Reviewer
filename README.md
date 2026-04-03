# 🤖 AI Code Reviewer

An intelligent AI-powered code analysis platform that helps developers write cleaner, safer, and more efficient Python code.
It combines static analysis with AI-driven suggestions to deliver real-time feedback, improvements, and insights.

---

## 🚀 Live Demo

🔗 [(https://ai-code-reviewer-navy-panda.reflex.run/)]

---

## 📌 Features

### 🔍 Syntax Analysis

* Detects syntax errors with exact line numbers
* Prevents execution failures before runtime

### ⚠️ Bug & Issue Detection

* Infinite loops detection
* Undefined variables
* Unused variables & imports
* Logical issues

### 🤖 AI-Powered Suggestions

* Beginner-friendly explanations
* Code improvement recommendations
* Best practices based on PEP8
* Time & space complexity insights

### 🧪 Test Case Generation *(Advanced Feature)*

* Automatically generates:

  * Normal test cases
  * Edge cases
  * Expected outputs
* Helps developers validate logic effectively

### 📊 Clean UI Dashboard

* Structured output sections:

  * Syntax Result
  * Detected Issues
  * AI Suggestions
* Easy-to-use and developer-friendly interface

### 📄 Downloadable Report

* Export analysis results as a professional PDF
* Useful for documentation and reviews

---

## 🧠 How It Works

1. User inputs Python code
2. AST parser analyzes syntax and structure
3. Custom error detector finds bugs and issues
4. AI model generates suggestions and explanations
5. Results are displayed in a structured UI

---

## 🛠️ Tech Stack

### Frontend

* Reflex (Python-based full-stack framework)

### Backend

* Python
* AST (Abstract Syntax Tree)

### AI Integration

* Groq API (LLM-powered suggestions)
* LangChain

### Other Tools

* ReportLab (PDF generation)
* dotenv (environment management)

---

## 📂 Project Structure

```
ai_code_reviewer/
│
├── backend/
│   ├── code_parser.py
│   ├── error_detector.py
│   └── ai_suggester.py
│
├── ai_code_reviewer/
│   ├── pages/
│   ├── components/
│   ├── state.py
│   └── ai_code_reviewer.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/AI-Code-Reviewer.git
cd AI-Code-Reviewer
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Add Environment Variable

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 5. Run the App

```
reflex run
```

---

## 📸 Screenshots

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ef1fc242-d60a-4c58-80ed-42a926077fde" />



<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8248af37-6cb7-49ba-a5fd-cfbc729a3cf5" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/88751f8f-e169-43e7-98b7-b7cc9c96d51f" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d52226e9-8143-45b6-8a1f-beb577003374" />




---

## 🎯 Future Enhancements

* 🔄 Auto Code Fix (Refactoring)
* 📊 Code Quality Score System
* 🔐 Security Vulnerability Scanner
* 🌍 Multi-language Support
* 🎮 Gamified Coding Feedback
* 🧠 Interview Preparation Mode

---

## 🏆 Use Cases

* Students learning programming
* Developers improving code quality
* Code review automation
* Hackathons & project demonstrations

---

## 👩‍💻 Author

**Jeevia Harshini**
B.Tech AI & Data Science
Passionate about AI, Web Development, and Innovation

---

## ⭐ Acknowledgements

* Groq API
* LangChain
* Reflex Framework

---

## 📜 License

This project is for educational and demonstration purposes.

---

## 💬 Final Note

> This project goes beyond traditional code checkers by combining static analysis with AI to not just detect issues, but also explain, improve, and educate developers.

---
