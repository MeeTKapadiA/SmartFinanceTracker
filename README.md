# Smart Personal Finance Tracker

A comprehensive personal finance tracking application featuring a FastAPI backend and a modern Next.js frontend. It includes automated expense extraction from emails, intelligent categorization, and a rich dashboard for financial analytics.

![Landing Page](file:///C:/Users/Meet/.gemini/antigravity/brain/ce8469c4-2026-4ecb-8530-8d8e314bfc5f/landing_page_1764182122651.png)

## Features

### 🚀 Backend (FastAPI)
- **Authentication**: Secure JWT-based login and registration.
- **Transaction Management**: CRUD operations for expenses and income.
- **Smart Email Extraction**: Automatically scans Gmail for transaction emails and logs them (requires Google Cloud setup).
- **Analytics Engine**: Calculates total expenses, income, net savings, and category-wise breakdowns.
- **SQLite Database**: Lightweight and easy to set up (SQLAlchemy ORM).

### 💻 Frontend (Next.js + TailwindCSS)
- **Modern Dashboard**: Visualizes financial data with interactive charts (Recharts).
- **Responsive Design**: Fully responsive UI with Dark Mode support.
- **Transaction Table**: Filterable and sortable list of all transactions.
- **Email Scan Integration**: Trigger email scanning directly from the UI.

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic, Google Gmail API.
- **Frontend**: TypeScript, Next.js, TailwindCSS, Shadcn UI (concepts), Recharts, Framer Motion.
- **Database**: SQLite (Development).

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Google Cloud Project credentials (for email scanning).

### 1. Backend Setup
```bash
# Navigate to root
cd d:/FinanceTracker

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload --port 8001
```
The API will be available at `http://localhost:8001`. API Docs at `http://localhost:8001/docs`.

### 2. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
The app will be available at `http://localhost:3000` (or `3001` if 3000 is busy).

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=sqlite:///./finance.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: For Real Email Scanning
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## Email Integration
To enable the "Smart" email scanning feature, follow the [Setup Guide](SETUP_GUIDE.md) to configure your Google Cloud credentials.

## Screenshots
![Login Page](file:///C:/Users/Meet/.gemini/antigravity/brain/ce8469c4-2026-4ecb-8530-8d8e314bfc5f/login_page_1764182140815.png)
