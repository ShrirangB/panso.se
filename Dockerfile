FROM nginx:latest
COPY main/public /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
EXPOSE 80
VOLUME [ "/var/log/nginx" ]
CMD ["nginx", "-g", "daemon off;"]
