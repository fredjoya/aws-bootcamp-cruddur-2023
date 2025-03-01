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
