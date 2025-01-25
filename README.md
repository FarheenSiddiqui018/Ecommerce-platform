# Simple E-Commerce Platform

A minimal FastAPI-based e-commerce application using **SQLModel** and **PostgreSQL**, featuring:
- **Products** API (CRUD-like operations)
- **Orders** API (placing orders, validating stock)
- **Simple HTML/JS** UI (`static/index.html`)

---

## Getting Started

**Clone** the repository:
   ```bash
   git clone https://github.com/FarheenSiddiqui018/Ecommerce-platform.git
   cd Ecommerce-platform
   ```
---

### Using Virtual Environment (Manual Setup)

1. **Start PostgreSQL** (if you’re using Postgres locally) or ensure your `.env` points to the correct DB.

2. **Create and activate a virtual environment** (recommended):

   **macOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   **Windows**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you want developer/test tools, also install:
   ```bash
   pip install -r dev-requirements.txt
   ```
4. **Configure environment**:

   - Copy the sample `.env` (if provided) or create a new one:
     ```bash
     cp .env.example .env
     ```
     Update the environment variables inside if you are using PostgreSQL or any other environment-specific config.  

5. **Run the FastAPI app** with **Uvicorn**:
    ```bash
    uvicorn app.main:app --reload
    ```
    - By default, this starts the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

6. **Check the interactive API docs** at:
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
    - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc UI)

7. **Static Front-End**:
    - Access the sample UI at [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html)

### Using Docker

1. **Ensure Docker and Docker Compose are installed**:
    - [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. **Create and configure your `.env` file**:
    - If you haven't already, copy `.env.template` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - **Update** `.env` with your PostgreSQL credentials. Ensure that `POSTGRES_HOST` is set to `db` when using Docker Compose.

3. **Build and start the Docker containers**:
    ```bash
    docker-compose up --build
    ```
    - **Flags**:
        - `--build`: Rebuilds the images.
        - `-d`: (Optional) Runs containers in detached mode (in the background).

4. **Access the application**:
    - FastAPI app: [http://localhost:8000](http://localhost:8000)
    - Interactive API docs:
        - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
        - ReDoc UI: [http://localhost:8000/redoc](http://localhost:8000/redoc)
    - Static Front-End: [http://localhost:8000/static/index.html](http://localhost:8000/static/index.html)

5. **Stopping the containers**:
    - If running in detached mode:
      ```bash
      docker-compose down
      ```
    - If running in the foreground, press `CTRL+C` and then run:
      ```bash
      docker-compose down
      ```

---

### Managing Database Migrations with Alembic

Alembic is used to manage database schema changes in this project. Follow these steps to create and apply migrations:

#### 1. **Create a New Migration**
Generate a migration after modifying your SQLModel models:
```bash
alembic revision --autogenerate -m "Migration description"
```

#### 2. **Apply Migrations**
Apply the generated migrations to your database:
```bash
alembic upgrade head
```

#### 3. **Rollback Migrations**
Undo the most recent migration:
```bash
alembic downgrade -1
```

#### 5. **Key Files**
- **`alembic.ini`**: Configuration file (uses `env:DATABASE_URL`).
- **`alembic/env.py`**: Configures metadata and database connection.

#### 6. **Common Troubleshooting**
- **Missing Models in Migration**: Ensure all models are imported in `alembic/env.py`.

---

## Testing

### 1. Using Virtual Environment

1. **Activate your virtual environment** (if not already active).

2. **Install dev/test dependencies**:
    ```bash
    pip install -r dev-requirements.txt
    ```

3. **Run Tests** with **Pytest**:
    ```bash
    pytest
    ```
    - Discovers and runs **unit** + **integration** tests by default.
    - You can also run tests in specific subfolders, e.g.:
      ```bash
      pytest tests/unit
      pytest tests/integration
      ```

4. **Check Coverage** (if `pytest-cov` is installed):
    ```bash
    pytest --cov=app --cov-report=term-missing
    ```
    - The test suite uses an **in-memory SQLite DB** by default, so it won’t affect your local or production PostgreSQL DB.

### 2. Using Docker

    ```bash
    docker-compose run --rm test
    ```
