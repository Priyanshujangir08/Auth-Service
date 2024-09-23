
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

## Features

- **User Registration**: Allows users to create accounts with email verification.
- **Organization Management**: Enables the creation and management of organizations.
- **Role-Based Access Control**: Supports multiple roles within organizations (e.g., Admin, Member).
- **Statistics APIs**: Provides insights into user distribution by organization and role.
- **Email Integration**: Sends verification and notification emails.

## Technologies Used

- **Python**: Backend language for building the service.
- **FastAPI**: Web framework for building APIs quickly.
- **SQLAlchemy**: ORM for database interactions.
- **MySQL**: Database for storing user and organization data.
- **Docker**: For containerization (optional).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AUTH-SERVICE.git
   cd AUTH-SERVICE
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
   
   ....
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
  - Description: Register a new user and create an organization.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password",
      "organization_name": "OrgName"
    }
    ```
  - Response:
    ```json
    {
      "message": "User signed up successfully",
      "user_id": 1,
      "org_id": 1
    }
    ```

- **POST /signin**
  - Description: Authenticate a user.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "access_token_value",
      "refresh_token": "refresh_token_value"
    }
    ```

### Organization Management

- **POST /organizations**
  - Description: Create a new organization.
  - Request Body:
    ```json
    {
      "name": "OrgName",
      "details": "Some details about the organization"
    }
    ```
  - Response:
    ```json
    {
      "message": "Organization created successfully",
      "org_id": 1
    }
    ```

### Role Management

- **GET /stats/org-role-wise-users**
  - Description: Get a count of users grouped by organization and role.
  - Response:
    ```json
    [
      {
        "organization": "OrgName",
        "role": "Owner",
        "user_count": 10
      }
    ]
    ```

## Database Models

### User
Represents a user in the system.

| Column Name     | Type     | Description                |
|-----------------|----------|----------------------------|
| `id`            | Integer  | Primary key                |
| `email`         | String   | Unique email address       |
| `password`      | String   | Hashed password            |
| `profile`       | JSON     | Profile information        |
| `status`        | Integer  | Status of the user         |
| `settings`      | JSON     | User-specific settings     |
| `created_at`    | BigInteger | Timestamp of creation   |
| `updated_at`    | BigInteger | Timestamp of last update |

---

### Organization
Represents an organization.

| Column Name     | Type     | Description                     |
|-----------------|----------|---------------------------------|
| `id`            | Integer  | Primary key                     |
| `name`          | String   | Unique name of the organization |
| `status`        | Integer  | Organization status             |
| `personal`      | Boolean  | Indicates if personal org       |
| `settings`      | JSON     | Organization settings           |
| `created_at`    | BigInteger | Timestamp of creation        |
| `updated_at`    | BigInteger | Timestamp of last update      |

---

### Member
Links a user to an organization with a role.

| Column Name     | Type     | Description                     |
|-----------------|----------|---------------------------------|
| `id`            | Integer  | Primary key                     |
| `org_id`        | Integer  | Foreign key to Organization      |
| `user_id`       | Integer  | Foreign key to User              |
| `role_id`       | Integer  | Foreign key to Role              |
| `status`        | Integer  | Member status                   |
| `settings`      | JSON     | Member-specific settings        |
| `created_at`    | BigInteger | Timestamp of creation        |
| `updated_at`    | BigInteger | Timestamp of last update      |

---

### Role
Represents a role in an organization.

| Column Name     | Type     | Description                |
|-----------------|----------|----------------------------|
| `id`            | Integer  | Primary key                |
| `name`          | String   | Role name                  |
| `description`   | String   | Role description           |
| `org_id`        | Integer  | Foreign key to Organization |



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