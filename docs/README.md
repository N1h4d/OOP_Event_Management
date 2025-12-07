# 🎫 Event Management System (OOP + SQLite)

This is a **console-based Event Management System** developed in Python using
**Object-Oriented Programming (OOP)**, **SOLID, GRASP, CUPID principles**, and
**SQLite** as a database.

The project was developed for **Seminar 1 and Seminar 2** at university and
demonstrates clean architecture, layered design, design patterns, and testing.

---

## 🚀 Features

### ✅ Features

- Object-Oriented Design (OOP)
- SQLite Database Integration
- CRUD Operations:
  - Venue
  - Event
  - Participant
  - Ticket
- Logging system
- CLI-based UI
- Repo + Service + Controller Layer Architecture
- UUID-based IDs
- Encapsulation & Abstraction with BaseModel

### ✅ Extended Features

- ✅ Service Layer (Business Logic)
- ✅ Update & Delete Operations
- ✅ Strategy Pattern (Ticket Pricing)
- ✅ Unit Testing with `unittest`
- ✅ Layered Architecture (Controller → Service → Repository → DB)
- ✅ Error Handling & Logging at all layers

---

## 🛠 Technologies Used

- Python 3
- SQLite
- Logging
- unittest (Testing)
- OOP & Design Patterns

---

## 📂 Project Structure

OOP_Event_Management/
│
├── src/
│ ├── controllers/
│ ├── services/
│ │ ├── pricing/ ← Strategy Pattern
│ ├── repositories/
│ ├── models/
│ ├── database/
│ ├── logging_config.py
│ └── main.py
│
├── tests/
│ ├── test_ticket_service.py
│ ├── test_repositories.py
| ├── test_models.py
│
├── docs/
│ ├── design_principles.md
│ ├── architecture.md
│ ├── seminar2_features.md
│
└── README.md

## ▶️ How to Run

```bash
python3 -m src.main


🧪 How to Run Tests
python3 -m unittest discover

'''

🧠 Design Patterns Used
 - Strategy Pattern (Ticket Pricing)
 - Singleton (Database Connection)
 - Repository Pattern
 - Service Layer Pattern



```
