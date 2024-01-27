# Kubernetes configuration files

# NFS PersistentVolume
nfs_pv_yaml = """
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
  namespace: appdist
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /path/to/nfs/share
    server: nfs-server-ip
"""

# PersistentVolumeClaim for each microservice
nfs_pvc_yaml_template = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {service_name}-pvc
  namespace: appdist  
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: ""
"""

# Deployments
deployment_yaml_template = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: appdist 
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
    spec:
      containers:
      - name: {service_name}
        image: {image}
        ports:
        - containerPort: {port}
        volumeMounts:
        - name: nfs-storage
          mountPath: /path/inside/container
      volumes:
      - name: nfs-storage
        persistentVolumeClaim:
          claimName: {service_name}-pvc
"""

# Services
service_yaml_template = """
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: appdist
spec:
  selector:
    app: {service_name}
  ports:
    - protocol: TCP
      port: {port}
      targetPort: {port}
"""

# NGINX
nginx_service_yaml = """
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
  namespace: appdist
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
"""

# Docker registry
docker_registry_yaml = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: docker-registry-pvc
  namespace: appdist
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 6Gi
  storageClassName: ""
"""

# Store all configuration files
config_files = {
    'nfs_pv.yaml': nfs_pv_yaml,
    'auth_pvc.yaml': nfs_pvc_yaml_template.format(service_name='auth'),
    'blob_pvc.yaml': nfs_pvc_yaml_template.format(service_name='blob'),
    'auth_deployment.yaml': deployment_yaml_template.format(service_name='auth', image='neculavalentin/blob_server', port=8080),
    'blob_deployment.yaml': deployment_yaml_template.format(service_name='blob', image='neculavalentin/blob_server', port=8081),
    'auth_service.yaml': service_yaml_template.format(service_name='auth', port=8080),
    'blob_service.yaml': service_yaml_template.format(service_name='blob', port=8081),
    'nginx_service.yaml': nginx_service_yaml,
    #'docker_registry.yaml': docker_registry_yaml
}

# Save configuration file in /mnt/data directory
file_paths = []
for file_name, content in config_files.items():
    path = f'mnt/data/{file_name}'
    file_paths.append(path)
    with open(path, 'w') as file:
        file.write(content)

file_paths