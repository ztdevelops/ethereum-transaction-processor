FROM python:3.10.15-slim
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y curl
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD src/ src/
CMD ["fastapi", "run", "src/main.py"]