FROM nginx
RUN apt update && apt install -y nfs-common
COPY shared /shared
COPY default /etc/nginx/conf.d/default.conf