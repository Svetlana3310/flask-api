# Use an official Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Set environment variables
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}

# Expose Flask port
EXPOSE 8000

# Command to run the app
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5005"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.main:app"]