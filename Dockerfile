FROM python:3.6

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install gunicorn==19.9.0
RUN while read p; do pip install $p; done < requirements.txt;

COPY . /app
EXPOSE 8081


CMD ["gunicorn", "-t", "4", "--bind", "0.0.0.0", "web.app:app"]
