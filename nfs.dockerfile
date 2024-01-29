
FROM ubuntu:latest

# Install NFS server
RUN apt-get update &&     apt-get install -y nfs-kernel-server

# Create a directory to share
RUN mkdir -p /nfs/share

# Update the NFS export list
RUN echo "/nfs/share *(rw,sync,no_root_squash,no_subtree_check)" > /etc/exports

# Expose the NFS port
EXPOSE 2049

# Start the NFS server
COPY nfs-startup.sh .
RUN chmod +x nfs-startup.sh

CMD ["/bin/bash","-c","./nfs-startup.sh"]