# Gunakan Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy file
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Command to run app
CMD ["python", "app.py"]
