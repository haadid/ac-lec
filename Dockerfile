# Use the base image that includes Python and necessary dependencies
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

ENTRYPOINT [ "app.py" ]
