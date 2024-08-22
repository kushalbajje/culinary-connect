# Culinary Connect - Full-Stack Project Setup

Welcome to the Culinary Connect repository, a full-stack application designed to manage and share culinary recipes. This project combines a Django backend with a frontend React.js.

## Project Structure

```
CULINARY-CONNECT/
├── backend/
│   ├── culinary_connect/
│   ├── recipes/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── auth.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── users/
├── venv/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── frontend/
    ├── node_modules/
    ├── public/
    ├── src/
    ├── .gitignore
    ├── package-lock.json
    ├── package.json
    ├── README.md
    └── LICENSE
```

## About the Project

Culinary Connect is a web application that allows users to share, discover, and manage recipes. It features a Django backend providing RESTful APIs and a modern JavaScript frontend for a responsive user interface.

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.8+
- Node.js and npm
- Git
- SQLite (included with Python) or PostgreSQL

## Setup Instructions

### Backend Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/culinary-connect.git
   cd culinary-connect/backend
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Backend Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**
   Create a `.env` file in the root directory and add:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run the Backend Server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install --force
   ```

3. **Run the Frontend Development Server**
   ```bash
   npm run start 
   ```

## Running the Application

1. Start the Django backend server
2. In a separate terminal, start the frontend development server
3. Access the application through the URL provided by your frontend server

## Development

- Backend API: http://127.0.0.1:8000/
- Frontend: Typically http://localhost:3000/ (may vary based on your frontend setup)

## Deployment

For production deployment:
1. Set `DEBUG=False` in your backend `.env` file
2. Configure a production database
3. Set up static file serving for Django
4. Build your frontend for production
5. Set up a web server like Nginx to serve your application

## License

This project is licensed under the MIT License - see the LICENSE file for details.
