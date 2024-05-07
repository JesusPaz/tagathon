# Setting Up MySQL Server in Docker

To set up a MySQL server using Docker, follow these steps:

1. Run the MySQL Docker container:
   ```bash
   docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=your_password -p 3306:3306 -d mysql
   ```

2. Check the status of running Docker containers:
   ```bash
   docker ps
   ```

3. Use `docker inspect` to obtain the IP address of the MySQL container:
   ```bash
   docker inspect mysql-container
   ```

4. Use the following command to initialize the database using the provided SQL script (`init_db.sql`):
   ```bash
   mysql -u root -p -h <container_ip_address> < init_db.sql
   ```

5. Optionally, populate the database with initial data using the provided SQL script (`dummy_data.sql`). This step is recommended to have some sample data for testing the application:
   ```bash
   mysql -u root -p -h <container_ip_address> < dummy_data.sql
   ```

6. Note that the server uses MySQL as the database management system (DBMS), and it can be executed anywhere the server has access, such as a virtual machine (VM) in the cloud, the local machine, or any desired location. For this example, Docker is used. However, it is recommended to assign a volume to the Docker image to prevent data loss if the container is deleted.

7. After following these steps, the MySQL server should be set up and ready to use.
