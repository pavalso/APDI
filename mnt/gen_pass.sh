export REGISTRY_USER=admin
export REGISTRY_PASS=registryPass
export DESTINATION_FOLDER=./registry-creds

mkdir -p ${DESTINATION_FOLDER}
echo ${REGISTRY_USER} >> ${DESTINATION_FOLDER}/registry-user.txt
echo ${REGISTRY_PASS} >> ${DESTINATION_FOLDER}/registry-pass.txt

docker run --entrypoint htpasswd registry:2.7.0 \
    -Bbn ${REGISTRY_USER} ${REGISTRY_PASS} \
    > ${DESTINATION_FOLDER}/htpasswd

unset REGISTRY_USER REGISTRY_PASS DESTINATION_FOLDER