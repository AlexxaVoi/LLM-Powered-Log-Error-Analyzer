# LLM-Powered-Log-Error-Analyzer

## 🛠 Technology Stack
* **FastAPI**: A fast asynchronous framework.
* **SQLAlchemy**: An ORM for working with PostgreSQL.
* **Alembic**: Database migrations.
* **Pandas**: Efficient processing and cleaning of log texts.
* **Ollama (Llama 3)**: A local AI engine for error analysis.
* **PostgreSQL**: A reliable object-relational database for storing user information and log analysis history.
* **Pytest**: A framework for automated code testing and API reliability verification.
  
## 📝 Project Description
**AI Log Analyzer** is a FastAPI-based web application designed for analyzing system logs. The system allows you to upload log files, preprocess and clean them, and leverage the power of local LLMs (Llama 3 via Ollama) to identify the causes of failures and find solutions.

The project demonstrates the integration of a traditional Python backend with modern AI services.

## 🚀 How to Run the Project

### 1. Prerequisites
* **Python 3.10+**
* **PostgreSQL** (locally or in Docker)
* **Ollama** with a loaded model: `ollama pull llama3`

### 2. Setting up the environment
Clone the repository and set up environment variables:
```bash
# Create .env from the template
cp .env.example .env  # For Linux/macOS
copy .env.example .env # For Windows
```
Open the .env file and specify your DATABASE_URL.

### 3. Installing dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Working with the database (Alembic)
The project uses Alembic to manage migrations. To create the table structure, run:

```bash
alembic upgrade head
```

### 5. Running the application

```bash
uvicorn app.main:app --reload
```
API Documentation (Swagger UI): http://127.0.0.1:8000/docs

## 📁 Project structure

* alembic/ — a folder containing the database migration history. This folder stores scripts that automatically create and update tables in PostgreSQL. (Excluded from linter checks).
* app/ — the main directory containing the application’s source code:
  * models/ — database table definitions using SQLAlchemy (users, logs, analysis results).
  * schemas/ — Pydantic schemas responsible for validating input data and defining the API response format.
  * services/ — the “heart” of the application. This is where the business logic is concentrated: the authorization function, log cleaning using Pandas, and queries to the Ollama neural network.
  * routers/ — description of API endpoints. This is where it is defined which paths (URLs) are available to the user (for example, /upload or /analysis).
  * tests/ — a directory for automated testing using pytest
  * constants.py — used to store constant values that do not change during program execution.
  * create_tables.py — is a utility for quickly initializing a database.
  * database.py — configuration for connecting to the database and creating sessions.
  * main.py — the main file that initializes FastAPI and combines all routers.
 
* data/ - a folder containing a test file for testing the application.
* .env.example — a sample configuration file. It contains the names of the necessary variables (e.g., database connection details), but without any secret passwords.
* requirements.txt — a file listing all third-party libraries (FastAPI, SQLAlchemy, Pandas, etc.) required for the project to run.
* README.md — the project’s main documentation, describing its functionality and steps for running it.

## 🛠 Detailed API Information (Commands and Parameters)
All API requests (except for registration) require a Basic Auth header (username and password).

1. **User Management (Auth)**
* POST /register — Registration
  (Creates a new user in the system)
  * Parameters (Body):
    * username (string): Unique username (min. 3 characters).
    * password (string): Password.
  * Response: JSON with id and username.

* POST /login — Authentication
(Used to verify existing account credentials)
  * Response: User data or a 401 Unauthorized error.

2. **Log Management (Logs)**
* POST /upload — File Upload
(Accepts a physical log file, cleans it, and stores it in the database)
  * Parameters (Multipart/Form-Data):
    * file: File in .txt, .log, or .csv format.
  * Logic: The file passes through file_transformation, where Pandas extracts only lines containing critical errors (ERROR, CRITICAL, etc.).
  * Response: A log object created with id and log_text.

* POST /raw — Manual text insertion
(Accepts log text directly in the request body)
  * Parameters (Body):
    * log_text (string): Raw log text.
  * Response: A saved log object.

* GET /logs — Upload history
(Returns a list of all logs uploaded by the currently authorized user)
  * Response: An array of log objects.

3. **Log Analysis (AI Analysis)**
* POST /logs/{log_id}/analysis — Start analysis
(Sends the text of a specific log to the Ollama neural network)
  * Parameters (Path):
    * log_id (int): The unique identifier of the log in the database.
* Logic:
  1. The system checks whether this log belongs to the current user.
  2. The log text is passed to the Llama 3 model.
  3. The response is structured into three fields: issue, root_cause, solution.
  * Response: An analysis object with detailed recommendations.
