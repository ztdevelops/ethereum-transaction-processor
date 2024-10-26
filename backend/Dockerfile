FROM python:3.10.15-slim
RUN apt-get update && apt-get install -y curl # installed for healthcheck purposes
WORKDIR /app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD src/ src/
CMD ["fastapi", "run", "src/app/main.py"]