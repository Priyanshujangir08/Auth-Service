
# Authentication Service for Multi-Tenant SaaS Platform

## Overview

This project is an authentication service designed for a multi-tenant Software as a Service (SaaS) platform. It provides user and organization management, role-based access control, and integrates with email services for notifications and user verification.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Registration**: Allows users to create accounts with email verification.
- **Organization Management**: Enables the creation and management of organizations.
- **Role-Based Access Control**: Supports multiple roles within organizations (e.g., Admin, Member).
- **Statistics APIs**: Provides insights into user distribution by organization and role.
- **Email Integration**: Sends verification and notification emails using Brevo (formerly Sendinblue).

## Technologies Used

- **Python**: Backend language for building the service.
- **FastAPI**: Web framework for building APIs quickly.
- **SQLAlchemy**: ORM for database interactions.
- **MySQL**: Database for storing user and organization data.
- **Brevo**: Email service provider for sending emails.
- **Docker**: For containerization (optional).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/authentication-service.git
   cd authentication-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MySQL database and update the database connection settings in the `.env` file:
   ```plaintext
   DATABASE_URL=mysql+pymysql://user:password@localhost/db_name
   EMAIL_API_KEY=your_brevo_api_key
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## API Endpoints

### User Management

- **POST /signup**
  - Description: Register a new user.
  - Request Body: `{"email": "user@example.com", "password": "password", "organization_name": "OrgName"}`

- **POST /login**
  - Description: Authenticate a user.
  - Request Body: `{"email": "user@example.com", "password": "password"}`

### Organization Management

- **POST /organizations**
  - Description: Create a new organization.
  - Request Body: `{"name": "OrgName", "details": "Some details about the organization"}`

### Role Management

- **GET /stats/org-role-wise-users**
  - Description: Get a count of users grouped by organization and role.

## Database Models

### User
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `hashed_password`: String
- `organization_id`: Integer (Foreign Key)

### Organization
- `id`: Integer (Primary Key)
- `name`: String (Unique)

### Member
- `user_id`: Integer (Foreign Key)
- `organization_id`: Integer (Foreign Key)
- `role_id`: Integer (Foreign Key)

### Role
- `id`: Integer (Primary Key)
- `name`: String (Unique)

## Testing

To run the tests, use the following command:
```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.