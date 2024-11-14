FROM python:3.12

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
COPY ./.venv/packages /tmp/packages
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY ./.env.local /api/.env.local
COPY ./app /api/app
COPY ./res /api/res

CMD [ "python","-m","app","-H","0.0.0.0","-M","prod" ]
