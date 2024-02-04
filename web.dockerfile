FROM nginx
RUN apt update && apt install -y nfs-common
COPY default /etc/nginx/conf.d/default.conf