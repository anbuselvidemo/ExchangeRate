# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and .env file to the working directory
COPY .. .

# Install dependencies
RUN pip install -r requirements.txt

# Command to run the Python script
CMD ["python", "fetch_exchange_rates.py"]
