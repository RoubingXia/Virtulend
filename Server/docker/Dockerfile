# Use a base image with Python and required dependencies
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your app.py file to the Apache document root directory
COPY *.py /app
COPY *.json /app
COPY *.npy /app
COPY requirements.txt /app

# Set the environment variable for Flask
ENV FLASK_APP=server.py
RUN pip install --no-cache-dir -r /app/requirements.txt
# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
#CMD ["flask", "run", "--host=0.0.0.0"]
# Start the Apache HTTP Server and run the app.py file using Python
CMD ["python3", "/app/Server.py"]
