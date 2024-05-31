# Lincoln Golf Club Website Redevelopment

## 1. Project Overview

This project develops a new website for Lincoln Golf Club, aiming to provide a modern, user-friendly interface that improves content management systems and enhances site security. The site supports responsive design across devices, ensuring good accessibility and operability.

## 2. Technical Architecture

### 2.1 Frontend

- **Technologies**: HTML5, CSS3, JavaScript, React
- **Framework**: Bootstrap for responsive design
- **Features**: User registration, login, content browsing, admin backend management

### 2.2 Backend

- **Technologies**: Python, Flask
- **Main Functions**: Handle user requests, authentication, data processing, session management

### 2.3 Database

- **Technology**: MySQL
- **Tools**: Navicat for database management
- **Data Storage**: User information, membership data, sponsor information, etc.

## 3. Installation and Configuration Guide

### Environment Preparation

- Ensure Python and Node.js are installed on the server.
- Install MySQL and create necessary databases and tables.

### Deployment Guide

- Clone the repository to the server.
- Install frontend and backend dependencies with `npm install` and `pip install -r requirements.txt`.
- Configure environment variables, including database connection strings and any third-party API keys.

### Starting the Application

- Run the backend service: `python app.py`
- Run the frontend development server: `npm start`

## 4. User Guide

### 4.1 User Registration and Login

- Visit the homepage and click the "Register/Login" button.
- Enter the required registration information or use an existing account to log in.
- Follow the instructions on the screen to complete the operation.

### 4.2 Content Management

- Administrators can add, modify, or delete website content by accessing the `/admin` path.

## 5. API Documentation

- **Get User Information**:
  - **Request Type**: GET
  - **URL**: `/api/user/<user_id>`
  - **Parameters**: None
  - **Returns**: Detailed information of the user

## 6. Troubleshooting

- **Problem**: Unable to connect to the database
  - **Solution**: Check if the database service is running and confirm the connection string is correct.



