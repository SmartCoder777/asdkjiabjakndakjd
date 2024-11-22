# Use the official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TZ=UTC

# Set the working directory
WORKDIR /usr/src/app

# Copy all project files into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Make executables in bin/ directory executable
RUN chmod +x /usr/src/app/bin/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (if needed for future expansion)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
