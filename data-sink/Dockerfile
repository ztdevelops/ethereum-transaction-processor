FROM python:3.10.15-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD src/ src/
CMD ["python3", "src/main.py"]