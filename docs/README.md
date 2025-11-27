# Event Management System – Python OOP Project

This project is a **console-based Event Management System** developed in Python.
It is designed to demonstrate strong **Object-Oriented Programming (OOP)** concepts,
a clean **layered architecture**, and the practical implementation of
**SOLID, GRASP, and CUPID** design principles.

All project data is stored using **SQLite**, and the system includes
**centralized logging** and **unit testing**.

---

## 1. Key Features

- ✅ Create, list, and manage venues
- ✅ Create, list, and manage events
- ✅ Register participants
- ✅ Sell and list tickets
- ✅ Persistent data storage using SQLite
- ✅ Centralized logging system (console + optional file logging)
- ✅ Unit testing with `unittest`
- ✅ Clean layered architecture
- ✅ Full application of OOP principles
- ✅ SOLID, GRASP, and CUPID design principles implemented
- ✅ CLI-based interactive user interface

---

## 2. Technologies Used

- **Python 3**
- **SQLite** (`sqlite3` module)
- **Python logging module**
- **unittest** for testing
- **UUID** for unique entity identification

---

## 3. Project Structure

```text
OOP_Event_Management/
├── src/
│   ├── main.py
│   ├── logging_config.py
│   ├── database/
│   │   ├── connection.py
│   │   └── schema.py
│   ├── models/
│   │   ├── base_model.py
│   │   ├── venue.py
│   │   ├── event.py
│   │   ├── participant.py
│   │   └── ticket.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── venue_repository.py
│   │   ├── event_repository.py
│   │   ├── participant_repository.py
│   │   └── ticket_repository.py
│   └── controllers/
│       └── cli_controller.py
├── tests/
│   ├── test_models.py
│   └── test_repositories.py
└── docs/
    ├── README.md
    ├── architecture.md
    ├── user_guide.md


Object-Oriented Programming Implementation

This project fully demonstrates:

Abstraction
Implemented via the abstract BaseModel class.

Encapsulation
All attributes are protected (_name, _date, etc.) and accessible only via properties.

Inheritance
All domain models (Event, Venue, Participant, Ticket) inherit from BaseModel.

Polymorphism
Each model overrides the display_info() method differently.

Design Principles Applied

✅ SOLID
Single Responsibility Principle (SRP)
Open/Closed Principle (OCP)
Liskov Substitution Principle (LSP)
Interface Segregation Principle (ISP)
Dependency Inversion Principle (DIP)

✅ GRASP
Controller (CLIController)
Creator (Controller creates model objects)
High Cohesion
Low Coupling

✅ CUPID
Composable
Understandable
Predictable
Idiomatic
Domain-based


Design Patterns Used
Singleton Pattern
Used in DatabaseConnection to ensure a single SQLite connection.

Repository Pattern
Used to separate data access logic from the business logic.

Controller Pattern (GRASP)
Used to manage all user interactions through CLIController.



Logging System
The application uses a centralized logging system:
Logs application start and stop
Logs all CREATE operations
Logs all READ (list) operations
Logs database initialization
Can optionally log into a file (logs/app.log)
This makes the system fully traceable and debuggable.



Unit tests are implemented using Python's built-in unittest framework:
✅ Model tests (test_models.py)
✅ Repository tests with in-memory SQLite (test_repositories.py)

Run all tests using:
python3 -m unittest



CLI Menu Overview
1. Create Venue
2. List Venues
3. Create Event
4. List Events
5. Create Participant
6. List Participants
7. Sell Ticket
8. List Tickets
0. Exit

```
