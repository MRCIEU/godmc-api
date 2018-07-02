#FROM tiangolo/uwsgi-nginx-flask:flask
FROM tiangolo/uwsgi-nginx-flask:python2.7
COPY ./app /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
