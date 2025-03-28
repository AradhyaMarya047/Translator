# 🌍 Real-Time Translation API

A FastAPI-powered real-time translation API that converts **English** text to **French** using Google Translate and evaluates the quality of translation using **BLEU Score** and **Perplexity**. It also tracks memory usage and response time for every request.

---

## 👥 Who Is This For?

This project is perfect for:

- 🧑‍🎓 **Students & Researchers** working on NLP, machine translation, or language modeling
- 👨‍💻 **Developers** building translation features into applications
- 📚 **Educators** teaching about BLEU scores, perplexity, and API architecture
- ⚙️ **Engineers** interested in real-time performance monitoring and FastAPI

---

## 📦 Features

- ✅ Translates English text into French using **Google Translate**
- 📊 Computes **BLEU Score** to evaluate translation accuracy
- 📉 Calculates **Perplexity** using Hugging Face’s `facebook/m2m100_418M` model
- 📈 Tracks total requests, response time, and memory usage
- 🔎 Swagger UI & ReDoc API documentation
- 🌐 Automatically opens documentation on server start

---

## 🗃️ Project Structure

            +-------------------------+
            |   End User (Client)     |
            |  (e.g. Postman, Browser)|
            +-----------+-------------+
                        |
                        | 1. Send POST request with text
                        v
            +-----------+-------------+
            |       FastAPI Server    |
            |       (main.py)         |
            +-----------+-------------+
                        |
                        | 2. Calls TranslationModel
                        v
            +-----------+-------------+
            | model.py:               |
            | - Google Translate API  |
            | - BLEU Score via NLTK   |
            | - Perplexity via HF     |
            +-----------+-------------+
                        |
                        | 3. Return translated text and metrics
                        v
            +-------------------------+
            |     JSON Response       |
            +-------------------------+
