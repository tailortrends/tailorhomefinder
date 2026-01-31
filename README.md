# Tailor Home Finder

A professional real estate search platform for high-value properties ($1M+), focusing on East Coast markets.

## 🏗️ Project Structure
```
Tailor Home Finder/
├── frontend/           # Vue 3 + TypeScript application
├── firebase/           # Firebase configuration files
└── backend/            # FastAPI + UV (to be created)
```

## 📦 Technology Stack

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Language:** TypeScript
- **State Management:** Pinia
- **Routing:** Vue Router
- **Build Tool:** Vite
- **Package Manager:** pnpm
- **Authentication:** Firebase Auth
- **Database:** Firestore
- **Storage:** Firebase Storage

### Backend (Planned)
- **Framework:** FastAPI
- **Package Manager:** UV
- **Database:** PostgreSQL
- **Data Source:** RapidAPI (real estate listings)

## 🚀 Getting Started

### Frontend Setup
```bash
cd frontend
pnpm install
pnpm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your Firebase credentials:
```bash
cd frontend
cp .env.example .env
```

Required variables are documented in `frontend/.env.example`.

## 📖 Documentation

- **Frontend Setup Guide:** See `frontend/SETUP.md`
- **API Documentation:** Coming soon
- **Deployment Guide:** Coming soon

## 🔗 Links

- **GitHub Repository:** https://github.com/tailortrends/tailorhomefinder
- **Firebase Project:** tailorhomefinder

## 🎯 Current Status

### ✅ Completed
- Professional frontend folder structure
- Firebase authentication integration
- Basic UI components and views
- Routing with protected routes
- TypeScript type definitions
- Git repository setup

### 🚧 In Progress
- Backend FastAPI setup
- RapidAPI integration
- Property data models
- Search functionality

### 📋 Planned
- User profiles and preferences
- Saved properties feature
- Advanced filtering
- Map integration
- Email notifications
- Admin dashboard

## 👥 Team

**Tailor Trends, LLC**

## 📝 License

Private - All Rights Reserved