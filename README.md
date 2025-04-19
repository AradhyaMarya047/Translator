# 🌍 Real-Time English ➜ French Translation API with Streamlit Frontend

A full-stack **real-time translation application** that uses a **FastAPI backend** and an **interactive Streamlit frontend** to translate English text to French. The app integrates **Google Translate**, evaluates output using **BLEU Score** and **Perplexity**, and visualizes insights with **SHAP Beeswarm plots**. It also tracks performance metrics like response time and memory usage.

---

## 👥 Who Is This For?

This project is perfect for:

- 🧑‍🎓 **Students & Researchers** working on NLP, machine translation, or model explainability  
- 👨‍💻 **Developers** integrating real-time translation into web apps  
- 📚 **Educators** teaching model evaluation, APIs, or SHAP  
- 🛠️ **Engineers** interested in containerization and GCP deployment  

---

## ⚙️ Features

✅ Translate English text to **French**  
📊 Compute **BLEU Score** to evaluate translation accuracy  
📉 Calculate **Perplexity** using Hugging Face's `facebook/m2m100_418M`  
🔒 **Input Validation** using Pydantic  
✅ **SHAP Beeswarm** plots for translation explainability  
🛡️ **Great Expectations** for optional data contract enforcement  
📟 Monitor **response time**, **memory usage**, and **total requests**  
🧪 View and test all endpoints using **Swagger UI** and **ReDoc**  
🖥️ Beautiful **Streamlit frontend** with voice support and TTS  

---

## 🧱 Architecture Overview

```txt
+--------------------------+
|      End User           |
|  (Browser / Streamlit)  |
+-----------+--------------+
            |
            | 1. Send input text
            v
+-----------+--------------+
|  Streamlit Frontend      |
|  - Collects input        |
|  - Shows translation     |
|  - Sends POST to FastAPI |
+-----------+--------------+
            |
            | 2. API Request
            v
+-----------+--------------+
|  FastAPI Backend          |
|  - Validation (/validate)|
|  - Translation (/translate)
|  - Returns scores & metrics
+-----------+--------------+
            |
            | 3. Translation + SHAP
            v
+-----------+--------------+
|  model.py                |
|  - Google Translate      |
|  - BLEU (NLTK)           |
|  - Perplexity (HF)       |
|  - SHAP beeswarm         |
+-----------+--------------+
            |
            | 4. JSON Response
            v
+--------------------------+
|  Streamlit Displays      |
|  - Translated text       |
|  - BLEU & Perplexity     |
|  - Beeswarm plot         |
|  - Metrics & Voice       |
+--------------------------+
