FROM nginx:latest
ADD nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y procps

ADD start.sh /start.sh
RUN chmod +x /start.sh
ADD nginx-secure.conf /etc/nginx/nginx-secure.conf
ADD dhparams.pem /etc/ssl/private/dhparams.pem
CMD /start.sh
