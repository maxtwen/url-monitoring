FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./rest_api .
ENV FLASK_APP=app.py
ENV PYTHONPATH=PYTHONPATH:/usr/src/app
CMD flask run --host 0.0.0.0 --port 80