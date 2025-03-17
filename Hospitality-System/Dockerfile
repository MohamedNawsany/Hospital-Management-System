# ✅ Use an official Python base image
FROM python:3.11

# ✅ Set the working directory in the container
WORKDIR /app

# ✅ Copy the project files into the container
COPY . /app

# ✅ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Set environment variables (Modify if needed)
ENV DB_HOST=mysql
ENV DB_USER=root
ENV DB_PASSWORD=12345
ENV DB_NAME=hospitalll_db

# ✅ Run the application
CMD ["python", "hospital.py"]