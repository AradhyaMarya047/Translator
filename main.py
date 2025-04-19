# --- System & Server Utilities ---
import time
import psutil  # For tracking memory usage
import threading  # To run the server in the background
import webbrowser  # To open the API docs in a browser
import uvicorn  # ASGI server for FastAPI

# --- FastAPI Components ---
from fastapi import FastAPI, Request  # Core FastAPI features
from fastapi.responses import JSONResponse  # Custom response
from pydantic import BaseModel, validator  # Request validation

# --- ML Translation Model ---
from model import model  # Import the TranslationModel class instance

# --- Regex for input validation ---
import re

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Real-Time Translation API",
    description="An API for translation with BLEU & Perplexity scores. Includes validation and monitoring.",
    version="1.0",
    docs_url="/docs",     # Swagger UI
    redoc_url="/redoc"    # Alternative ReDoc UI
)

# --- Request Schema using Pydantic ---
class TranslationRequest(BaseModel):
    text: str

    # Custom validator to check the input text rules
    @validator("text")
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("Text must not be empty.")
        if len(value) > 1000:
            raise ValueError("Text must be less than 1000 characters.")
        if not re.match(r"^[A-Za-z0-9\s.,!?@'\"()]+$", value):
            raise ValueError("Text contains invalid characters.")
        return value

# --- Global Stats for Monitoring ---
request_count = 0
min_memory_usage = float("inf")
max_memory_usage = float("-inf")

# --- Middleware for Logging and Monitoring ---
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    global request_count, min_memory_usage, max_memory_usage
    request_count += 1
    start_time = time.time()

    # Process the actual request
    response = await call_next(request)

    # Calculate response time and memory
    duration = time.time() - start_time
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)

    # Track min/max memory usage
    min_memory_usage = min(min_memory_usage, memory_usage)
    max_memory_usage = max(max_memory_usage, memory_usage)

    # Print request log
    print(f"📌 Request {request_count} | Response Time: {duration:.4f}s | Memory Usage: {memory_usage:.2f}MB")
    return response

# --- /translate Endpoint ---
@app.post("/translate", tags=["Translation"])
def translate(request: TranslationRequest):
    start_time = time.time()

    # Call model to get translation + evaluation scores
    translated_text = model.translate(request.text)
    bleu_score = model.compute_bleu(request.text, translated_text)
    perplexity = model.compute_perplexity(translated_text)

    # Response time & memory usage
    duration = time.time() - start_time
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)

    return {
        "original_text": request.text,
        "translated_text": translated_text,
        "bleu_score": bleu_score,
        "perplexity": perplexity,
        "response_time": round(duration, 4),
        "memory_usage_MB": round(memory_usage, 2),
        "total_requests": request_count
    }

# --- /validate Endpoint ---
@app.post("/validate", tags=["Validation"])
def validate_input(request: TranslationRequest):
    try:
        # If validation passed via Pydantic, return success
        request_dict = request.dict()
        return {"success": True, "message": "Valid input"}
    except Exception as e:
        # Return error message if something fails
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

# --- /monitor Endpoint ---
@app.get("/monitor", tags=["Monitoring"])
def monitor():
    return {
        "total_requests": request_count,
        "min_memory_usage_MB": round(min_memory_usage, 2),
        "max_memory_usage_MB": round(max_memory_usage, 2)
    }

# --- Auto-start Uvicorn Server and Open Swagger UI ---
if __name__ == "__main__":
    url = "http://127.0.0.1:8000/docs"
    print(f"🚀 Launching API at {url}")

    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000)

    # Run FastAPI server in a daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1.5)  # Give time for server to spin up
    webbrowser.open(url)  # Open Swagger UI in browser
    server_thread.join()  # Keep server alive
