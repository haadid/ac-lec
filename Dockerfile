# Use the base image that includes Python and necessary dependencies
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the environment file to the working directory
COPY acne /app

ENTRYPOINT [ "app.py" ]
