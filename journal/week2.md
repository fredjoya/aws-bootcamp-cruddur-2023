# Week 2 — Distributed Tracing

The AWS Cloud Project Bootcamp included a Week 2 session focused on observability, specifically using distributed tracing. Here's what was covered:

### Observability and Distributed Tracing

This week, the focus was on **observability**, which is gaining insights into a running system, especially complex cloud-based software. Normal software can become very complicated over time, and it can become difficult to understand what is happening inside of it at any given time. The key is to instruct the software to tell what's going on.

**Distributed tracing** is a core component of modern observability. Rather than just relying on separate log lines, distributed tracing aims to create a story of what happens with a request as it moves through different services.

### Implementing Honeycomb

Honeycomb was used as the observability tool in this session because it is easier to use than Amazon X-Ray. Here are the steps taken to implement it:

*   **Honeycomb Account:** The first step was to set up a Honeycomb account. A specific option for "Boot Camp or student" was added to the sign-up form because of the boot camp.
*   **Environment Setup:** An environment named "boot camp" was created within Honeycomb to segment the data.
*   **API Key:** The Honeycomb API key for the boot camp environment was obtained.
*   **Environment Variables:** The following environment variables were set in the Gitpod environment:
    *   `Honeycomb_API_Key`: The API key from Honeycomb.
    *    It was determined that the *otel service name* should be hard coded in the Docker Compose rather than system wide
*   **Install Packages**: The following packages were installed:
    *  `opentelemetry-api`
    * `opentelemetry-sdk`
    * `opentelemetry-exporter-otlp`
    * `opentelemetry-instrumentation-flask`
    *  `opentelemetry-instrumentation-requests`
*   **app.py Modifications:** Code was added to `app.py` to initialize tracing and set up an exporter to send data to Honeycomb. This included:
    *   Import statements.
    *   Initializing the tracer.
    *   Setting up automatic instrumentation with Flask.
*   **Docker Compose:** The `docker-compose.yaml` file was configured to pass the necessary environment variables to the backend container.
*   **Testing:** After setting up the key and running the application, it was confirmed that traces were being sent to the test environment.

### Understanding Traces and Spans

*   **Traces:** A trace represents the entire story of a request.
*   **Spans:** A span represents a single unit of work within a trace, with a start time and duration. Spans can be nested in a tree structure, showing what happened as part of something else.

### Custom Instrumentation

To add more valuable information to the traces, custom instrumentation was added to the `home_activities.py` service:

*   A tracer was acquired and named "home activities".
*   A span was created around the `run` function, named "run home activity".
*   Attributes were added to the span, including the current time (using ISO format) and the length of the results.

### Queries

Honeycomb's query interface was used to visualize and analyze the trace data. A heat map of duration was created to see the distribution of request times, along with the 90th percentile (P90).

### Possible Future Work:

*   Instrumenting Honeycomb for the front-end application to observe network latency between the front end and back end.
*   Adding custom instrumentation to Honeycomb to add more attributes with context.
*   Running custom queries and saving them for later use.

# Topics -- Observability vs Monitoring Explained in AWS


*   **Observability vs. Monitoring** I learned what distinguishes between observability and monitoring in the context of AWS, noting how observability improves upon traditional logging methods.
*   **Traditional Application Logging** An understanding of traditional application logging, its value, and its limitations is important. Traditional logging can be time-consuming because security operation teams spend time analyzing logs daily.
*   **Cloud Logging** Cloud logging differs from data centre logging, particularly in infrastructure and application logs, due to the various compute models (IaaS, PaaS, SaaS).
*   **Why Logging Can Be Problematic** Logging can be time-consuming and may lead to alert fatigue because of the large amounts of data involved and the need to correlate logs with application context.
*   **Observability as a Solution** Observability is presented as a way to decrease alert fatigue and provide cost-effective solutions to logging problems. It involves looking at the holistic picture, checking application health, and facilitating collaboration between teams.
*   **Observability Definition** Observability provides visibility into every process of an application. It enables the breaking down of an application into multiple processes, tracing data flow, and identifying relevant metrics.
*   **Observability Metrics (Logs, Traces, Metrics)** Observability includes logs, metrics, and traces.
    *   Logs are produced by every application.
    *   Metrics enhance logs and can be used to identify issues.
    *   Traces pinpoint the root cause of a problem.
*   **The Role of Security** Security is a priority, but improving tracing requires more digging to integrate security services with CloudWatch.
*   **Instrumentation** Instrumentation is needed to create logs, metrics, and traces, often using CloudWatch Agent, X-Ray Agent, or AWS Distro for OpenTelemetry.
*   **Practical Implementation with CloudWatch and CloudTrail** Integration of CloudTrail with CloudWatch allows for the creation of metrics and alarms, which helps in identifying and responding to security incidents.
*   **Threat Modeling** Threat modelling exercises help identify potential attack vectors, which informs the creation of relevant metrics and dashboards.
*   **Central Observability Platforms** Centralised platforms like AWS Security Hub, SIEM solutions, or ELK stacks can be used to manage and visualise observability metrics.
*   **Event-Driven Architecture** An event-driven architecture uses events to identify and react to occurrences, such as an S3 bucket being open to the internet, which provides an alternative to traditional logging.
*   **AWS Services for Threat Intelligence** Services like CloudTrail, GuardDuty, and Inspector provide threat intelligence information that can be integrated using EventBridge.


# Instrument XRay
This week we focused on implementing AWS X-Ray for tracing and debugging applications. Here's a breakdown of the steps:

*   **Initial Setup:**
    *   Create a new branch in the repository for X-Ray implementation.
    *   Open the project in Gitpod.
    *   Install the necessary dependencies, including the AWS X-Ray SDK.

*   **X-Ray Daemon:**
    *   Understanding the necessity of running an X-Ray daemon alongside the application to collect, batch, and send data to the X-Ray API.
    *   Add the X-Ray daemon to the Docker Compose file using the `amazon/aws-xray-daemon` image.
    *   Configure environment variables for the daemon, including the region.

*   **AWS SDK and Instrumentation**
    *   Install the AWS X-Ray SDK for Python.
    *   Add the SDK to the backend Flask application's requirements.
    *   Utilise middleware to capture information from incoming requests for tracing.
    *   Import necessary modules from the `aws_xray_sdk`.

*   **Configuration and Code Changes:**
    *   Implement the X-Ray recorder and Flask middleware in the application code to capture data.
    *   Set the AWS X-Ray URL, which might involve dynamic naming based on the environment.
    *   Create an `x-ray.json` file for setting up sampling rules.

*   **Sampling and Groups:**
    *   Create an X-Ray group to group traces, which aids in filtering and analysis.
    *   Configure sampling rules to control the amount of data collected, balancing cost and detail.

*   **Docker Compose Configuration:**
    *   Add the X-Ray daemon service to the `docker-compose.yml` file.
    *   Set environment variables for the X-Ray daemon, including the AWS region.

*   **Running the Application:**
    *   Use `docker compose up` to start the application with the X-Ray daemon.
    *   Monitor logs to ensure data is being sent to X-Ray.

*   **Verification and Troubleshooting:**
    *   Check the X-Ray console in the AWS Management Console to view traces and service maps.
    *   Address any errors related to authentication or configuration.
    *   Adjust the `docker-compose.yml` file and application code to resolve issues.

*   **Enhancements (Stretch Goals):**
    *   Explore adding sub-segments for more granular tracing.
    *   Implement custom segments and sub-segments in the code to capture specific data points.
    *   Experiment with metadata and annotations to add additional context to traces.


