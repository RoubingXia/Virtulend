# Use the official Apache HTTP Server base image
FROM httpd:latest

# Copy custom configuration files (if any)
#COPY ./httpd.conf /usr/local/apache2/conf/httpd.conf

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start the Apache HTTP Server
CMD ["httpd-foreground"]
