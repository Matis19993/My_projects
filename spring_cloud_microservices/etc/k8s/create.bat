kind load docker-image ms-publisher-k8s

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
kubectl wait --namespace metallb-system --for=condition=ready pod --selector=app=metallb --timeout=90s
kubectl apply -f .\metallb-config.yaml

kubectl apply -f .\auth.yaml
kubectl apply -f .\ms-publisher.yml

kubectl get all --all-namespaces
