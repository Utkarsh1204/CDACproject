FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME Frontend

CMD python app.py