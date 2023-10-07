FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6009

ENV NAME SQL_Injection

CMD python app.py
