# 🎟️ Event Management System (CLI + SQLite)

This project is a fully-featured **Event Management System** developed using **Python**, following **Object-Oriented Programming (OOP)** principles and advanced **software design principles** such as:

- ✅ SOLID
- ✅ GRASP
- ✅ CUPID
- ✅ Design Patterns (Singleton, Strategy)
- ✅ Layered Architecture (Controller, Service, Repository, Model)

The system is controlled via a **Command Line Interface (CLI)** and persists data using **SQLite**.

---

## 📌 Features

✅ Venue Management (CRUD)  
✅ Event Management (CRUD)  
✅ Participant Management (CRUD)  
✅ Ticket Sales with Dynamic Pricing (Strategy Pattern)  
✅ VIP / Student / Standard Pricing  
✅ Validation System for All Fields  
✅ Real-Time Error Handling  
✅ SQLite Database Integration  
✅ Logging System  
✅ Fully Interactive CLI

---

## 🧱 Technologies Used

- Python 3
- SQLite
- OOP & Design Patterns
- CLI Interface
- Logging Module

---

## 🗂️ Project Structure

src/
│
├── controllers/
│ └── cli_controller.py
│
├── services/
│ └── _\_service.py
│
├── repositories/
│ └── _\_repository.py
│
├── models/
│ └── venue.py, event.py, participant.py, ticket.py
│
├── utils/
│ └── validators.py
│
├── database/
│ ├── connection.py
│ └── schema.py
│
├── main.py
│── logging_config.py

---

## ▶️ How to Run the Project

```bash
python3 -m src.main

Validation System

All fields are strictly validated:

✅ Email format

✅ Phone format

✅ Date & Time format

✅ Positive numeric values

✅ Gender validation

✅ Yes/No boolean validation
```

Design Principles Used

| Principle        | Usage                                            |
| ---------------- | ------------------------------------------------ |
| SOLID            | Applied across Service & Repository layers       |
| GRASP            | Controller handles inputs, Services handle logic |
| CUPID            | Clean and modular design                         |
| Strategy Pattern | Ticket pricing                                   |
| Singleton        | Database connection                              |
| Repository       | Database abstraction                             |

Academic Purpose
This project was developed as a final academic project based on:
✅ Seminar 1 requirements
✅ Seminar 2 enhancements
✅ OOP_FF Final Framework
