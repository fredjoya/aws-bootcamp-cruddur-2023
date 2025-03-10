# Week 1 — App Containerization

## End-to-End Containerisation of a Multi-Tier Application with Docker and Docker Compose

This document outlines the comprehensive steps taken to containerise a multi-tier application, encompassing both the backend (Flask) and frontend (React) components, using Docker and Docker Compose. This process was undertaken as part of an intensive AWS Cloud Project Bootcamp focused on app containerisation.

## Prerequisites

Before commencing the containerisation process, the following prerequisites were ensured:

- **Active GitHub Account:** Necessary for accessing and managing the project repository.
- **Access to the Bootcamp Repository:** Providing the source code, Dockerfiles, and Docker Compose configurations.
- **GitPod Environment Setup:** Leveraging GitPod as the cloud-based development environment, pre-configured with Docker.
- **Completion of Week Zero Deliverables:** This included foundational tasks such as creating **architectural diagrams**, installing the **AWS CLI**, and establishing a **billing alarm and budget** within AWS.

## Step-by-Step Containerisation Process

The following details the sequential steps undertaken to achieve a fully containerised and orchestrated application:

### 1. Accessing Week One Instructions and Code

Initially, I navigated to the designated **`week one` branch** within the bootcamp's GitHub repository. The core instructions were contained within the **journal file** in this branch, which served as the primary guide.

### 2. Launching the Development Environment

Subsequently, I initiated the **GitPod environment** from the **`main` branch** of the repository. 

### 3. Defining Container Images with Dockerfiles

#### Backend (Flask) Dockerfile

1. Navigate to the `backend-flask` directory within GitPod's terminal:
    ```bash
    cd backend-flask
    ```
2. Create a new **`Dockerfile`**:
    ```bash
    touch Dockerfile
    ```
3. Add the following content to build the Flask backend:
    ```dockerfile
    FROM python:3.10-slim-buster
    WORKDIR /app
    COPY requirements.txt .
    RUN pip3 install -r requirements.txt
    COPY . .
    ENV FLASK_APP=app.py
    ENV FLASK_RUN_HOST=0.0.0.0
    EXPOSE 4567
    CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]
    ```

#### Frontend (React) Dockerfile

1. Navigate to the `frontend-reactjs` directory:
    ```bash
    cd ../frontend-reactjs
    ```
2. Install Node.js dependencies:
    ```bash
    npm install
    ```
3. Create a **`Dockerfile`**:
    ```bash
    touch Dockerfile
    ```
4. Add the necessary instructions to build and serve the React app (using Node.js base image and a web server).

### 4. Building Docker Images

Build the Docker image for the backend:
```bash
docker build -t backend-flask ./backend-flask
```
Verify the built images:
```bash
docker images
```

### 5. Running a Single Backend Container

Run the backend container:
```bash
docker run -p 4567:4567 -e FRONTEND_URL="*" -e BACKEND_URL="*" backend-flask
```

Unlock port 4567 in GitPod's Ports tab. Access the `/api/activities/home` endpoint to confirm the backend is operational.

### 6. Orchestrating Multi-Container Deployment with Docker Compose

1. Create a `docker-compose.yaml` in the project root:
    ```bash
    touch docker-compose.yaml
    ```
2. Define services, ports, environment variables, and dependencies:
    ```yaml
    version: '3.8'
    services:
      backend:
        build: ./backend-flask
        ports:
          - "4567:4567"
        environment:
          FLASK_APP: app.py
      frontend:
        build: ./frontend-reactjs
        ports:
          - "3000:3000"
        environment:
          REACT_APP_API_ENDPOINT: http://localhost:4567
        depends_on:
          - backend
    ```
3. Launch the containers:
    ```bash
    docker compose up
    ```
4. Unlock ports 3000 and 4567 in GitPod's Ports tab.

### 7. Verifying the Full Application Deployment

After running the above command, visit the GitPod-generated URL for port 3000. This confirms the frontend communicates with the backend, completing the full containerisation.

### 8. Development Workflow with Volume Mounting

The `volumes` configuration in `docker-compose.yaml` enables hot-reloading. Any code changes made locally reflect instantly within the running containers.

## Key Learnings and Observations

- **Dockerfiles**: Define reproducible container images.
- **Building Images**: Encapsulate app code and dependencies.
- **Running Containers**: Use `docker run` for standalone containers.
- **Docker Compose**: Orchestrate multi-container apps.
- **Environment Variables**: Configure inter-service communication.
- **Volume Mounting**: Enable live code updates.
- **File Systems**: Understand host vs. container directories.

## Potential Enhancements and Best Practices

- **Multi-Stage Builds**: Reduce final image size.
- **Health Checks**: Monitor and restart unhealthy containers.
- **Secure Config**: Use Docker secrets for env variables.
- **Container Registry**: Push images to Docker Hub or ECR.
- **Optimized Dockerfiles**: Leverage caching, use specific tags.

## Conclusion

This project solidified my understanding of Docker and Docker Compose, showcasing their role in modern application development. Containerisation boosts portability, reproducibility, and simplifies managing complex cloud-based applications.

