#!/bin/bash
docker build -t my-expense-app ./app
echo "Preparing application..."
docker tag my-expense-app kirkiruch/my-expense-app