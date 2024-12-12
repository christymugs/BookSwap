# BookSwap README

## Introduction

Welcome to the **BookSwap** project! This repository contains the setup and configuration details for integrating with the New York Times Books API, a MySQL database for storing user data, a Flask web server deployed on an AWS EC2 instance, and a recommendation engine.

Follow the steps below to set up the project.

---

## Technologies Used

- **New York Times Books API**: Provides access to book data from The New York Times.
- **MySQL**: Relational database management system used for storing user requests and other data.
- **AWS EC2**: Cloud-based service used to host the web server and other components.
- **Nginx**: Web server used to handle incoming requests and serve the Flask application.
- **Kafka**: Distributed event streaming platform used for message consumption and handling.
- **Flask**: Micro web framework for building the BookSwap web application.
- **Python**: Programming language used for backend services, API interaction, and web server logic.
- **Scikit-learn**: Python library used for machine learning (in the recommendation engine).
- **Postman**: API testing tool for making HTTP requests to interact with the server and test the API endpoints.
- **pip**: Python package installer for managing dependencies.

---

## Keys, Logins, and Connection Strings

### New York Times Books API
- **API Key**: Store your API key securely in environment variables or a `.env` file.
  - **Important**: Do not hit this API more than 5 times per minute (up to 500 times per day).

### Database (MySQL)
- **User**: `admin`
- **Password**: Store your database password securely in environment variables or a `.env` file.
- **URL**: `your AWS URL`
- **Port**: `3306`

### Web Server (EC2)
- **SSH Connection**: Connect to the EC2 instance via SSH:
  ```bash
  ssh -i aws-vm-key.pem ec2-user@your-ec2-public-ip
 - **Note**: Before connecting, ensure the correct permissions are set for the SSH key:
   ```bash
   chmod 400 aws-vm-key.pem
## Project Setup

### Installation

#### Step 1: Clone the Repository

Clone the repository to your local machine:
```bash
git clone https://github.com/christymugs/BookSwap.git
cd Bookswap
```

#### Step 2: Install Required Packages

Create a virtual environment (optional but recommended) and install the dependencies:
```bash
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

## Project Structure
```bash
BookSwap/
│
├── ec2/
│   ├── app_server.conf
│   └── nginx.conf
│
├── src/
│   ├── app_server.py
│   └── db_consumer.py
│
├── testData/
│   ├── book_metadata/
│   │   ├── books_reduced_997_nonfiction.json
│   │   ├── books_reduced.json
│   │   ├── books_reduced_1093_fiction.json
│   │   └── retrieve_bestsellers.py
│   │
│   ├── test_library_data/
│   │   └── TEST-library_subscription.csv
│   │
│   └── test_user_data/
│       └── TEST-user.csv

```

## EC2 Instance Setup
- connection via SSH:
    ``` bash
        ssh -i aws-vm-key.pem ec2-user@your-ec2-public-ip
    ```
- Get app_server.py onto EC2:
    ``` bash
    - scp -i ~/CloudComputing/bookSwap/aws-vm-key.pem ~/CloudComputing/bookSwap/src/app_server.py ec2-user@ec2-user@your-ec2-public-ip:/home/ec2-user
     ```
- Run app server:
     ``` bash
     python3 app_server.py
    ```
 - **Note**: Run in the background: bg
 
## Recommendation Engine
1. Transfer the recommendation engine:
    ```bash
    scp -i ~/CloudComputing/bookSwap/aws-vm-key.pem ~/CloudComputing/bookSwap/recommendation-engine.py ec2-user@your-ec2-public-ip:/home/ec2-user
    scp -i ~/CloudComputing/bookSwap/aws-vm-key.pem ~/CloudComputing/bookSwap/isbn_10.csv ec2-user@your-ec2-public-ip:/home/ec2-user
    ```
    ## Logic of the System

The **BookSwap** project functions as an intelligent book recommendation system integrated with the New York Times Books API and a MySQL database. The system operates in the following way:

1. **User Interaction**: Users interact with the Flask web application, where they can request books from various libraries. The system accepts input such as ISBN numbers and request types (e.g., borrowing or returning books).

2. **Database Storage**: User requests are recorded in a MySQL database for later analysis. This allows tracking of requests, the libraries involved, and specific book details. The system uses the `library_request` table to store these details, which helps keep track of each request's status.

3. **API Integration**: The system integrates with the New York Times Books API to fetch real-time book data. This data is displayed to users through the Flask web application. Users can view detailed information about books, including title, author, and description.

4. **Recommendation Engine**: Using a machine learning model (via Scikit-learn), the system can suggest books based on user preferences. The recommendation engine takes input from user requests, analyzes past preferences, and then suggests books that are likely to be of interest to the user. This model is transferred to the EC2 instance and runs as a Python script.

5. **Kafka Messaging**: The system uses Kafka for event streaming, ensuring that messages (such as user requests and book data) are efficiently handled across different components. This helps in scaling the application and managing real-time data flows between components like the Flask application, database, and recommendation engine.

6. **Nginx Reverse Proxy**: The Nginx server handles incoming requests to the EC2 instance, forwarding them to the appropriate backend services (Flask, MySQL, etc.) to ensure efficient request processing.

## Conclusion

The **BookSwap** project is a comprehensive solution for managing book requests, providing personalized recommendations, and integrating real-time data from external sources like the New York Times Books API. By utilizing technologies such as Flask, MySQL, Kafka, and a machine learning recommendation engine, this project demonstrates a solid implementation of a modern web application with robust backend services. The integration of Nginx and the deployment on AWS EC2 ensures that the application can scale efficiently to handle multiple users and large volumes of data. The BookSwap system is an ideal starting point for anyone looking to build a book recommendation platform with real-time data processing capabilities.# BookSwap
