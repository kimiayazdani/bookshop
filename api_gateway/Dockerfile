FROM python:3.7

WORKDIR /code

ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 8000
COPY . .

CMD ["flask", "run"]