# Official Python 3.7.2 Alpine image
FROM python:3.7.2-alpine

# Set working directory and "pre-copy" the requirements
WORKDIR /app
COPY ./requirements /app/requirements

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements

# Make port 80 available to the world outside this container
EXPOSE 5040

# Define environment variable
ENV FLASK_APP friendship
ENV FLASK_ENV production

# Copy the rest of the files
COPY . /app

# Run app.py when the container launches
CMD flask run -h 0.0.0.0 -p 5040
