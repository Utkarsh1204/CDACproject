FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6001

ENV NAME iplocator

CMD python app.py
