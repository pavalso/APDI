kubectl apply -f .\mnt\data\nfs_persistent_volume.yaml
kubectl apply -f .\mnt\data\nfs_persistent_volume_claim.yaml
kubectl apply -f .\mnt\data\auth_deployment.yaml
kubectl apply -f .\mnt\data\auth_service.yaml
kubectl apply -f .\mnt\data\blob_deployment.yaml
kubectl apply -f .\mnt\data\blob_service.yaml
kubectl apply -f .\mnt\data\nginx_deployment.yaml
kubectl apply -f .\mnt\data\nginx_service.yaml
