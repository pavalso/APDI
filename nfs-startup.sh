mkdir /nfs/share
chmod 777 /nfs/share
/usr/sbin/rpcbind -w && /usr/sbin/exportfs -ra && /usr/sbin/rpc.mountd --foreground