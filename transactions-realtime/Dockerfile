FROM python:3.10.15-slim
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD src/ src/
ADD src/service/contract-abi.json .
CMD ["python3", "src/main.py"]