# 💸 Digital Wallet System - FastAPI Backend

A secure and scalable digital wallet backend system built with **FastAPI** and **SQLAlchemy**, developed by [subhamhacks](https://github.com/subhamhacks).  
This project supports wallet management, currency conversion, peer-to-peer transfers, product purchases, and transaction tracking.

---
# Digital Wallet System

A powerful and secure digital wallet system built with FastAPI and PostgreSQL.

✨ **Visit the live application:** [Digital Wallet System](https://digital-wallet-system-fastapi-postgresql-orpe.onrender.com/docs)

## 🚀 Features

- ✅ User Registration & Login (Basic Auth)
- 💰 Add/Check Wallet Balance (with optional currency conversion)
- 🔁 Pay Another User
- 📜 View Transaction History
- 🛒 Product Catalog (Add, List)
- 🛍️ Purchase Product using Wallet
- 🧪 Test Cases with Pytest
- 🔒 Proper error handling & clean JSON responses

---

## 📦 Tech Stack

- **FastAPI** (API Framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Database)
- **Pytest** (Testing)
- **CurrencyAPI** (for currency conversion)

---

## 📄 API Endpoints

| Method | Endpoint         | Description                     | Auth Required |
|--------|------------------|----------------------------------|---------------|
| POST   | `/register`      | Register new user                | ❌ No         |
| POST   | `/login`         | Login & get Basic Auth header    | ❌ No         |
| POST   | `/wallet/Fund`   | Fund wallet                      | ✅ Yes        |
| GET    | `/wallet/balance`| Check wallet balance             | ✅ Yes        |
| POST   | `/wallet/pay`    | Transfer money to another user   | ✅ Yes        |
| GET    | `/stmt`          | View transaction history         | ✅ Yes        |
| POST   | `/product`       | Add product                      | ✅ Yes        |
| GET    | `/product`       | List all products                | ❌ No         |
| POST   | `/buy`           | Purchase a product               | ✅ Yes        |

---

## 🔧 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/subhamhacks/digital-wallet-system.git
   cd digital-wallet-system
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
4. **Create a .env file**:
    ```env
    CURRENCY_API_KEY=your_currencyapi_key
    DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
5. **Run the app**:
   ```bash
   uvicorn main:app --reload
6. **Visit Swagger Docs**:
   ```arduino
   http://127.0.0.1:8000/docs
7. **Run Tests**:
   ```bash
   pytest
📌 Author - subhamhacks
