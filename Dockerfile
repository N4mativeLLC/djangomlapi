FROM python
ENV HTTP_PROXY http://proxy.nas.medcity.net:80
ENV HTTPS_PROXY http://proxy.nas.medcity.net:80
ENV MQ_HOST_NAME myrabbitmq
ENV MQ_QUEUE_NAME predict_logs
WORKDIR /app
COPY . ./
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3", "app.py", "runserver", "0.0.0.0:8080"]