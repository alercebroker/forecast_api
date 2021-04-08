FROM python:3.6

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install gunicorn==19.9.0
RUN while read p; do pip install --use-deprecated=legacy-resolver $p; done < requirements.txt;

COPY . /app
EXPOSE 8080


CMD ["gunicorn", "-t", "4", "--bind", "0.0.0.0", "web.app:app"]
