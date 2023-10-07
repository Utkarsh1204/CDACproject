FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6005

ENV NAME links_Scrape

CMD python app.py
