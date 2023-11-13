FROM node:lts-alpine

WORKDIR /frontend

COPY . .

RUN npm install

RUN npm run build

CMD [ "npm", "run", "serve"]
