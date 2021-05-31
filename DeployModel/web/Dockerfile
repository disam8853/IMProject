FROM node:15.14

COPY . /app
WORKDIR /app

RUN npm install
EXPOSE 3000

ENTRYPOINT ["npm", "start"]