FROM python:3.9

WORKDIR /app

COPY requirements.txt app.py /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]