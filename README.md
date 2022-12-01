
# End-to-end Data Engineering: World Cup 2022 Tweets Pipelining

<a> <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/> </a>
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
<img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/microsoft%20azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white" />
<img src="https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white"/>


This repository contains a dockerized pipeline for collecting tweets extracted from two different sources, which are Twitter scraping and dataset sampling. The pipeline is based on airflow DAGs and the tweets are stored in Azure Database for PostgreSQL. We utilize the data from the warehouse as the input for sentiment analysis predictive modelling and fine tuning.

## Group 11

- [Wahyu Cahyo Wicaksono - 19/444077/TK/49273](https://www.github.com/whycw010)
- [Aulia Nur Fajriyah - 20/456360/TK/50490](https://www.github.com/aulianurfajriyah)
- [Daffa Muhammad Romero - 20/456363/TK/50493](https://www.github.com/daffaromero)
- [Hafizha Ulinnuha Ahmad - 20/456365/TK/50495](https://www.github.com/hafizhaua)
- [Mochammad Novaldy Pratama Hakim - 20/463606/TK/51598](https://www.github.com/novaldypratama)

## Running the project

Airflow image has been extended to include Python dependencies listed in requirements.txt.

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

Edit the DAG as such:
- Insert your Twitter API credentials in dags/twitter_dag_azure_ETL.py, lines 17-20:
```
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
```

- Insert database credentials in CREDENTIALS.md in dags/csv_to_azure_dag.py, lines 33-37:
```
# Update connection string information
host = ""
dbname = ""
user = ""
password = ""
sslmode = ""
```

To access local database via pgAdmin,
- Go to https://localhost:15432
- Input the default email and password
- Add a new server. 
- Set host to 'airflow-postgres-1'
- Set username and password to 'airflow'
- You can now access the table for the scraped Tweets.

To access Azure database via pgAdmin,
- Add a new server.
- Set host, username, and password
- Use the credentials listed in CREDENTIALS.md
- You can now access the table for the scraped Tweets (DAG ID: twitter_crawl_azure).
