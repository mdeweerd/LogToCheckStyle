# Container running the action
FROM python:3.11-slim-bookworm

RUN pip install regex
# Copy entry point
COPY entrypoint.sh /entrypoint.sh
COPY logToCs.py    /logToCs.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
