FROM nginx:latest

WORKDIR /usr/share/nginx/html

# Remove default nginx static site
RUN rm -rf ./*

# Copy Hugo static site
COPY public/ .

# Copy nginx config
COPY Docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
