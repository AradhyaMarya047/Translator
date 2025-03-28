import time
import psutil  # For monitoring system resource usage
import threading  # For running server in a separate thread
import webbrowser  # To open API docs in browser
import uvicorn  # ASGI server to run FastAPI
from fastapi import FastAPI, Request  # FastAPI tools
from pydantic import BaseModel  # For request validation
from model import model  # Importing the TranslationModel instance from model.py

# Initialize FastAPI app with title, description, version, and documentation paths
app = FastAPI(
    title="Real-Time Translation API",
    description="An API for translation with automatic BLEU score and Perplexity computation. Includes monitoring features.",
    version="1.2",
    docs_url="/docs",    # Swagger UI
    redoc_url="/redoc"   # ReDoc UI (optional alternative docs)
)

# Define input format for translation endpoint using Pydantic
class TranslationRequest(BaseModel):
    text: str

# Initialize tracking variables for performance monitoring
request_count = 0
min_memory_usage = float("inf")  # Will track the lowest memory usage seen
max_memory_usage = float("-inf")  # Will track the highest memory usage seen

# Middleware for logging response time and monitoring memory usage
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    global request_count, min_memory_usage, max_memory_usage

    request_count += 1  # Increment total request count
    start_time = time.time()  # Record start time
    
    # Process the incoming request and get the response
    response = await call_next(request)

    # Calculate duration and current memory usage
    duration = time.time() - start_time
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # Convert bytes to MB

    # Update min and max memory usage
    min_memory_usage = min(min_memory_usage, memory_usage)
    max_memory_usage = max(max_memory_usage, memory_usage)

    # Log the request details
    print(f"📌 Request {request_count} | Response Time: {duration:.4f}s | Memory Usage: {memory_usage:.2f}MB")

    return response

# Translation endpoint: accepts text input and returns translation, BLEU, perplexity, timing, memory usage
@app.post("/translate", summary="Translate text with BLEU & Perplexity", tags=["Translation"])
def translate(request: TranslationRequest):
    start_time = time.time()  # Start timing

    # Perform translation, BLEU score (based on input vs translation), and perplexity
    translated_text = model.translate(request.text)
    bleu_score = model.compute_bleu(request.text, translated_text)
    perplexity = model.compute_perplexity(translated_text)

    # Final metrics
    duration = time.time() - start_time
    memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)

    # Return structured response
    return {
        "original_text": request.text,
        "translated_text": translated_text,
        "bleu_score": bleu_score,
        "perplexity": perplexity,
        "response_time": round(duration, 4),
        "memory_usage_MB": round(memory_usage, 2),
        "total_requests": request_count
    }

# Monitoring endpoint: returns basic usage stats
@app.get("/monitor", summary="API Usage Monitoring", tags=["Monitoring"])
def monitor():
    return {
        "total_requests": request_count,
        "min_memory_usage_MB": round(min_memory_usage, 2),
        "max_memory_usage_MB": round(max_memory_usage, 2)
    }

# Auto-start server and open Swagger docs in browser
if __name__ == "__main__":
    url = "http://127.0.0.1:8000/docs"
    print(f"🚀 Starting FastAPI server at {url}")

    # Function to start Uvicorn server
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8000)

    # Start the server in a separate daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Wait a moment to ensure the server is ready
    time.sleep(1.5)

    # Automatically open Swagger UI in browser
    webbrowser.open(url)

    # Keep the main thread alive while server runs in background
    server_thread.join()
