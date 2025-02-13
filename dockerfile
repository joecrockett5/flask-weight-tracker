# Use an official Python runtime as the base image
FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that the app will run on, random for use with cloudflare
EXPOSE 4286

# Run the app with Gunicorn (use 4 worker processes for production)
CMD ["gunicorn", "--bind", "0.0.0.0:4286", "app:app"]
