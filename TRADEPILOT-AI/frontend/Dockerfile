# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json /app/

# Install dependencies
RUN npm install --silent

# Copy the rest of the application
COPY frontend /app/frontend

# Expose port
EXPOSE 5173

# Set working directory to frontend to run Vite
WORKDIR /app/frontend

# Run development server
CMD ["npm", "run", "dev", "--", "--host"]
