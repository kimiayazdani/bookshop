FROM python:3.7

WORKDIR /code

ENV FLASK_APP=Filter.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 8003
COPY . .

CMD ["flask", "run"]