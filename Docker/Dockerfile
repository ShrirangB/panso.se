FROM nginx:latest

WORKDIR /usr/share/nginx/html

# Remove default nginx static site
RUN rm -rf ./*

# Copy Hugo static site
COPY public/ .

# Copy nginx config
COPY Docker/cf_real-ip.conf /etc/nginx/conf.d/cf_real-ip.conf
COPY Docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
