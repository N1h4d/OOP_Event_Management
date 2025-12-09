---

#`docs/architecture.md`

```md
# 🏗️ System Architecture

This project follows a **multi-layered clean architecture** approach.

---

## 🔹 Architectural Layers

### 1️⃣ Controller Layer

- Handles all user input/output
- No business logic
- Example: `CLIController`

### 2️⃣ Service Layer

- Business logic
- Validations
- Rules
- Example: `EventService`, `TicketService`

### 3️⃣ Repository Layer

- Database access only
- Pure SQL operations
- Example: `EventRepository`

### 4️⃣ Model Layer

- Domain objects
- Pure data classes
- Example: `Event`, `Venue`, `Participant`, `Ticket`

---

## 🔁 Data Flow

User → CLI → Service → Repository → SQLite

---

## 🧠 Design Patterns

### ✅ Singleton

Used in `DatabaseConnection` to keep **one active database connection**.

### ✅ Strategy Pattern

Used in ticket pricing:

- StandardPricing
- VipPricing
- StudentPricing

---

## ✅ Principles Applied

### SOLID:

- SRP – Each class has single responsibility
- OCP – New ticket pricing strategies can be added
- DIP – Services depend on Repository abstraction

### GRASP:

- Controller → CLIController
- Information Expert → Services
- Low Coupling → All layers separated

### CUPID:

- Composable services
- Predictable structure
- Idiomatic Python
- Domain-focused design

---

## ✅ Logging Architecture

- All important operations are logged:
  - Create
  - Read
  - Update
  - Delete
- Logs written to:
  logs/app.log

---

✅ This architecture fully satisfies **Seminar 1 + Seminar 2 + Final Framework** standards.
