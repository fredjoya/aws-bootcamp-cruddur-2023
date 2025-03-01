# Week 4 — Postgres and RDS

This journal entry summarizes the activities undertaken during week four of the AWS Cloud Project Bootcamp, focusing on relational databases and bash scripting.

*   **Setting up an RDS instance** An RDS (Relational Database Service) instance was provisioned using the AWS CLI (Command Line Interface), which was considered easier than using the AWS console (the website). The process involved using a command to set up a PostgreSQL database.
*   **Configuring the RDS Instance** Although the CLI was used for provisioning, the options available in the RDS console were reviewed, including:
    *   Choosing between standard and easy create modes.
    *   Selecting PostgreSQL as the database engine.
    *   Ensuring the free tier is selected to reduce costs.
    *   Setting up public accessibility.
    *   Configuring security groups and considering port numbers for enhanced security.
    *   Configuring database authentication methods, such as password authentication.
    *   Managing backups and encryption.
*   **Stopping the RDS Instance** After creation, the RDS instance was temporarily stopped to avoid incurring costs, with a reminder that it would restart automatically after seven days.
*   **Setting up PostgreSQL Locally**
    *   Ensuring that PostgreSQL is set up in the Docker Compose file.
    *   Starting the Docker Compose file.
    *   Connecting to the local PostgreSQL instance using the `psql` command-line client.
    *   Creating a database named "crudder".
*   **Creating a schema.sql file** A `schema.sql` file was created to define the database schema, including setting up tables and extensions. The file included commands to create the `users` and `activities` tables, with specific columns and data types.
*   **Creating Bash Scripts** Multiple bash scripts were created to automate database tasks:
    *   `db_create` to create the database.
    *   `db_drop` to drop the database.
    *   `db_schema_load` to load the schema.
*   **Setting File Permissions** Permissions were set on the bash scripts to make them executable.
*   **Modifying the `db_drop` script** The `db_drop` script was modified to remove the database name from the connection URL to allow the script to drop the currently open database. This involved using `sed` (stream editor) to manipulate the connection string.
*   **Creating a `db_connect` script** A `db_connect` script was created to simplify connecting to the PostgreSQL database.
*   **Creating a `db_seed` script** A `db_seed` script was created to automate the process of loading seed data into the database. A seed.sql file was also created.
*   **Implementing Conditional Logic** Implemented conditional logic in the schema load script to switch between local and production databases.
*   **Adding Colour Coding to Scripts** Colour coding was added to the scripts to improve readability and distinguish output.

# SQL RDS
In this part of the boot camp, the focus was on setting up a **PostgreSQL database**, connecting to it, and performing basic queries. Additionally, work was done to prepare the environment for further development, including setting up connection pooling and writing scripts for database management.

Here's a breakdown of the key steps:

*   **Database Connection and Exploration**: Connected to the database using the `db_connect` script. Explored database tables using `\dt` in `psql`. Used `SELECT * FROM activities` to view table data. Expanded record display with `\x` for better readability.

```bash
# Connecting to the database
./bin/db_connect
# Viewing tables
\dt
# Selecting all records from the activities table
SELECT all from activities;
```

*   **Connection Pooling Setup**: Installed `psycopg` version 3, a PostgreSQL adapter for Python, to enable connection pooling.

```python
# Snippet from requirements.txt
psycopg[binary]
psycopg_pool
```

Created `db.py` inside the `lib` directory to establish a connection pool.

```python
# Snippet from lib/db.py
import os
from psycopg_pool import ConnectionPool

```

Modified `docker-compose.yaml` to pass the connection URL as an environment variable.

```yaml
# Snippet from docker-compose.yaml
environment:
    CONNECTION_URL: ${CONNECTION_URL}
```

*   **Writing Raw SQL Queries**: Implemented raw SQL queries to fetch data from the database. Utilised PostgreSQL's JSON functions to directly return JSON from the database.

```python
# Example query in home_activities.py
sql = """
    SELECT row_to_json(activities.*) FROM activities
    """
with pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute(sql)
        json = cur.fetchone()
print(json)
```

*   **Database Management Scripts**: Created a `db_setup` script to automate database tasks like dropping, creating, loading the schema and seeding the database.

```bash
# Snippet from bin/db_setup
#!/bin/bash
set -e
source ./bin/db_path
./bin/db_drop
./bin/db_create
./bin/schema_load
./bin/db_seed
```

Implemented a `db_sessions` script to view active database connections and terminate idle connections.

```sql
# Example SQL command to show active connections
SELECT pid, datname, usename, client_addr, state, query FROM pg_stat_activity WHERE datname = current_database();
```

Addressed dropping the database with active connections by identifying and terminating these connections.

*   **Automating Security Group Updates in Gitpod**: Created a script (`RDS_update_SG_rule`) to automatically update the security group rule with the Gitpod IP address.

```bash
# Snippet from bin/RDS_update_SG_rule
#!/bin/bash
export GITPOD_IP=$(curl -s https://api.ipify.org)
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 5432 --cidr ${GITPOD_IP}/32 --group-name gitpod
```

Configured `gitpod.yml` to run the script on every workspace start.

```yaml
# Snippet from .gitpod.yml
tasks:
  - name: PostgreSQL
    init: source ./bin/RDS_update_SG_rule
```

These steps detail setting up a database, connecting to it, writing queries, and automating database management.

