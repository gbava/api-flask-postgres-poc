#!/bin/bash


echo "Creating the volume..."

kubectl apply -f ./k8s/pv.yml
kubectl apply -f ./k8s/pvc.yml

echo "Creating the configmap.."

kubectl apply -f ./k8s/configmap.yml

echo "Creating the database credentials..."

kubectl apply -f ./k8s/secret.yml


echo "Creating the postgres deployment and service..."

kubectl create -f ./k8s/postgres-deployment.yml
kubectl create -f ./k8s/postgres-service.yml



echo "Creating the Flask API deployment and service..."
#
kubectl create -f ./k8s/app-deployment.yml
kubectl create -f ./k8s/app-service.yml

# Todo: Add LoadBalancer or Ingress
#echo "Adding the ingress..."
#
#minikube addons enable ingress
#kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
#kubectl apply -f ./k8s/minikube-ingress.yml
