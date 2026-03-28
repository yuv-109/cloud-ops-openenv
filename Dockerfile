# Use the official Python image
FROM python:3.10-slim

# Set the folder inside the container where our code will live
WORKDIR /app

# Copy your requirements first (this makes building faster)
COPY requirements.txt .

# Install the libraries (fastapi, uvicorn, pydantic, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY main.py .
COPY models.py .
COPY openenv.yaml .

# Tell the container to listen on port 7860 (Hugging Face default)
EXPOSE 7860

# The command to start your FastAPI app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]