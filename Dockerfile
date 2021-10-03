FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r --no-cache-dir requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]