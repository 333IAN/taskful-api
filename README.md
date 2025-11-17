# Taskful API

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-092E20.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.15+-A30000.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collaborative task management API built with Django and Django Rest Framework. This backend service allows users to form "Houses" (teams), create shared task lists, manage tasks, and track progress with an automated point system.

This project is built to be a robust, scalable, and secure backend for a modern web or mobile application.


## ✨ Key Features

* **User Management:** Full user authentication, including registration, login, and password management.
* **Social Authentication:** Pre-configured for social sign-on (Google, etc.) using `rest_framework_social_oauth2`.
* **Collaborative Houses:** Users can create, join, leave, and manage "Houses." Each house is a shared workspace with a designated `manager` and `members`.
* **Task & List Management:** Full CRUD (Create, Read, Update, Delete) functionality for `Tasklists` and `Tasks` within each house.
* **Attachments:** Users can upload file attachments (e.g., images, documents) to specific tasks.
* **Automated Point System:** Houses automatically earn 10 points for each completed task, managed by Django signals for real-time updates.
* **Daily Statistics Job:** A daily background job runs to recalculate and validate all house statistics (total tasks, completed tasks, and points) to ensure 100% data integrity.
* **Cloud File Storage:** Natively configured for Google Cloud Storage to handle all user-uploaded media (like house profile pictures) in a scalable way.

## 🏗️ Data Model

The application's logic is built around these core relationships:



* **User -> Profile (One-to-One):** The default Django `User` is extended with a `Profile`.
* **Profile -> House (Many-to-One):** A `Profile` can be a `member` of one `House`.
* **House -> Profile (One-to-One):** A `House` has one `Profile` set as its `manager`.
* **House -> Tasklist (One-to-Many):** A `House` can have many `Tasklist`s (e.g., "Kitchen Chores," "Yard Work").
* **Tasklist -> Task (One-to-Many):** A `Tasklist` can have many `Task`s.
* **Task -> Attachment (One-to-Many):** A `Task` can have many `Attachment`s.
* **Profile -> Task (Many-to-One):** A `Profile` is linked as the `created_by` and `completed_by` for tasks.

## 💻 Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Django | The core web framework. |
| **API** | Django Rest Framework | For building powerful and secure REST APIs. |
| **Database** | PostgreSQL (Production) | A robust, production-grade SQL database. |
| **Async Tasks** | `django-background-tasks` | To run the daily stats calculation job. |
| **Auth** | `oauth2_provider` | For token-based authentication (Bearer tokens). |
| **Social Auth**| `rest_framework_social_oauth2`| For integrating Google, Facebook, etc. login. |
| **File Storage**| `django-storages` | For connecting to Google Cloud Storage. |
| **Server** | `gunicorn` | A production-ready WSGI server. |

---

## 📖 API Documentation

Below are the key endpoints. All requests must be authenticated by passing an `Authorization: Bearer <ACCESS_TOKEN>` header after logging in.

### Authentication

#### 1. Register a New User
* **Method:** `POST`
* **Endpoint:** `/api/accounts/users/`
* **Permission:** `AllowAny`
* **Description:** Creates a new user and their associated profile.
* **Example Body:**
    ```json
    {
        "username": "newuser",
        "name": "New User Name",
        "email": "user@example.com",
        "password": "a-strong-password-123",
        "confirm_password": "a-strong-password-123"
    }
    ```

#### 2. Obtain Access Token (Login)
* **Method:** `POST`
* **Endpoint:** `/api/auth/token/`
* **Permission:** `AllowAny`
* **Description:** Swaps a username and password for an access token.
* **Example Body:**
    ```json
    {
        "grant_type": "password",
        "username": "newuser",
        "password": "a-strong-password-123",
        "client_id": "YOUR_OAUTH_CLIENT_ID",
        "client_secret": "YOUR_OAUTH_CLIENT_SECRET"
    }
    ```

### House Management

#### 1. Create a House
* **Method:** `POST`
* **Endpoint:** `/api/house/houses/`
* **Permission:** `IsAuthenticated`
* **Description:** Creates a new house and automatically sets the creator as the `manager`.
* **Example Body:**
    ```json
    {
        "name": "The Best House",
        "description": "Our awesome collaborative space.",
        "image": "path/to/image.jpg"
    }
    ```

#### 2. Join a House
* **Method:** `POST`
* **Endpoint:** `/api/house/houses/{house_id}/join/`
* **Permission:** `IsAuthenticated`
* **Description:** A custom action to join a house. Sets the user's `profile.house` field.

### Task Management

#### 1. Create a Task
* **Method:** `POST`
* **Endpoint:** `/api/task/tasks/`
* **Permission:** `IsAuthenticated` (and must be a member of a house).
* **Description:** Creates a new task. The `task_list` provided must belong to the user's current house.
* **Example Body:**
    ```json
    {
        "name": "Wash the dishes",
        "description": "All of them. Now.",
        "task_list": "[http://api.com/api/task/tasklists/1/](http://api.com/api/task/tasklists/1/)"
    }
    ```

#### 2. Update Task Status
* **Method:** `PATCH`
* **Endpoint:** `/api/task/tasks/{task_id}/update_task_status/`
* **Permission:** `IsAuthenticated` (and must be in the task's house).
* **Description:** Custom action to mark a task as complete or incomplete. This action triggers the point-awarding signal.
* **Example Body:**
    ```json
    {
        "status": "COMPLETE"
    }
    ```
    (or `"status": "NOT_COMPLETE"`)

---

## 🛠️ Local Development Setup

### 1. Prerequisites
* Git
* Python 3.10+
* A package manager (like `pip`)

### 2. Clone & Install
```bash
# 1. Clone the repository
git clone https://github.com/333IAN/taskful-api.git
cd taskful-api

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # (On Windows, use: venv\Scripts\activate)

# 3. Install all required packages
pip install -r requirements.txt
