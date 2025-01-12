# Easy CV Project

Easy CV is a platform that allows users to create and manage professional CVs. This project uses Django for the backend (API) and Vue.js for the frontend.

---

## Features
- API for managing user profiles and CV data.
- PostgreSQL for database management.
- Vue.js frontend for an interactive user interface.

---

## Requirements
- **Python**: 3.9+
- **Node.js**: Latest LTS version for Vue.js
- **PostgreSQL**: 14 or later
- **Pip**: Latest version for Python package management

---

## Setup Instructions

### **Backend Setup (Django)**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/easy-cv.git
   cd easy-cv
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Apply database migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. Run the development server:
   ```bash
   python3 manage.py runserver
   ```

The backend will be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### **Frontend Setup (Vue.js)**

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vue.js development server:
   ```bash
   npm run serve
   ```

The frontend will be accessible at: [http://localhost:8080/](http://localhost:8080/)

---

## Environment Variables
Ensure you configure your `.env` file with the necessary variables for the Django backend. See `.env.example` for reference.

---

## Database Setup
If you're using PostgreSQL, ensure the database is created and accessible:

```sql
CREATE DATABASE easy_cv_db;
CREATE ROLE ivanko WITH LOGIN PASSWORD 'i_6057858_';
ALTER DATABASE easy_cv_db OWNER TO ivanko;
```

---

## File Structure
```
easy-cv/
├── backend/               # Django backend
│   ├── api/               # API application
│   ├── easy_cv_django/    # Django project settings
│   ├── manage.py          # Django command-line utility
│   └── requirements.txt   # Python dependencies
├── frontend/              # Vue.js frontend
│   ├── src/               # Vue.js source files
│   └── package.json       # Node.js dependencies
├── .env.example           # Environment variable template
└── README.md              # Project documentation
```

---
