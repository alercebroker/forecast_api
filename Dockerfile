FROM python:3.10

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install gunicorn==19.9.0
RUN pip install Cython numpy
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8080


CMD ["gunicorn", "-t", "4", "--bind", "0.0.0.0", "web.app:app"]
