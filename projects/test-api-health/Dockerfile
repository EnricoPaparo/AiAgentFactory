FROM node:20-lts-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (production only)
RUN npm ci --production

# Copy source code
COPY src ./src

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "src/index.js"]
