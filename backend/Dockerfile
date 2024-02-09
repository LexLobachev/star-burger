FROM python:3.10.12

WORKDIR /star-burger

COPY ./backend/requirements.txt ./

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./backend/ .
EXPOSE 8080
