# Tagathon

Tagathon is a software for marking beats in songs. It consists of three main components: the server, the database, and the client. This README provides instructions for setting up and running each component.

## Components

The repository contains the following directories:

1. `server`: Contains the server application.
2. `database`: Contains scripts and configurations for the database.
3. `client`: Contains the client application.

## Setup and Execution

### Server

The server component handles communication between clients and the database. Follow these steps to set up and run the server:

1. Navigate to the `server` directory.
2. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the server's IP address and port number in the code if necessary.
4. Start the server by running:
   ```bash
   python server.py
   ```

### Database

The database component stores the necessary data for the application. Follow these steps to set up and initialize the database:

1. Navigate to the `database` directory.
2. Initialize the database using the provided SQL script (`init_db.sql`). You may need to adjust the script based on your database management system (DBMS).
3. Optionally, populate the database with initial data using the provided SQL script (`dummy_data.sql`).

### Client

The client component provides a user interface for interacting with the server. Follow these steps to set up and run the client application:

1. Ensure that Python and Tkinter are installed on your system. Use the following command to install Tkinter on Fedora or RPM-based Linux distributions:
   ```bash
   sudo dnf install python3-tkinter
   ```
2. Navigate to the `client` directory.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the server's IP address and port number in the code if necessary.
5. Start the client application by running:
   ```bash
   python client.py
   ```

## Execution Order

1. Start the database to ensure that it is accessible by the server.
2. Start the server application to handle incoming client requests.
3. Finally, run the client application to interact with the server.

## Deployment

Tagathon can be deployed in a local or distributed environment. It is designed to function seamlessly in either environment. While the maximum number of users it can support simultaneously has not been tested, it has been observed to function perfectly with up to 10 users concurrently.
