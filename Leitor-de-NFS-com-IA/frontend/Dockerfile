# Estágio 1: Build (Node)
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Serve (Nginx)
FROM nginx:1.25-alpine
WORKDIR /usr/share/nginx/html

# Remove o index.html padrão
RUN rm -f index.html

# Copia os arquivos estáticos do estágio de build
COPY --from=build /app/build .

# Copia a configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]