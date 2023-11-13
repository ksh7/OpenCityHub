## Traffic Management App Deployment

Major parts involved:

- Modifying config values
- (Optional) Creating own docker images using Dockerfile and source code at `./smartcity_apps/traffic_mgmt/web_app/Dockerfile`
- Login to OpenShift using `oc login`
- Executing each component's deployment/service configuration commands one by one.
- Creating routes for public facing components like Django app
- (Optional) Deploying serverless applications using respective commands.


**NOTE:** You can either use same common services like PostgreSQL, Redis instance or deploy seperately as per your use-case. For this demo, we're using different instances.

**Steps for App:**

1. Go to directory `./k8s_configs/traffic_mgmt_app_configs` at root.
2. Modify config key/values in file `k8s-configmap.yaml`
3. Deploy configs: `kubectl apply -f k8s-configmap.yaml`
4. Deploy Postgres DB: `kubectl apply -f k8s-postgres-deploy.yaml`
5. Create an associated service for PostgresDB: `kubectl apply -f k8s-postgres-service.yaml`
6. Deploy Redis instance: `kubectl apply -f k8s-redis-deploy.yaml`
7. Create an associated service for Redis: `kubectl apply -f k8s-redis-service.yaml`
8. Create an associated service for Celery app: `kubectl apply -f k8s-celeryapp-service.yaml`
9. Deploy 'Traffic Management' Celery app: `kubectl apply -f k8s-celeryapp-deploy.yaml`
10. Deploy 'Traffic Management' RabbitMQ Consumer app: `kubectl apply -f k8s-rabbitmq-deploy.yaml` (Note: Currently, you need to supply full AMPQS URI in configmap, as we're not deploying it on OpenShift, but using a free 3rd party service like https://cloudamqp.com)
11. Create an associated service for RabbitMQ Consumer app: `kubectl apply -f k8s-rabbitmq-service.yaml`
12. Deploy Django docker container for 'Traffic Management' App: `kubectl apply -f k8s-django-deploy.yaml` (Note: you can build and use your own docker image)
13. Run a dummy/mock data loading Job (optional): `kubectl apply -f k8s-django-dummydata-job.yaml` (Note: this runs only once)
14. Create an associated service for Django app: `kubectl apply -f k8s-django-service.yaml`
15. Use OpenShift Web Dashboard to create a route for above Django service.


Now you should be able to access the 'Traffic Management' app using Route created in step 15.

Also, if something doesn't work, look for particular container's logs in OpenShift Web Dashboard or open an issue on Github.
