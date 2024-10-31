# Use a lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose port if your app listens on a specific port (optional, e.g., 8080)
EXPOSE 8080

# Run the Python application
CMD ["python", "main.py"]