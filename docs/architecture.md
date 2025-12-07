# 🏗 Project Architecture

This project follows a **4-Layer Architecture**:

CLI Controller
↓
Service Layer (Business Logic)
↓
Repository Layer (Database Access)
↓
SQLite Database

---

## 🔹 Controller Layer

- Handles user input/output
- Calls service layer
- No database logic here

Example:

- `CLIController`

---

## 🔹 Service Layer

- Validations
- Business rules
- Strategy pattern for ticket pricing
- Acts as mediator

Example:

- `VenueService`
- `TicketService`

---

## 🔹 Repository Layer

- Communicates with SQLite
- Pure SQL logic
- CRUD operations

Example:

- `VenueRepository`
- `EventRepository`

---

## 🔹 Database Layer

- SQLite
- Tables:
  - venues
  - events
  - participants
  - tickets
