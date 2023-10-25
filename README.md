# ICMP-ping

## Project Overview
This project is a simple web application with Python Flask that provides endpoints for health checks and ping functionality. It can be used to check the health of the application and to send ping requests to specified IP addresses.

## Project Structure
The project contains three main routes:

1. Health Check
Route: /health
Method: GET

2. API Ping
Route: /api/ping
Method: GET
Description: This route allows you to send ICMP ping requests to a specified IP address. It accepts the following query parameters:
IP (required): The IP address to ping.
count (optional, default: 1): The number of ping requests to send.
timeout (optional, default: 1): The timeout for each ping request.
data (optional, default: 56): The size of the data payload in each ping request.
The route logs the parameters and sends the specified number of ping requests to the provided IP address. It then returns a JSON response with the number of sent and received pings.

3. Ping
Route: /ping
Method: GET
Description: A simple route that responds with "Pong" when accessed.
