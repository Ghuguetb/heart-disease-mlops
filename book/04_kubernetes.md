# Orquestación con Kubernetes

Tener la API en un contenedor de Docker ya es un buen paso, pero en un entorno real normalmente se necesita algo que administre esos contenedores, que los reinicie si fallan y que controle cómo se accede a ellos. Para eso usamos Kubernetes, y para no depender de la nube lo corrimos de forma local con Minikube.

Definimos dos archivos de configuración. El primero es `k8s/deployment.yaml`, que le dice a Kubernetes qué imagen de Docker debe correr y cuántas copias mantener activas. El segundo es `k8s/service.yaml`, que expone esa aplicación para que se pueda acceder a ella desde afuera del clúster.

```bash
minikube start --driver=docker
minikube image load heart-api:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
minikube service heart-service
```

Como trabajamos todo en local, la imagen se carga directamente en Minikube con `minikube image load`, en vez de subirla a un registro externo como Docker Hub.

Con esto, el modelo queda desplegado de una forma muy parecida a como se haría en un entorno de producción real, solo que corriendo en nuestro propio computador.
