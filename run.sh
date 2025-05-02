#!/bin/bash
if [ -f "./app/prepare-app.sh" ]; then
    ./app/prepare-app.sh || { echo "Prepare script failed"; exit 1; }
else
    echo "prepare-app.sh not found, skipping..."
fi
docker-compose up --build || { echo "Docker compose failed"; exit 1; }