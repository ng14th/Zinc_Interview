# Architecture Planning
## 1. High-Level Architecture Diagram
### 1.1. Normal Architecture Diagram (This Repository)
![alt text](image.png)
### 1.2. Fully Architecture Diagram
![alt text](image-2.png)

## 2. API & Data Model Sketch
### 2.1. Import Sales
```
This api using for import sales data and save to database

URL : http://{ip}:{port}/api/sales/import-sales/
Method : POST
Body : (form-data) - file *only csv
```
```
Example :
 
curl --location 'http://{ip}:{port}/api/sales/import-sales/' \
--form 'file=@"/C:/Users/tngeen/Desktop/sales.csv"'

Response : Status 201 Created
{
    "status": 201,
    "message": "success",
    "data": {
        "imported_row": 3322
    }
}
```
### 2.2. Revenue
```
This api get total and average revenue sales in range start date and end date

URL : http://{ip}:{port}/api/metrics/revenue/
Method : GET
Param : 
 - start (date) : Month/Day/Year
 - end (date) : Month/Day/Year
```
```
Example :
 
curl --location 'http://{ip}:{port}/api/metrics/revenue/?start=3%2F1%2F2025&end=3%2F1%2F2025'

Response : Status 200 OK
{
    "status": 200,
    "message": "success",
    "data": {
        "total_revenue_sgd": 5069.044,
        "average_order_value_sg": 55.1
    }
}
```
### 2.3. Revenue Daily
```
This api group by revenue by date in range start date and end date

URL : http://{ip}:{port}/api/metrics/revenue/daily
Method : GET
Param : 
 - start (date) : Month/Day/Year
 - end (date) : Month/Day/Year
```
```
Example :
 
curl --location 'http://{ip}:{port}/api/metrics/revenue/daily?start=3%2F1%2F2025&end=3%2F1%2F2025'

Response : Status 200 OK
{
    "status": 200,
    "message": "success",
    "data": [
        {
            "date": "2025-03-01",
            "revenue_sgd": 5069.044
        },
        {
            "date": "2025-03-02",
            "revenue_sgd": 2134.436
        }
    ]
}
```
## 3. Infrastructure Choices
### 3.1 Infrastructure
- **Docker** – (containerization ) : ***Use in repository***
- **PostgreSQL** – (Main database) : ***Use in repository***
- **GitHub Actions** – CI/CD (build, test, deploy) : ***Use in repository***
- **Redis** – In-memory data store (cache)
- **Nginx** – (Web server/reverse proxy)
- **RabbitMQ** – (Message broker)
- **ELK Stack – Elasticsearch, Logstash, Kibana** (Tracing and analys log)
- **Grafana** – (Monitoring / Dashboard visualization)
- **OpenTelemetry – Observability framework** (trace, metrics, logs)
### 3.2 Framework
- **Python**
- **Django – Web framework (Python)**
- **Gunicorn – Python WSGI HTTP server**
- **Celery – Task queue (Python library)**

## 4. Scaling & Resilience Strategy
### 4.1 Scalability
To ensure the system can handle increasing loads efficiently, both horizontal and vertical scaling strategies are applied:

**Application Layer:**

Horizontal scaling is achieved by increasing the number of application instances and containers (e.g., using Docker and orchestration tools like Kubernetes or Docker Compose).

This allows better load distribution and fault isolation across multiple service replicas.

**Database Layer:**
Vertical scaling can be used to enhance database performance by upgrading hardware resources (CPU, RAM, IOPS).

Horizontal scaling is achieved through database sharding, which partitions data across multiple database nodes to distribute the load and reduce contention.

This strategy is useful for handling large-scale data and improving read/write throughput.

### 4.2 Resilience
To maintain high availability and fault tolerance, resilience techniques are implemented:

**Database Replication:**

Master-slave or multi-primary replication strategies are used to ensure redundancy and failover capability.

In case of node failure, traffic can be redirected to replica nodes without service interruption.

**Failover & Health Checks:**

Automatic health checks and failover mechanisms are configured at both the application and database levels, ensuring that the system continues operating even if one or more components fail.

## 5. CI/CD & Rollback Plan
### 5.1 CI/CD Pipeline with GitHub Action s
The CI/CD process is managed using GitHub Actions.

The pipeline is split into multiple jobs for clarity and control:

**CI Job:**

- Checks out the source code.
- Builds the Docker image.
- Runs unit and integration tests.
- Executes database migrations (if all tests pass).
- If successful, the pipeline proceeds to the deployment stage.

**CD Job:**
- Deploys the newly built image.
- Uses proper version tagging and environment-specific configuration.

### 5.1 Rollback Strategy
**Image Backup:**

- Before deployment, the previous image version is backed up to enable safe rollback.

**Deployment Flow:**

- If the build, test, and migration steps succeed, the new image is deployed.
- Upon successful deployment, the old image is removed to clean up resources.

**Failure Recovery:**

- If any step in the deployment fails, the system will automatically roll back to the previously backed-up image.

**Blue-Green Deployment :**
A Blue-Green deployment strategy is used to minimize downtime and avoid service disruption.

Traffic is routed to the new environment only after it passes health checks, ensuring zero-downtime releases.

## 6. Observability & SRE
### 6.1 Logging & Tracing
- The ELK Stack (Elasticsearch, Logstash, Kibana) is used to collect, parse, and visualize logs.
- Each request is tagged with a unique EID (Event ID) to enable end-to-end tracing across services.
- This allows for efficient debugging and correlation of logs across distributed components.

### 6.2 Metrics & Monitoring
OpenTelemetry is integrated into the services to collect telemetry data such as:
- Request rates
- Response times
- Error rates
- SQL queries executed

The collected metrics are exported and visualized through Grafana, enabling real-time monitoring and historical analysis.


### 6.3 SRE
...

## 7. Trade-Off Discussion