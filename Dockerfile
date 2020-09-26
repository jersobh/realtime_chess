FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
WORKDIR /src
ADD ./src /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn server:factory --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker