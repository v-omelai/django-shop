#!/bin/bash

# Add Docker's official GPG key:
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y

# Install the Docker packages
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Clone the repository
git clone https://github.com/v-omelai/django-shop.git /app

# Copy the environment file
cp /tmp/.env.prod /app/.env.prod

# Grant execute permissions to the entrypoint script
sudo chmod +x /app/docker/web/entrypoint.sh

# Build and start the containers
cd /app || { echo "Error: Directory does not exist. Exiting."; exit 1; }
sudo docker compose build
sudo docker compose up -d
