FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache -r requirements.txt --timeout=1000
EXPOSE 8000
CMD ["uvicorn","serverApp:serverApp","--host","0.0.0.0","--port","9000"]