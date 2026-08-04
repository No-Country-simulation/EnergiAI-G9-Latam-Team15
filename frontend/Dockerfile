# EnergiAI — frontend (Vite/React) → build estático servido con nginx.
# Colocar como frontend/Dockerfile. Construir con contexto ./frontend.
# OJO: Vite hornea VITE_API_URL en el BUILD (reemplaza import.meta.env al compilar).
# Como el navegador es quien llama al backend, VITE_API_URL debe ser una URL que el
# NAVEGADOR pueda alcanzar (local: http://localhost:8080 ; OCI: la IP/URL pública del backend).
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL=http://localhost:8080
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
