# Kubernetes configuration files

# HostPath NFS volume
nfs_volume_yaml_template = """
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-volume
  namespace: appdist
  labels:
    type: local
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "shared"
"""

nfs_volume_claim_yaml_template = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-volume-claim
  namespace: appdist
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
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
      volumes:
      - name: nfs-volume
        persistentVolumeClaim:
          claimName: nfs-volume-claim
      containers:
      - name: {service_name}
        image: {image}
        ports:
        - containerPort: {port}
        volumeMounts:
        - name: nfs-volume
          mountPath: /nfsshare
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


# Store all configuration files
config_files = {
    'auth_deployment.yaml': deployment_yaml_template.format(service_name='auth',
                                                            image='neculavalentin/auth_server:latest', port=3001),
    'blob_deployment.yaml': deployment_yaml_template.format(service_name='blob',
                                                            image='neculavalentin/blob_server:latest', port=3002),
    'nginx_deployment.yaml': deployment_yaml_template.format(service_name='webserver',
                                                              image='finnllex/nginx-web-server:latest', port=80),
    'auth_service.yaml': service_yaml_template.format(service_name='auth', port=3001),
    'blob_service.yaml': service_yaml_template.format(service_name='blob', port=3002),
    'nginx_service.yaml': service_yaml_template.format(service_name='webserver', port=80),
    'nfs_volume.yaml': nfs_volume_yaml_template,
    'nfs_volume_claim.yaml': nfs_volume_claim_yaml_template
}

# Save configuration file in /mnt/data directory
file_paths = []
for file_name, content in config_files.items():
    path = f'mnt/data/{file_name}'
    file_paths.append(path)
    with open(path, 'w') as file:
        file.write(content)

file_paths
