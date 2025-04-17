# 🧠 Online Learning Platform

A full-stack online learning platform built with Django (REST API), React, and Stripe. This platform enables instructors to create and manage courses and allows students to browse, purchase, and access content securely.

---

## 🚀 Features

### ✅ Core Features
- User authentication and registration (JWT based)
- Role-based access: Students and Instructors
- Course creation and management (Instructor)
- Course browsing, preview, and search (Student)
- Secure Stripe integration for payments
- Automatic enrollment on successful payment
- Protected course content (video, documents)
- Success and cancellation pages after payment
- Responsive and modern frontend (React + TailwindCSS)

### 📈 Advanced Features
- Admin dashboard for analytics and user management
- Stripe Webhook support for server-side payment verification
- Course progress tracking (Upcoming)
- Ratings and Reviews system (Upcoming)

---

## 🧩 Tech Stack

| Layer      | Technology |
|------------|------------|
| Frontend   | React, TailwindCSS, Axios |
| Backend    | Django, Django REST Framework |
| Payments   | Stripe API & Webhooks |
| Auth       | JWT (SimpleJWT) |
| Database   | PostgreSQL (or SQLite for development) |
| Deployment | Docker, Gunicorn, Nginx (Upcoming) |

---

## ⚙️ Installation & Setup

### 🔧 Backend (Django)

```bash
git clone https://github.com/yourusername/online-learning-platform.git
cd backend
python -m venv env
source env/bin/activate  # Use `env\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
