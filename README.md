# Service Center Knowledge Check

This repository contains the Backend Module 2 “Knowledge Check” deliverables for the Service Center API:

- **Full CRUD** implementations for four resources (Mechanics, Customers, Inventory, Service Tickets)  
- **Interactive Swagger/OpenAPI** documentation served at `/api/docs/`  
- **Unit tests** (positive & negative) for every endpoint using Python’s `unittest`  

---

## 📁 Folder Structure
.
├── README.md
├── app.py
├── config.py
├── application/
│ ├── init.py
│ ├── extensions.py
│ ├── models.py
│ └── blueprints/
│ ├── mechanics.py
│ ├── customers.py
│ ├── inventory.py
│ └── service_ticket.py
├── static/
│ └── swagger.yaml
└── tests/
├── test_mechanics.py
├── test_customers.py
├── test_inventory.py
└── test_service_ticket.py

## 🚀 Getting Started

### 1. Clone & install dependencies
```bash
git clone https://github.com/your-org/service-center-knowledge-check.git
cd service-center-knowledge-check
python -m venv venv
# Windows (Git Bash)
source venv/Scripts/activate
# macOS/Linux
# source venv/bin/activate
pip install -r requirements.txt
2. Run the server
bash
Copy
Edit
python app.py
Open your browser at http://127.0.0.1:5000/api/docs/ to view the interactive Swagger UI.

3. Run the test suite
bash
Copy
Edit
python -m unittest discover tests -v

📝 Technologies & Libraries
Flask – lightweight web framework

Flask-Swagger-UI – interactive API docs

Flask-SQLAlchemy – ORM for SQLite

unittest – built-in Python testing framework

🎯 Learning Outcomes
Implement RESTful CRUD endpoints in Flask blueprints

Document every route with OpenAPI/Swagger (paths, parameters, responses, examples, security)

Write positive and negative unit tests for full coverage

Serve interactive API docs and automate validation via tests
