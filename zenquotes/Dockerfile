# Base image
FROM python:3.11-slim

# Work directory
WORKDIR /app

# Copy files 
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment
ENV PYTHONUNBUFFERED=1

# Command
CMD ["python", "-m", "app.main"]