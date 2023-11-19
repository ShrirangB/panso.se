FROM nginx:latest
COPY main/public /usr/share/nginx/html
COPY nginx/cf_real-ip.conf /etc/nginx/conf.d/cf_real-ip.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]