# Sportiva Base

[🔗 Go to Frontend Repository (React)](https://github.com/ivosokoloski/sportiva-base)

**Sportiva Base** is a specialized web platform designed for mapping and managing information about sports centers and gyms in Prilep. The project combines the robust data management capabilities of Django with the dynamic nature of React for a modern user experience.

#### 1. Frontend (React)
Navigate to the frontend directory, install the dependencies, and start the development server:
```bash
npm install
npm run dev
```

#### 🔹 Backend (Django)
1. Navigate to the backend directory.
2. Install the required dependencies (ensure your virtual environment is active).
3. Run the migrations and start the development server:
```bash
python manage.py migrate
python manage.py runserver
```


---

### 📌 Description
The application enables quick and easy orientation through the sports locations in the city. The main focus is on interactivity—users can not only locate facilities via the map but also actively participate in the community by leaving reviews and ratings regarding the quality of services.

### 🧱 Architecture
The project follows a **Decoupled Architecture** for better modularity:
* **Backend (Django 6.0.3):** Acts as a robust REST API handling application logic, security, and data structuring.
* **Frontend (React):** A modern Single Page Application (SPA) that provides instant interaction without page reloads.
* **Database (PostgreSQL):** Ensures secure and fast storage for locations, users, and feedback data.

### ⚙️ Functionalities
* 📍 **Interactive Map** – Visualization of all active fitness centers in Prilep using React-Leaflet.
* 🔍 **Smart Filtering** – Ability to search for facilities based on specific sports activities or names.
* ⭐ **Reviews & Ratings** – A system for sharing experiences with scrollable detailed comments.
* 📱 **Responsive Design** – An interface that scales seamlessly across mobile and desktop devices.
* 🔐 **Authentication** – Secure access for registered users.

### 🔐 Security & API Management
* **Django REST Framework (DRF):** Integrated for clean and standardized API endpoints.
* **Token Authentication:** Secure identity transfer between the frontend and the backend.
* **CRUD Operations:** Full data control with appropriate permissions based on user roles.

### 🛠 Technologies Used
* **Python / Django 6.0.3**
* **Django REST Framework**
* **React.js**
* **PostgreSQL**
* **React-Leaflet**
* **CSS (Cyber-Minimalist Aesthetic)**

### 🎨 Design Concept
The application is built with a **Cyber-Minimalist** aesthetic:
* Dark Mode with neon accents (Cyan/Blue).
* Glassmorphism effects on cards and menus.
* Clean typography and a focused user interface.

### 🎯 Project Goal
The primary goal is the practical application of **Full-stack** development, with a specific focus on integrating geo-location data and establishing a stable bridge between a Django API and a React frontend environment.
