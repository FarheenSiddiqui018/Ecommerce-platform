# Simple E-Commerce Platform

A minimal FastAPI-based e-commerce application using **SQLModel** and **PostgreSQL**, featuring:
- **Products** API (CRUD-like operations)
- **Orders** API (placing orders, validating stock)
- **Simple HTML/JS** UI (`static/index.html`)

---

## Getting Started

1. **Clone** the repository (replace `YOUR-USERNAME` and `YOUR-REPO` as appropriate):
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO
   ```

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

4. **(Optional) Configure environment**:

   - Copy the sample `.env` (if provided) or create a new one:
     ```bash
     cp .env.example .env
     ```
     Update the environment variables inside if you are using PostgreSQL or any other environment-specific config.  

---

## Running the Application

### 1. Using Virtual Environment (Manual Setup)

1. **Start PostgreSQL** (if you’re using Postgres locally) or ensure your `.env` points to the correct DB.

2. **Run the FastAPI app** with **Uvicorn**:
    ```bash
    uvicorn app.main:app --reload
    ```
    - By default, this starts the server at [http://127.0.0.1:8000](http://127.0.0.1:8000).

3. **Check the interactive API docs** at:
    - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)
    - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (ReDoc UI)

4. **Static Front-End**:
    - Access the sample UI at [http://127.0.0.1:8000/static/index.html](http://127.0.0.1:8000/static/index.html) if you’ve mounted `app/static` at `/static`.

### 2. Using Docker

#### Step-by-Step

1. **Ensure Docker and Docker Compose are installed**:
    - [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

2. **Create and configure your `.env` file**:
    - If you haven't already, copy `.env.template` to `.env`:
      ```bash
      cp .env.template .env
      ```
    - **Update** `.env` with your PostgreSQL credentials. Ensure that `POSTGRES_HOST` is set to `db` when using Docker Compose.
    
      Example `.env` for Docker:
      ```env
      POSTGRES_USER=myuser
      POSTGRES_PASSWORD=mypassword
      POSTGRES_DB=ecomm_db
      POSTGRES_HOST=db
      POSTGRES_PORT=5432
      TESTING=0
      ```

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

1. **Ensure Docker containers are running**:
    ```bash
    docker-compose up --build
    ```
    - Alternatively, you can run tests within the Docker container.

2. **Run Tests inside Docker**:
    - **Option A**: Modify `docker-compose.yml` to include a test service or run commands manually.
    - **Option B**: Use Docker's `exec` to run tests in the running container.

    **Example using `docker-compose exec`**:
    ```bash
    docker-compose exec web pytest
    ```

    - **Note**: Ensure that your Docker container has `pytest` and other test dependencies installed (already covered in `Dockerfile`).

3. **Check Coverage inside Docker**:
    ```bash
    docker-compose exec web pytest --cov=app --cov-report=term-missing
    ```

---


## Access the Documentation

Swagger UI:
- Open your web browser and navigate to: http://localhost:8000/docs
- You should see the interactive Swagger interface where you can explore and test your API endpoints.

ReDoc:
- Open your web browser and navigate to: http://localhost:8000/redoc
- ReDoc provides a detailed and user-friendly documentation interface for your API.

## Interacting with the API

### 1. Products
- **List Products**: `GET /products`  
- **Create a Product**: `POST /products`  
  Example body:
  ```json
  {
    "name": "Laptop",
    "description": "High performance",
    "price": 1299.99,
    "stock": 15
  }
  ```

### 2. Orders
- **Create an Order**: `POST /orders`  
  Example body:
  ```json
  {
    "products": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 3,
        "quantity": 1
      }
    ]
  }
  ```
  - Validates stock, calculates total price, and marks order as "completed".

---

## Additional Notes

1. **CORS**: If you’re calling the API from a different origin (like a separate React/Vue app), ensure [CORS settings](https://fastapi.tiangolo.com/tutorial/cors/) are configured in `main.py`.
3. **Environment Variables**: Store secrets (database credentials, etc.) in `.env` or another config method, not in version control.
4. **Deployment**: For production, consider using a proper WSGI/ASGI server (e.g., **gunicorn** + **uvicorn workers**), Docker, or a hosting platform (e.g., AWS, Heroku).
