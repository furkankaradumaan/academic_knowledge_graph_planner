# 🧠 Academic Knowledge Graph & Study Planner

An intelligent, heterogenous knowledge graph and study routing application that abstracts academic courses, topics, and subtopics into a **Directed Graph**. It automatically computes the most optimal chronological learning path for students using advanced graph theory algorithms.

This project focuses heavily on **Object-Oriented Programming (OOP) abstractions**, **Relational Database Integrity**, and robust **RESTful API** structures to bridge complex backend data structures with an interactive frontend visualization layer.

---

## 🚀 Key Features

*   **Heterogeneous Knowledge Graph:** Models discrete academic entities (Subjects, Topics, Subtopics) and maps their structural dependencies via directional semantic edges (`INCLUDES`, `SUBTOPIC`, `PREREQUISITE`).
*   **Algorithmic Path Optimization (Topological Sort):** Implements a Depth-First Search (DFS) tracking algorithm utilizing a three-color node state architecture (`WHITE`, `GRAY`, `BLACK`). It resolves complex dependency chains and features built-in **Cycle Detection** to prevent infinite deadlocks in curriculum planning.
*   **Dynamic Graph Visualization (Cytoscape.js):** Generates an interactive, responsive node-link diagram utilizing a force-directed spring embedder layout engine (`cose`). The view re-renders smoothly via asynchronous operations whenever data modifications occur.
*   **Desktop-Grade UX Architecture:** Features a smooth draggable, resizable splitter sidebar constrained by stateful browser window listeners, combined with isolated viewport overflow scrolling.
*   **RESTful Compliance:** Adheres strictly to standard HTTP methods (`GET`, `POST`, `DELETE`) leveraging localized Query Parameters to preserve statelessness across the wire.

---

## 🛠️ Technology Stack

*   **Backend Engineering:** Python 3.x, Flask (Micro-framework)
*   **Data Storage:** SQLite3 Engine with declarative foreign keys and `ON DELETE CASCADE` mechanics.
*   **Frontend UI Layer:** HTML5, CSS3 (Grid Template Mosaics & Flexbox layouts), Vanilla Javascript (ES6+ Async/Await architecture).
*   **Graph Engine:** Cytoscape.js (Data visualization architecture).

---

## 📐 Software Architecture & Abstraction Layers

The application isolates concerns cleanly across an decoupled 3-tier software architecture:
1.  **Domain Model Layer (`model.py`):** Encapsulates the core business entities. It references physical entities via in-memory pointers to construct a live **Object Graph** inside the RAM runtime environment.
2.  **Data Access Object Layer (`sqlite_manager.py`):** Inherits from an abstract base class (`DatabaseManager`) to fulfill the Dependency Inversion Principle. It guarantees transactional integrity by explicitly enforcing `PRAGMA foreign_keys = ON;` constraints across database boundaries to avoid orphan records.
3.  **Core Routing Layer (`algorithm.py`):** Isolates the top-level analytical functions from framework and structural dependencies, evaluating graph vectors strictly based on pointer evaluations.

---

## 📊 Database Schema Blueprint

The infrastructure organizes spatial nodes and connective edges efficiently across 3 relational entities:

*   **`subjects`:** `id (INTEGER PRIMARY KEY)`, `name (TEXT)`
*   **`topics`:** `id (INTEGER PRIMARY KEY)`, `name (TEXT)`, `main_topic_id (INTEGER FK)`, `subject_id (INTEGER FK)`
*   **`prerequisites`:** `id_first (INTEGER FK)`, `id_next (INTEGER FK)` -> `PRIMARY KEY(id_first, id_next)`

---

## 📦 Local Installation & Deployment

### 1. Clone the repository
```bash
git clone https://github.com
cd academic-study-planner
```

### 2. Install Python Dependencies
```bash
pip install Flask
```

### 3. Initialize Server
```bash
python app.py
```
**Important Note:** Use `sqlite database.sqlite < schema.sql` command for the first time you use it. This will initialize the database for application.

Once the development server binds successfully, open your browser and navigate to **`http://127.0.0.1:5000`** to access the live application environment.

---

## 💡 Operational Heuristics
*   **Hierarchical Generation:** When inserting a topic, specifying only the `Course Name` declares it as a **Root Node (Main Topic)**. Specifying only the `Parent Topic Name` natively flattens it as a **Nested Leaf Node (Subtopic)**.
*   **Logical Execution:** Clicking the **Sort** button triggers the analytical compilation step, delivering a structured workflow layout mapping out which foundational nodes must be conquered first.

