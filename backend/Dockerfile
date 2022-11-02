# Create a dockerfile to run fastapi_server.py which requires files from the lib directory, requirements.txt and python 3.10
# The api is exposed on port 8000

FROM python:3.10
COPY lib /lib
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
COPY fastapi_server.py /fastapi_server.py
# CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python3", "fastapi_server.py"]


# Running the Dockerfile from a docker-compose file in the parent directory (this file is /backend/Dockerfile)
# version: "3.9"

# services:
#   backend:
#     build: .
#     ports:
#       - "8000:8000"
#     volumes:
#       - .:/backend
#     # command: uvicorn fastapi_server:app --reload --host 0.0.0.0 --port 8000
#     command: python3 fastapi_server.py