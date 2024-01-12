# Use a lightweight Python base image
FROM python:3.9-slim

# Install Flask
RUN pip install Flask

# Set the working directory
WORKDIR /app

# Copy the application script
COPY app.py /app/app.py

# The container listens on port 5000 by default
EXPOSE 5000

# The application requires an environment variable APP_KEY to run
# The application is started with 'flask run' command, which can be set through CMD
CMD ["flask", "run", "--host=0.0.0.0"]
