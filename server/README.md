# Setting Up Python Server with Database Connection

This README provides instructions for setting up a Python server with a database connection. Follow these steps to ensure everything works smoothly:

## Pre-requisites
- Python installed on your system
- Database server already initialized and running

## Installation Steps

1. Install the required dependencies by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure to initialize the database server before running the Python server.

## Configuration

Before running the Python server, ensure that the database connection settings are configured correctly. The following constants in your Python code control the database connection:

```python
# Constants
HOST = "127.0.0.1"
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "beats_db")
```

- `HOST`: Set the IP address where the server will listen for incoming connections. Change this to the IP address of your machine if you want to connect from other computers within the local network.
- `PORT`: Set the port number for the server to listen on.
- `DB_HOST`: Set the IP address or hostname of the database server.
- `DB_USER`: Set the username for connecting to the database.
- `DB_PASSWORD`: Set the password for connecting to the database.
- `DB_NAME`: Set the name of the database to connect to.

Make sure to update these variables according to your specific database configuration. If you need to connect from different computers, replace the `HOST` variable with the IP address of your machine to allow connections from other machines on the local network.

After configuring these variables, your Python server should be ready to run.
