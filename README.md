# Social Networking Platform to Connect Classmates

### Made with teamwork by:
1. Alok Mukesh Sharma 
2. Zaid Zaheer Sheliya 
3. Vikash Rakesh Singh

### Under the Guidence of 
1. Asst.prof - Krunali Mehta

## Overview
This project is a secure social networking platform for students to connect via private and group chats. Built for real-time communication, it also includes an admin panel for user management.

## Features
- **Private & Group Chat**: Real-time messaging for one-on-one and group interactions.
- **Admin Control**: Add, edit, and delete user information through a dedicated admin page.
- **Secure Databases**: Messages and user data are stored securely in SQLite databases.

## Security
We prioritize security across the platform:
- **SQL Injection Protection**: Custom Python logic is used to prevent SQL injection.
- **Cross-Site Scripting (XSS)**: Inputs are sanitized using specialized Python libraries.
- **Cross-Site Request Forgery (CSRF)**: Protection is implemented using `Flask-WTF` to ensure form submissions are safe.

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript.
- **Backend**: Python with Flask framework.
- **Database**: SQLite3 for storing messages, user data, and session information.

## Python & Flask Usage
- **Flask Framework**: Flask is used to handle backend processes, routing, and database connections.
- **SQLite3**: The lightweight database stores chat messages and user information efficiently.
- **Multi-Port Setup**: Flask is configured to run across multiple ports (5000, 5001, etc.) for smooth multitasking.
- **Security Libraries**: Python libraries ensure the platform is secured against various attacks like SQL injection, XSS, and CSRF.

## Deployment
- The application can be deployed across different environments (development, production) and devices using Flask.


## Note
- The project might contain some issues in running, so please proceed and run at your own discretion.
- The flask servers are running on port 5000,5001,5002,5003,5004.
