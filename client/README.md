# Client Setup Instructions

This README provides instructions for setting up the client application. Follow these steps to ensure everything works smoothly:

## Pre-requisites
- Python installed on your system
- Tkinter installed (required for GUI functionality)

### Installing Tkinter on Fedora or RPM-based Linux distributions
```bash
sudo dnf install python3-tkinter
```

## Installation Steps

1. Install the required Python dependencies by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure that the server application is running and accessible. The server's IP address and port number must be correctly configured in the client code.

## Configuration

Before running the client application, ensure that the server's IP address and port number are configured correctly. Modify the following variables in your Python code:

```python
# The server's hostname or IP address
# HOST = "192.168.114.38"
HOST = "127.0.0.1"

# The port used by the server
PORT = 65432
```

- `HOST`: Set this variable to the IP address or hostname of the server where the client will connect.
- `PORT`: Set this variable to the port number used by the server.

Ensure that `HOST` is set to the correct IP address of the server where the client will communicate. If the server is running on the same machine, you can use `"127.0.0.1"` for the localhost.

After configuring these variables, your client application should be ready to run and communicate with the server.
