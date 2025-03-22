FROM node:16
WORKDIR /app
COPY package.json package.json
RUN npm install
COPY . .
CMD ["node", "gateway.js"]