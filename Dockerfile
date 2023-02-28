FROM python:3.10.6

ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install uvicorn==0.20.0
RUN pip install Cython numpy
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8080

CMD ["uvicorn", "--host", "0.0.0.0", "src.frameworks.fastAPI:app"]