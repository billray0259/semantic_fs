=== FILE: program.dockerfile
# Create a dockerfile to run program.py which requires lib/util.py and python 3.10
FROM python:3.10
COPY lib /lib
COPY program.py /program.py
CMD ["python", "/program.py"]

=== EOF

=== FILE docker-compose.yml
# Docker compose file to run program.py
version: "3.9"
services:
  program:
    build: .
    volumes:
      - .:/app
    command: python /app/program.py

=== EOF

=== FILE: start.sh
# sh file to run docker-compose
docker-compose up --build

=== EOF