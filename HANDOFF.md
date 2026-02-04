# Tailor Home Finder - Project Handoff Document
**Date:** February 4, 2026
**Status:** Full-Stack Platform with Email Notification System

---

## PROJECT OVERVIEW

**Tailor Home Finder** - A luxury real estate platform for high-end properties.

**Repository:** https://github.com/tailortrends/tailorhomefinder
**Project Path:** `/home/user/tailorhomefinder/`

---

## WHAT'S COMPLETE

### **Frontend (Vue 3 + TypeScript)** - 100% Complete
- **Path:** `/frontend/`
- **Running on:** http://localhost:5173 or 5174
- **Stack:** Vue 3, Pinia, Firebase Auth, Tailwind CSS, DaisyUI, Leaflet, Chart.js

**Features:**
- User authentication (Firebase)
- Property search with advanced filters
- Interactive maps (Leaflet with dark theme)
- Price history charts (Chart.js)
- User dashboard
- Admin panel with tabs
- Image lightbox gallery
- Property comparison (up to 3 properties)
- Favorites system (localStorage)
- Contact form with real API integration
- Mobile responsive design

### **Backend (FastAPI + PostgreSQL)** - 100% Complete
- **Path:** `/backend/`
- **Running on:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Stack:** FastAPI, SQLAlchemy, PostgreSQL, Pydantic, fastapi-mail

**Data Loaded:** 247,941 properties across multiple states

**API Endpoints:**
```
Properties:
- GET  /api/properties/           - List properties with filters & pagination
- GET  /api/properties/{id}       - Get single property
- GET  /api/properties/stats/overview - Platform statistics

Inquiries (NEW):
- POST /api/inquiries/contact     - Submit contact form (sends emails)
- GET  /api/inquiries/            - List all inquiries (admin)
- GET  /api/inquiries/{id}        - Get single inquiry
- PATCH /api/inquiries/{id}/status - Update inquiry status
- GET  /api/inquiries/stats/overview - Inquiry statistics
```

### **Email Notification System** - NEW
- **fastapi-mail** integration
- HTML email templates with luxury branding
- Background task email sending
- Three email templates:
  1. `inquiry_notification.html` - Sent to admin/agent
  2. `inquiry_confirmation.html` - Sent to user
  3. `tour_scheduled.html` - Sent for tour requests

**Email Configuration:**
- SMTP support (Gmail, SendGrid, Mailgun)
- Environment-based configuration
- Development mode (EMAIL_ENABLED=false logs emails)
- Production mode (EMAIL_ENABLED=true sends real emails)

---

## PROJECT STRUCTURE

```
tailorhomefinder/
├── backend/
│   ├── .env.example (template for environment variables)
│   ├── run.py (start server)
│   ├── create_tables.py (create database tables)
│   ├── src/app/
│   │   ├── main.py (FastAPI app with routers)
│   │   ├── api/
│   │   │   ├── properties.py (property endpoints)
│   │   │   └── inquiries.py (inquiry/contact endpoints) NEW
│   │   ├── models/
│   │   │   ├── property.py (SQLAlchemy Property model)
│   │   │   └── inquiry.py (SQLAlchemy Inquiry model) NEW
│   │   ├── schemas/
│   │   │   ├── property.py (Pydantic property schemas)
│   │   │   └── inquiry.py (Pydantic inquiry schemas) NEW
│   │   ├── services/
│   │   │   ├── property_service.py
│   │   │   └── email_service.py NEW
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── email_config.py NEW
│   │   ├── templates/email/ NEW
│   │   │   ├── inquiry_notification.html
│   │   │   ├── inquiry_confirmation.html
│   │   │   └── tour_scheduled.html
│   │   └── db/database.py
│   └── pyproject.toml (UV dependencies)
├── frontend/
│   ├── src/
│   │   ├── views/ (Home, Search, PropertyDetail, Dashboard, Admin, Favorites)
│   │   ├── components/
│   │   │   └── property/
│   │   │       ├── ContactForm.vue (updated with API integration)
│   │   │       └── ... (17 total components)
│   │   ├── stores/ (auth, properties, favorites, comparison)
│   │   └── services/
│   │       ├── realEstate/dataService.ts
│   │       └── inquiryService.ts NEW
│   └── public/data/
└── data/states/ (8,477 JSON source files)
```

---

## HOW TO START EVERYTHING

### **1. Start PostgreSQL**
- Ensure PostgreSQL is running on port 5432
- Database: `tailorhomefinder`

### **2. Start Backend**
```bash
cd /home/user/tailorhomefinder/backend

# Create .env file from template
cp .env.example .env
# Edit .env with your database credentials

# Create tables (if new database)
uv run python create_tables.py

# Start server
uv run python run.py
```
Visit: http://localhost:8000/docs

### **3. Start Frontend**
```bash
cd /home/user/tailorhomefinder/frontend
pnpm install
pnpm dev
```
Visit: http://localhost:5173

---

## EMAIL CONFIGURATION

To enable real email sending, update `/backend/.env`:

```env
# Enable email sending
EMAIL_ENABLED=true

# Gmail SMTP (use App Password, not regular password)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@tailorhomefinder.com
MAIL_FROM_NAME=TailorHomeFinder
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=true
MAIL_SSL_TLS=false

# Admin email for notifications
ADMIN_EMAIL=admin@yourdomain.com
```

**Development Mode (default):**
- `EMAIL_ENABLED=false`
- Emails are logged but not sent
- Useful for testing without SMTP setup

---

## DATABASE STATS

- **Total Properties:** 247,941
- **Files Processed:** 8,477 JSON files
- **Tables:** properties, inquiries

**Create inquiries table:**
```bash
cd backend
uv run python create_tables.py
```

---

## KEY CREDENTIALS

**PostgreSQL:**
- User: `tailoruser`
- Password: `tailorpass123`
- Database: `tailorhomefinder`
- Port: 5432

---

## NEXT STEPS / FUTURE FEATURES

1. **User Registration Backend** - Store user data in PostgreSQL
2. **Favorites Backend API** - Persist favorites to database
3. **Saved Searches** - Store and alert on new matches
4. **Price Drop Alerts** - Email notifications for price changes
5. **Geospatial Search** - Search by radius/polygon
6. **Production Deployment** - Railway/Render/Fly.io

---

## RECENT CHANGES (February 4, 2026)

### Email Notification System
- Added `fastapi-mail` dependency
- Created email configuration (`core/email_config.py`)
- Created Inquiry model and schemas
- Created email service with HTML templates
- Created inquiries API endpoints
- Updated ContactForm.vue to call real API
- Created frontend inquiry service

### Files Added/Modified:
**Backend (new):**
- `src/app/api/inquiries.py`
- `src/app/models/inquiry.py`
- `src/app/schemas/inquiry.py`
- `src/app/services/email_service.py`
- `src/app/core/email_config.py`
- `src/app/templates/email/*.html` (3 templates)
- `create_tables.py`
- `.env.example`

**Frontend (modified):**
- `src/services/inquiryService.ts` (new)
- `src/components/property/ContactForm.vue` (updated)

---

**Generated:** February 4, 2026
