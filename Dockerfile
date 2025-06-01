FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install rich rich-argparse requests

CMD ["python", "optool.py", "--weighted", "1304000H0AAAAAA"]