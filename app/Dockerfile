FROM python:3.10

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install --upgrade pip \
     && pip install setuptools \
     && pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD alembic upgrade head && uvicorn --host=0.0.0.0 main:app --reload