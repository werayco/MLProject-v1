FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache -r requirements.txt --timeout=1000
RUN RUN python -m nltk.downloader stopwords
EXPOSE 7890
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","7890"]