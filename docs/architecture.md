---
#(Architecture & Design)

```markdown
# Architecture Overview – Event Management System

## 1. Layered Architecture

The project follows a layered architecture**:

### 1.1 Models (Domain Layer)
- `BaseModel`
- `Venue`
- `Event`
- `Participant`
- `Ticket`

These classes represent real-world domain entities.
All models inherit from `BaseModel`.

---

### 1.2 Repositories (Data Access Layer)

- `VenueRepository`
- `EventRepository`
- `ParticipantRepository`
- `TicketRepository`

These classes handle all **CRUD operations** using SQLite.
The database logic is completely separated from the business logic.

---

### 1.3 Database (Infrastructure Layer)

- `DatabaseConnection` – Singleton pattern
- `schema.py` – Creates all database tables

---

### 1.4 Controllers (Application Layer)

- `CLIController`

Implements the **GRASP Controller** principle and manages all user interactions.

---

### 1.5 Main Application (Composition Root)

- `main.py`

Initializes logging, database connection, schema, and starts the CLI controller.

---

## 2. Object-Oriented Programming Usage

- **Abstraction & Encapsulation**

  - Implemented using the abstract `BaseModel` class.
  - All attributes are protected (`_name`, `_date`, etc.).
  - Access through `@property`.

- **Inheritance**

  - All models inherit from `BaseModel`.

- **Polymorphism**
  - Each class overrides the `display_info()` method.

---

## 3. Design Patterns Used

- **Singleton Pattern**

  - Used in `DatabaseConnection` to maintain a single database connection.

- **Repository Pattern**

  - Each entity has a dedicated repository for data access.

- **GRASP Controller**
  - Implemented in `CLIController`.

---

## 4. Database Tables

- `venues`
- `events`
- `participants`
- `tickets`

All tables are created in `src/database/schema.py`.
