# Use a official lightweight Python 3.12 image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy the backend and frontend folders into the container
COPY backend ./backend
COPY frontend ./frontend

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application using uvicorn
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
