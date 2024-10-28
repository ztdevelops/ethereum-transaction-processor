FROM python:3.10.15-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD main.py main.py
CMD ["python3", "main.py"]