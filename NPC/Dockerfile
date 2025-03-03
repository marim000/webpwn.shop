FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mv /app/flag.txt /flag

EXPOSE 20016

CMD ["flask", "run", "--host=0.0.0.0", "--port=20016"]
