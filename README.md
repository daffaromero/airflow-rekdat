# airflow-rekdat

Airflow imaage has been extended to include Python dependencies listed in requirements.txt.<br>
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
