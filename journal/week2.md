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
