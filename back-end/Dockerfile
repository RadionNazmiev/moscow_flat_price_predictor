# Use the official Python image as base image
FROM python:3.10

# Copy the requirements file into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

RUN pip install --upgrade pip
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
