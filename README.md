# Microsprings ERP - Microservices Architecture

Converting monolithic Django ERP to microservices as a learning project.

## Architecture

- *8 Microservices* - Independent Django projects
- *Separate Databases* - Each service owns its data
- *API Gateway* - Single entry point
- *Docker* - Containerized deployment

## Services

1. Auth Service (Port 8001) - Authentication & authorization
2. Inventory Service (Port 8002) - Stock management
3. Manufacturing Service (Port 8003) - Production orders
4. Process Service (Port 8004) - Process templates
5. Quality Service (Port 8005) - QC & traceability
6. FG Store Service (Port 8006) - Finished goods
7. Third-Party Service (Port 8007) - Vendors & customers
8. Notification Service (Port 8008) - Alerts & notifications

## Tech Stack

- Django 5.2.6 + DRF
- MySQL 8.0
- Docker + Docker Compose
- RabbitMQ
- JWT Authentication

## Status

🚧 Phase 1: Foundation - In Progress