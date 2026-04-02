# Sethupathy Government Arts College - Modernized Website

A modern, responsive, and easy-to-manage official website for **Sethupathy Government Arts College (SGAC)**, Ramanathapuram.

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask API
- **Database**: MySQL (Aiven Cloud)
- **Auth**: JWT tokens

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env with your Aiven MySQL credentials
# Copy from .env.example and fill in your DB_PASSWORD

# Run the server
python app.py
```

The Flask API will run at `http://localhost:5000`

### 2. Frontend Setup

The frontend static files are served by Flask. Just open:
- **Website**: `http://localhost:5000`
- **Admin Login**: `http://localhost:5000/admin-login.html`
- **Admin Dashboard**: `http://localhost:5000/admin.html` (after login)

### 3. Database Setup

Run the Flask app once - it auto-creates all tables on startup.

Default admin credentials:
- **Email**: `admin@sgac.edu.in`
- **Password**: `sgac2025`

### 4. Deploy on Vercel + Render/Railway

**Frontend** (Vercel):
- Point Vercel to your GitHub repo
- Set `vercel.json` as configured

**Backend** (Render/Railway):
- Create a Python web service
- Set environment variables from `.env`
- Set start command: `gunicorn app:app`

**Important**: For production, set environment variables in your hosting dashboard, NOT in `.env` files.

## API Endpoints

### Public (no auth)
- `GET /api/public/all` - All site data
- `GET /api/public/site-config` - College info
- `GET /api/public/news` - News items
- `GET /api/public/events` - Events
- `GET /api/public/announcements` - Announcements
- `GET /api/public/carousel` - Carousel images
- `GET /api/public/downloads` - Downloads
- `GET /api/public/departments` - All departments
- `GET /api/public/departments/<key>` - Single department with faculty/gallery

### Admin (JWT required)
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Current user
- `GET /api/admin/stats` - Dashboard counts
- `GET/POST/PUT/DELETE /api/admin/news` - News CRUD
- `GET/POST/PUT/DELETE /api/admin/events` - Events CRUD
- `GET/POST/PUT/DELETE /api/admin/announcements` - Announcements CRUD
- `GET/POST/PUT/DELETE /api/admin/carousel` - Carousel CRUD
- `GET/POST/PUT/DELETE /api/admin/downloads` - Downloads CRUD
- `GET/POST/PUT/DELETE /api/admin/departments` - Departments CRUD
- `GET /api/admin/departments/<id>/faculty` - Faculty list
- `POST/PUT/DELETE /api/admin/faculty` - Faculty CRUD
- `POST/DELETE /api/admin/gallery` - Gallery CRUD
- `POST/DELETE /api/admin/activities` - Activities CRUD
- `POST/DELETE /api/admin/achievements` - Achievements CRUD
- `POST/DELETE /api/admin/econtent` - E-content CRUD
- `GET/PUT /api/admin/site-config` - Site settings
- `POST /api/admin/password` - Change password

## Environment Variables

```
DB_HOST=mysql-3c95dc03-keyan.h.aivencloud.com
DB_PORT=12610
DB_USER=avnadmin
DB_PASSWORD=your_password
DB_NAME=defaultdb
DB_SSL_CA=./ca.pem

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRY_HOURS=24
```

## Features

- Full admin dashboard with login system
- Manage News, Events, Announcements
- Manage Carousel images
- Manage Downloads
- Manage Departments with Faculty, Gallery, Activities, Achievements, E-Content
- Site configuration (college name, address, principal info)
- JWT-based authentication
- Password change functionality

---

Developed for **Sethupathy Government Arts College, Ramanathapuram**.
