FROM python:2.7-alpine
MAINTAINER Lukasz Zalewski <lzalewsk@gmail.com>

# Get and install required packages.
RUN apk add --no-cache build-base linux-headers pcre-dev

# Install required dependencies (includes Flask and uWSGI)
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Create a place to deploy the application
ENV APP_DIR /PhoneBook
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

# Set default ENV
COPY . $APP_DIR/

# Expose the port where uWSGI will run
EXPOSE 5000

# If running this app behind a webserver using the uwsgi protocol (like nginx),
# then use --socket.  Otherwise run with --http to run as a full http server.
CMD ["uwsgi", "--http", ":5000", "--http-timeout","180", "--wsgi-file", "phonebook.py", "--callable", "app", "--processes",  "2", "--threads", "4", "-b", "5120"]
#CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--wsgi-file", "phonebook.py", "--callable", "app", "--processes",  "2", "--threads", "4"]
