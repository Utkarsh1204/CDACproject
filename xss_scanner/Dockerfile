FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6011

ENV NAME XSS_Scanner

CMD python app.py
