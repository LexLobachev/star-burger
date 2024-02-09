FROM python:3.10.12

WORKDIR /star-burger

COPY ./backend/requirements.txt /star-burger/requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /star-burger
EXPOSE 8080
