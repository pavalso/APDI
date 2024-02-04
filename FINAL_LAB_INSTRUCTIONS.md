### Autores: Pablo Valverde Soriano, Raúl Moya Campillos, Raúl González Velázquez y Valentin Necula 

### Prerrequisitos
Antes de comenzar con la instalación y el uso de este proyecto, asegúrate de tener los siguientes componentes instalados:

1. **Docker:**
   -  Puedes instalar Docker siguiendo las instrucciones en la [documentación oficial de Docker](https://docs.docker.com/get-docker/).

2. **Minikube:**
   -  Para instalar Minikube, consulta la [documentación oficial de Minikube](https://minikube.sigs.k8s.io/docs/start/).

3. **Kubernetes:**
   -  Puedes instalar Kubernetes en tu sistema siguiendo las instrucciones proporcionadas en la [documentación oficial de Kubernetes](https://kubernetes.io/docs/setup/).



### Instrucciones de uso


1. **Clonar el repositorio**

2. **Iniciar minikube** 
```minikube start```

3. **Instalar la configuración del proyecto** 
```sh mnt/apply_config.sh```

Puede que instalar el nginx_ingress de error, ya que es necesario que pase unos minutos desde que iniciamos el minikube, si esto ocurre, instalar nginx_ingress con ```kubectl apply -f ./mnt/data/nginx_ingress.yaml```

4. **Introducir las rutas en etc/host** 
Para ello primero necesitamos saber la ip de nuestro minikube
```minikube ip```

Una vez que sepamos la ruta, añadimos al fichero host las rutas definidas en nuestro proyecto: 
```sudo nano etc/hosts```

Y en este fichero añadimos: 

    <minikube ip>   apiweb.com
    <minikube ip>   auth.apiweb.com
    <minikube ip>   blobs.apiweb.com

5. **Abrir la dashboard** 
```minikube dashboard```

6. **Usar la aplicación** 
Podemos comprobar que funciona accediendo por ejemplo a este [enlace](https://blobs.apiweb.com/api/v1/status)

