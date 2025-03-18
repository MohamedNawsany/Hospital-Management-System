# Use an official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install mysql-connector-python

# Expose the port (if necessary)
EXPOSE 5000  

# Define the command to run your Python script
CMD ["python", "/app/OrangeFinalBgd.py"]

