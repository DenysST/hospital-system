
# Hospital Management System

This project is a backend system for managing hospital operations, designed to streamline the registration of patients, assignment of doctors, and management of hospital resources such as departments, wards, and notifications.

---

## Features
- **Patient Management**:
  - Register patients with their medical problems.
  - Assign patients to appropriate departments and doctors based on their problems using an AI integration (Gemini).
  - Manage patient hospitalization status.
  
- **Department and Ward Management**:
  - Add, update, and view hospital departments.
  - Manage wards and their occupancy levels.

- **Doctor Management**:
  - Add and manage doctor profiles with department association and email contact for notifications.

- **Notifications**:
  - Notify doctors via email when:
    - A patient is assigned to them.
    - A patient's hospitalization is completed.

- **AI Integration**:
  - Use Gemini AI to recommend appropriate departments for patients based on their medical problems.
  - Dynamically provide AI with a problem description to get actionable JSON responses.

---

## Technologies Used
- **Backend Framework**: Flask
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Dependency Injection**: Dependency Injector
- **Email Notifications**: Flask-Mail
- **AI Integration**: Gemini AI
- **Testing**: Pytest
- **Containerization**: Docker

---

## Project Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd hospital-management-system
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and populate it with the required variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/hospital_db
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Initialize the Database
Run database migrations to create the required tables:
```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Start the Application
```bash
flask run
```

The application will be accessible at `http://127.0.0.1:5000`.

---

## API Endpoints

### Department Management
- **Create Department**: `POST /departments`
- **Get All Departments**: `GET /departments`
- **Update Department**: `PUT /departments/<int:department_id>`
- **Get Department by ID**: `GET /departments/<int:department_id>`

### Patient Management
- **Register Patient**: `POST /patients`
- **Get Patient by ID**: `GET /patients/<int:patient_id>`

### Ward Management
- **Get Ward Occupancy**: `GET /wards/occupancy`

---

## AI Integration

### Setup
- Gemini AI is configured during app initialization with the following prompt:
  ```plaintext
  You are an intelligent system designed to assign patients to appropriate hospital departments based on their medical problems. Respond in strict JSON format.
  ```

### Dynamic Problem Assignment
- When registering a patient, the problem is sent to Gemini, and the AI returns a department recommendation and hospitalization term.

---

## Logging
- Configured using Python's `logging` module.
- Logs are printed to the console and stored in `logs/app.log`.

---

## Testing
- **Run Tests**:
  ```bash
  pytest
  ```
- Includes unit tests for services, repositories, and views.

---

## Containerization
### Build and Run with Docker
1. **Build Docker Image**:
   ```bash
   docker build -t hospital-management-system .
   ```
2. **Run the Container**:
   ```bash
   docker run -d -p 5000:5000 hospital-management-system
   ```

---

## Future Enhancements
1. Add authentication and authorization.
2. Integrate real-time WebSocket notifications for doctors.
3. Expand AI logic for assigning wards and doctors based on historical data.

---

## Contributors
- **Project Lead**: Denys Stefanko
- **AI Integration**: Gemini AI
- **Backend Development**: Flask