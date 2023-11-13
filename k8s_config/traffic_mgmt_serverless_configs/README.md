## Traffic Management Serverless Apps

**Steps for Serverless Apps:**

**Note:** Traffic ManagementServerless apps docker images are readily available on Quay.io but you can build your own using Dockerfile and source code in `./smartcity_apps/traffic_mgmt/serverless_apps`

1. Install Openshift Knative on your system.
2. For each app in `./smartcity_apps/traffic_mgmt/serverless_apps` run Knative command `kn service create <name-of-serverless-function> --image <docker-image> --port <port>` command
2. For example, run `kn service create traffic-citizen-travel-planner-app --image quay.io/aenvsite/traffic_citizen_travel_planner --port 5000` command to deploy 'citizen_travel_planner' app.
3. Access using the URL printed on command line once deployment is completed.
