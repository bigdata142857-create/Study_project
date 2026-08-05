FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Health Check용 curl 설치
RUN apt-get update && apt-get install -y curl

COPY . .

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]