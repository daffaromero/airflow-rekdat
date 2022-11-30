# airflow-rekdat

Airflow image has been extended to include Python dependencies listed in requirements.txt.<br>

Change the image line in docker-compose.yaml to this:
```
image: ${AIRFLOW_IMAGE_NAME:-extending_airflow:latest}
```

<b>Note: The Dockerfile has been set up for Airflow version 2.4.3.</b> Change this line to suit a different version of Airflow:
```
FROM apache/airflow:2.4.3 
```

Build the image with:
```bash
$ docker build . --tag extending_airflow:latest
```

Then, to start the containers:
```bash
$ docker-compose -f docker-compose.yaml up -d
```

To access pgAdmin,
<ol>
  <li>Go to https://localhost:15432</li>
  <li>Input the default email and password</li>
  <li>Add a new server.</li> 
  <li>Set host to 'airflow-postgres-1'</li>
  <li>Set username and password to 'airflow'</li>
  <li>You can now access the table for the scraped Tweets.</li>
</ol>
