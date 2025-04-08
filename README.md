# SmartStudents - AI-Powered Study Assistant

SmartStudents is an intelligent study assistant that helps students manage their tasks, optimize study schedules, and maintain healthy study habits using AI-powered recommendations.

## Features

- **AI-Powered Schedule Optimization**
  - Smart study block recommendations based on deadlines and task priorities
  - Dynamic rescheduling based on progress and new tasks
  - Personalized study/break cycles

- **Task Management**
  - Priority-based task organization
  - Deadline tracking and reminders
  - Progress monitoring

- **Personalized Study Patterns**
  - Customizable study/break durations
  - AI-recommended optimal study times
  - Productivity pattern analysis

- **Progress Tracking**
  - Visual progress indicators
  - Productivity analytics
  - Study habit insights

## Tech Stack

### Frontend
- React
- Material-UI
- React Router
- Recharts
- Firebase (for authentication and real-time updates)

### Backend
- FastAPI
- SQLAlchemy
- Scikit-learn (for AI recommendations)
- Firebase Admin SDK

## Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- pip
- npm

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=sqlite:///./smartstudents.db
   SECRET_KEY=your_secret_key
   FIREBASE_CREDENTIALS=path_to_firebase_credentials.json
   ```

6. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 