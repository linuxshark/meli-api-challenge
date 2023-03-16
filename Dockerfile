FROM python:3.9

WORKDIR /app

COPY requirements.txt app2.py /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app2.py"]