# GeoTech Data Intelligence System

## Overview

This repository contains the design and implementation of the GeoTech Data Intelligence System. The goal of this assignment is to create a system that efficiently collects, processes, stores, and analyzes geospatial data to provide actionable insights for business decision-making. The project leverages various GCP services and technologies to build a scalable, secure, and efficient data intelligence platform.

## Table of Contents

- [System Design](#system-design)
  - [Requirements](#requirements)
- [Design Document](#design-document)
- [Technology Stack](#technology-stack)
- [Implementation](#implementation)
  - [ETL/ELT Pipelines](#etel-el pipelines)
  - [API Development](#api-development)
- [Evaluation Criteria](#evaluation-criteria)
- [Bonus Tasks](#bonus-tasks)
- [How to Run the Project](#how-to-run-the-project)
- [Submission and Contributors](#submission-and-contributors)

---

## System Design

### Requirements

1. **Data Sources:**
   The system ingests data from various sources:
   - Sensor data (e.g., satellite imagery)
   - Databases
   - APIs
   - Files (e.g., GeoJSON)

2. **Data Processing:**
   A robust ETL/ELT pipeline to handle various data formats and perform transformations.

3. **Storage:**
   Scalable and secure storage for both raw and processed data.

4. **Data Analysis:**
   Capabilities for spatial machine learning analysis, OCR, detection, segmentation, visualization, and reporting. Includes data quality profiling engines and a data catalog for business interaction.

5. **Integration:**
   Integration with business applications and workflows within GCP.

6. **Scalability & Monitoring:**
   System scalability to handle increasing data volume, along with monitoring and alerting capabilities for system health and performance.

7. **APIs:**
   An API catalog for accessing processed data for downstream use cases.

---

## Design Document

The full design document includes:

- **System Overview:**  
  The architecture includes components such as data sources, processing pipelines (ETL/ELT), data storage, analysis modules, and API services.

- **Data Flow:**  
  Data flows from sources like GeoJSON files and databases into the ETL/ELT pipeline, where it is processed, stored in GCP services (like BigQuery/Cloud Storage), and made available for analysis and API consumption. Real time data comimg from api's can also be handled and ingested by streaming pipelines using Dataflow.

- **Data Modeling:**  
  Data is structured in a schema optimized for geospatial analysis, leveraging BigQuery's spatial extensions for querying.

- **Technology Choices:**  
  GCP tools used: Cloud Storage, BigQuery, Dataproc, Dataflow, DataPlex, Cloud Functions, API Gateway.

- **Security and Privacy:**  
  IAM policies, encryption, and GCP’s security best practices are implemented for data security.
  Data Catalog and DataPlex can also be used for tagging of sensitive and important data for privacy and better visuality for 
downstream.

- **Scalability and Reliability:**  
  The system is designed to scale with growing data volumes and is resilient with high availability through GCP services.

- **Deployment and Maintenance:**  
  GCP CI/CD tools and monitoring services (Stackdriver) are used for seamless deployment, logging, and alerting.
  Everything can be taken care in GCP , but we can also use Jenkins configured with Github and Spinnaker for running and deployment of docker images.

---

## Technology Stack

- **Cloud Provider:** Google Cloud Platform (GCP)
- **Data Processing:** Dataflow, Dataproc, Cloud Functions
- **Data Storage:** BigQuery, Cloud Storage
- **APIs:** Cloud Endpoints, API Gateway
- **Monitoring:** Stackdriver, Cloud Logging
- **Visualization and Data Analysis:** Looker Studio, Bigquery GeoViz, BI Tools ( Tableau, Power BI)

---

## Implementation

### ETL/ELT Pipelines

**Ingestion Sources:**  
Data is ingested from a GeoJSON file (`states.geojson`) and a secondary database/API source.

**Processing:**  
The pipeline reads, transforms, and loads data into GCP storage services (BigQuery, Cloud Storage).

**Technologies:**  
- Apache Beam (Dataflow) for transformation and processing.
- Cloud Storage for raw data storage.
- BigQuery for structured geospatial data storage and querying.

### API Development

**API Functionality:**  
A RESTful API is developed that fetches geospatial data from BigQuery, processes it, and returns it as a response.

**Deployment:**  
The API is deployed using GCP API Gateway and Cloud Functions for serverless architecture.

**Endpoints:**
- `/getGeoData`: Fetches geospatial data based on the query parameters.

---

## Bonus Tasks

1. **Integration with MLOps:**  
   Demonstration of how the system integrates with MLOps on GCP, such as using AI Platform for model training on geospatial data. MLOps Integration with GeoTech Data Intelligence System is added in this repository in Bonus Directory.

2. **Real-world Dataset:**  
   Global Landslide Data Analysis Project is Added in Bonus repository with geospatial data and result captues of Bigquery GeoViz.

---

## How to Run the Project

1. **Fork the Repository:**  
   Fork this repository to your GitHub account.

2. **Set up GCP:**  
   Create a GCP account and set up the required services (BigQuery, Cloud Storage, Cloud Functions, API Gateway).

3. **Clone the Repository:**
   ```bash
   git clone <your-forked-repo-url>
   cd geotech-data-intelligence
   
4. **Deploy the ETL/ELT Pipelines:**
Follow the instructions in the pipeline code to deploy it on GCP.

6. **Deploy the API:**
Follow the API deployment instructions in the api/README.md to deploy it using GCP services.

8. **Run the System:**
After deployment, the ETL pipeline will begin ingesting data, and the API will be available at the endpoint for querying.
