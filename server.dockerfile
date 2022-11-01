# We're using the python 3.9 "Base Image". This just means we're starting with a computer that has python 3.9 installed already
FROM python:3.10.6

# We can run any shell commands you'd run on a real server. Here we just make a directory to put our server code in
RUN mkdir /app
WORKDIR /app

# This is Linux, so make sure the image is up to date
RUN apt update

# To get our code into the Docker image, we just need to copy it from our local computer.
# We start by copying over the requirements.txt file from the local path "./frontend_api/requirements.txt" to the working directory (/app) in the image
COPY ./requirements.txt ./
# Then we pip install all our requirements in the image
RUN pip install --no-cache-dir -r requirements.txt

# install pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113


# Finally we copy our server (e.g., your flask or FastAPI app) code over to the image
COPY ./fastapi_server.py .
COPY ./lib ./lib

ENV PYTHONPATH=/app

# The CMD keyword tells the image what command to run when it starts. Here we just call main.py, which starts serves our app.
CMD [ "python", "-u", "fastapi_server.py" ]

# One small detail to note: when you are normally testing a flask app, you run it on localhost. However, if you did that in a docker container, it would run on the localhost of the VM, and not be accessible from your host machine.
# So, you want to host your app in your container at 0.0.0.0, which will allow incoming connections