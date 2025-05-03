FROM node:20-alpine

WORKDIR /app

#Copie des dépendances
COPY package.json package-lock.json ./

#Installation sécurisée
RUN npm ci && npm cache clean --force

#Copie du reste du code
COPY . .

#Port exposé 
EXPOSE 5173

#Commande de démarrage
CMD ["npm", "run", "dev"]