
# FROM airbyte/python-connector-base:1.1.0

# COPY . ./airbyte/integration_code
# RUN pip install ./airbyte/integration_code

FROM python:3.9-slim

# Bash is installed for more convenient debugging.
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

WORKDIR /airbyte/integration_code
COPY source_waids_oscarpro ./source_waids_oscarpro
COPY main.py ./
COPY setup.py ./
RUN pip install .

ENV AIRBYTE_ENTRYPOINT "python /airbyte/integration_code/main.py"
ENTRYPOINT ["python", "/airbyte/integration_code/main.py"]

LABEL io.airbyte.version=0.1.4
LABEL io.airbyte.name=orx/source-waids-oscarpro
