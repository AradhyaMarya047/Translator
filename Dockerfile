# Use a minimal Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the frontend files
COPY . .

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
