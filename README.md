# React Native Web App

A simple cross-platform application built with React Native and Expo that runs on web, iOS, and Android platforms.

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)

## Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the application:
   ```bash
   expo start -c
   ```

## Running on Different Platforms

### Web

## Docker Setup

To run the application using Docker, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t my-react-native-web-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 19006:19006 my-react-native-web-app
   ```

3. Access the application in your web browser at `http://localhost:19006`.