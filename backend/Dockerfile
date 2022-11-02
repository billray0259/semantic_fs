# Run server.py
# Requires backend/server.py
# Requires backend/lib/...
# Requires requirements.txt
# Hosts flask app on port 8000

# install special pytorch with pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install flask

RUN python -c 'from sentence_transformers import SentenceTransformer; model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")'

COPY . .
EXPOSE 8000
CMD ["python", "server.py"]