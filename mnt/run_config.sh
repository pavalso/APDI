#!/bin/bash

kubectl create namespace appdist

kubectl apply -f data

echo "All configurations have been applied."