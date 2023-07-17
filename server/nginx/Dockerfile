#node builder
FROM node:12.2.0-alpine as builderNode
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY front/package*.json .
RUN npm install @vue/cli@3.7.0 -g
RUN npm install
COPY front /app

RUN npm run build


FROM nginx as production-stage
RUN mkdir /app
RUN mkdir /app/rsc
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builderNode /app/dist /app
COPY --from=builderNode /app/rsc /app/rsc

COPY nginx/nginx.conf /etc/nginx/conf.d