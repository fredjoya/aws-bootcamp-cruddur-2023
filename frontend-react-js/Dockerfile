FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR  /frontend-react-js
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]