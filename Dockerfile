# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN ls && pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Enable hot reloading with Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
