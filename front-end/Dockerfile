# Use an official Node.js runtime as the base image
FROM node:22-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the remaining app files
COPY . .

# Command to run the React app with Vite
CMD [ "npm", "run", "dev"]
