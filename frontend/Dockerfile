FROM node:17.0.0

WORKDIR /star-burger

COPY . /star-burger

RUN npm ci
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
