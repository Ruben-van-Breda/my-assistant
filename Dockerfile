# Use a newer Node.js image as a base (Node 16 or higher supports the ??= operator)
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 19006

# Command to run the application
CMD ["npm", "run", "web"]