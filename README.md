<<<<<<< HEAD
# AgroMind Nexus AI
**Predict Smarter. Explain Clearly. Farm Better.**

A full-stack capstone starter for crop recommendation and agricultural decision support:
- React + TypeScript + Vite frontend
- FastAPI backend
- Random Forest classifier, evaluation metrics, feature importance
- Retrieval-based agricultural knowledge assistant with source references
- Optional Gemini-powered grounded answer generation
- Optional CrewAI multi-agent advisory integration
- SQLite by default for easy local setup; PostgreSQL supported through `DATABASE_URL`
- Docker Compose deployment starter

> Research prototype: predictions are based on the public crop recommendation dataset and are not a substitute for local agronomic advice. Dataset patterns may not generalize to Bangladesh or a specific field. Confidence scores are model scores, not probabilities of harvest success.

## Requirements
- Python 3.11 (recommended)
- Node.js 20+
- Git
- Optional: Gemini API key; Docker Desktop

## 1. Start the backend (Windows PowerShell)
```powershell
cd backend
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python scripts/train_model.py
uvicorn app.main:app --reload
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal and activate again. Or use `\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.

The training script tries to download the public CSV from a known raw GitHub URL. If that fails, download `Crop_recommendation.csv` from the Kaggle Crop Recommendation Dataset and place it at `backend/data/Crop_recommendation.csv`, then rerun the script. See `backend/data/README.md`.

Backend docs: http://127.0.0.1:8000/docs

## 2. Start the frontend (new terminal)
```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```
Open the Vite URL printed in the terminal (usually http://localhost:5173).

## 3. Optional Gemini answers
Create a Gemini API key in Google AI Studio, then put it in `backend/.env`:
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```
Restart the backend. Without a key, RAG returns retrieved passages and a deterministic evidence summary. Never put the key in the frontend.

## 4. Optional PostgreSQL
Default storage is SQLite, so the project runs locally without a database server. For PostgreSQL, set:
```env
DATABASE_URL=postgresql+psycopg://agromind:change_me@localhost:5432/agromind
```
Then use Docker Compose or your own PostgreSQL instance.

## 5. Git and GitHub
```powershell
git init
git add .
git commit -m "Initial AgroMind Nexus AI capstone"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agromind-nexus-ai.git
git push -u origin main
```
Create the empty GitHub repository first. Do not commit `.env`, API keys, virtual environments, model artifacts, or database files.

## API endpoints
- `GET /api/health`
- `GET /api/model/metrics`
- `POST /api/predict`
- `POST /api/knowledge/ask`
- `POST /api/advisory`
- `GET /api/history`

## Evaluation and limitations
`train_model.py` uses a stratified train/test split and reports accuracy, macro-F1, and a classification report. The API returns global Random Forest feature importances. These are useful baseline explanations, but they are not SHAP explanations. To add SHAP after the baseline works, install `shap` and implement local TreeExplainer output; do not describe global feature importance as SHAP.

The knowledge collection in `backend/app/knowledge.py` contains short starter notes with source URLs. Add reviewed documents before using this for real decisions. Retrieval is a lightweight TF-IDF baseline rather than ChromaDB vector search. CrewAI is represented by a deterministic specialist workflow so the core project runs without paid APIs; replace/extend it with actual CrewAI agents in `backend/app/agents_crewai.py` when ready.

## Suggested capstone evaluation
1. Model: accuracy, macro-F1, confusion matrix, per-class recall.
2. Explainability: check top features and local explanations against test cases.
3. Retrieval: manually assess whether top passages support each answer; track source coverage.
4. API: run `pytest`.
5. UI: test invalid inputs, loading/error states, responsive layout, and API failure.
6. Deployment: verify frontend-to-backend CORS, environment variables, persistence, and secrets.
=======
# 🌱 AgroMind Nexus AI — AI-Powered Crop Recommendation System

**AgroMind Nexus AI** is a full-stack artificial intelligence project designed to support data-driven agricultural decision-making through machine learning. The application combines a modern web frontend, a FastAPI backend, crop prediction capabilities, database integration, and Docker-based deployment.

The project aims to help users identify potentially suitable crops based on soil nutrient levels and environmental conditions, including nitrogen, phosphorus, potassium, temperature, humidity, soil pH, and rainfall.

By integrating machine learning with modern web technologies, AgroMind Nexus AI demonstrates how AI-driven agricultural decision support can be developed, deployed, and maintained as a full-stack application.

<p align="center">
  <strong>Smart Agriculture • Machine Learning • Full-Stack AI • Intelligent Decision Support</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-TypeScript-3178C6?logo=react&logoColor=white" alt="React and TypeScript">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white" alt="Docker">
</p>

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Deployment Links](#-deployment-links)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Machine Learning Approach](#-machine-learning-approach)
- [Dataset Requirements](#-dataset-requirements)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [Environment Configuration](#-environment-configuration)
- [Model Training](#-model-training)
- [Running the Application](#-running-the-application)
- [Docker Deployment](#-docker-deployment)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Security Considerations](#-security-considerations)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌍 Project Overview

Agricultural decisions depend on several interacting factors, such as soil nutrient availability, rainfall, temperature, humidity, and soil pH. Selecting a suitable crop requires considering these factors together rather than evaluating them individually.

AgroMind Nexus AI applies machine learning to this problem by accepting agricultural parameters and generating a crop prediction from a trained classification model.

The application is organized into three primary layers:

- **Frontend:** A TypeScript-based React application built with Vite and styled with Tailwind CSS.
- **Backend:** A Python application using FastAPI to handle HTTP requests, validate data, and coordinate prediction workflows.
- **Machine Learning:** A training pipeline and model inference module for crop recommendation.

The repository also includes database integration modules, an AI-agent-related module, automated API tests, and Docker configuration to support development and deployment.

### Project Information

| Item | Details |
|---|---|
| Project Name | AgroMind Nexus AI |
| Project Type | Full-Stack AI/ML Application |
| Domain | Smart Agriculture |
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn and associated Python libraries, as configured |
| Database | PostgreSQL, when configured |
| Containerization | Docker and Docker Compose |
| API Testing | Pytest |
| Repository | [AgroMind Nexus AI on GitHub](https://github.com/fairuzzahin/AgroMind_Nexus_AI) |

---

## ❗ Problem Statement

Crop suitability depends on soil properties and environmental conditions. Making crop selection decisions without considering these factors may lead to unsuitable planting choices and inefficient use of agricultural resources.

Manual analysis can be challenging when multiple input variables must be evaluated together.

AgroMind Nexus AI addresses this challenge by using a trained machine learning model to learn patterns from labeled agricultural data and predict a crop category for new input values.

The application provides a digital interface for submitting agricultural parameters and accessing the prediction through a backend API.

**Important:** Predictions are intended to support agricultural decision-making. They are not guaranteed outcomes and should be considered alongside local climate, soil testing, farming practices, and professional agricultural advice.

---

## 🎯 Objectives

The main objectives of AgroMind Nexus AI are to:

1. Develop an AI-powered crop recommendation application.
2. Use soil and environmental parameters as machine learning inputs.
3. Build a responsive frontend using React and TypeScript.
4. Develop a REST API using FastAPI.
5. Integrate model training and inference into the backend workflow.
6. Validate input data using structured request schemas.
7. Support database connectivity through a dedicated database module.
8. Explore AI-agent functionality through the CrewAI-related module.
9. Add automated backend API tests.
10. Support consistent development and deployment using Docker.
11. Maintain a modular, version-controlled project structure.

---

## ✨ Key Features

### 🌾 Machine Learning-Based Crop Prediction

Predicts a crop category from the agricultural parameters supported by the trained model.

### 🧪 Soil Nutrient Analysis

Uses three primary soil nutrient features:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)

### 🌦️ Environmental Feature Processing

Supports additional input features:

- Temperature
- Humidity
- Soil pH
- Rainfall

### 🖥️ Modern Web Frontend

Uses React, TypeScript, Vite, and Tailwind CSS to build the user-facing application.

### ⚡ REST API

Uses FastAPI to expose backend functionality through HTTP endpoints and JSON requests and responses.

### 🧩 Structured Request Validation

The `schemas.py` module provides a dedicated location for defining and validating API request and response structures.

### 🗄️ Database Integration

The `db.py` module separates database connectivity and related configuration from the main API implementation.

### 🤖 AI-Agent Extension Point

The `agents_crewai.py` module provides a place for CrewAI-related functionality. The actual agent capabilities depend on its implementation and configuration.

### 📚 Agricultural Knowledge Module

The `knowledge.py` module provides a dedicated location for agricultural knowledge-related logic.

### 🧪 Automated API Tests

The `tests/test_api.py` module supports automated testing of backend endpoints.

### 🐳 Docker Support

The root-level `Dockerfile` and `docker-compose.yml` provide the configuration for containerized execution.

---

## 🏗️ System Architecture

AgroMind Nexus AI separates the user interface, API logic, model inference, and supporting services into dedicated modules.

```mermaid
flowchart TD
    U[User] --> FE[React and TypeScript Frontend]
    FE --> API[FastAPI Backend]
    API --> S[Request Schemas and Validation]
    S --> ML[Machine Learning Module]
    ML --> MODEL[Trained Crop Classification Model]
    MODEL --> P[Crop Prediction]
    P --> API
    API --> FE
    FE --> R[Display Prediction Result]

    API -.-> DB[Database Module]
    API -.-> K[Knowledge Module]
    API -.-> AG[ CrewAI Agent Module]
```

The database, knowledge, and agent modules represent supporting integration points. Their actual runtime involvement depends on how the application connects these modules.

### Architectural Components

| Layer | Main Files | Responsibility |
|---|---|---|
| Frontend | `frontend/src/App.tsx` | Main user interface |
| Frontend Entry | `frontend/src/main.tsx` | Initializes the React application |
| Frontend Styling | `frontend/src/styles.css` | Global styles |
| Backend API | `backend/app/main.py` | Application initialization and API routes |
| Request Schemas | `backend/app/schemas.py` | Request and response validation |
| Machine Learning | `backend/app/ml.py` | Model loading and prediction logic |
| Database | `backend/app/db.py` | Database configuration and connectivity |
| Agricultural Knowledge | `backend/app/knowledge.py` | Knowledge-related functionality |
| AI Agents | `backend/app/agents_crewai.py` | CrewAI-related functionality |
| Model Training | `backend/scripts/train_model.py` | Training workflow |
| API Tests | `backend/tests/test_api.py` | Backend test cases |
| Containerization | `Dockerfile`, `docker-compose.yml` | Container build and service configuration |

---

## 🔄 How It Works

The intended crop prediction workflow follows these steps:

1. The user opens the frontend application.
2. The user enters the required agricultural parameters.
3. The frontend submits a request to the FastAPI backend.
4. The backend validates the request against the defined schema.
5. The machine learning module loads or accesses the trained model.
6. The model processes the input features in the expected order.
7. The backend returns the prediction as a structured API response.
8. The frontend displays the result.

If the trained model is missing or cannot be loaded, the backend should report the problem rather than silently return a prediction.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend and machine learning implementation |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation and schema definitions |
| Scikit-learn | Machine learning utilities |
| NumPy | Numerical computation |
| Pandas | Dataset processing |
| Joblib | Model serialization, if used by the implementation |
| React | Frontend user interface |
| TypeScript | Type-safe frontend development |
| Vite | Frontend development server and build tooling |
| Tailwind CSS | Utility-first styling |
| PostgreSQL | Relational database, when configured |
| SQLAlchemy | Database ORM, if used by the implementation |
| Psycopg | PostgreSQL driver, if configured |
| CrewAI | AI-agent framework, if enabled by the implementation |
| Pytest | Backend testing |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Git and GitHub | Version control and collaboration |

The installed versions and actual usage of these dependencies are defined by `backend/requirements.txt`, `frontend/package.json`, and the source code.

---

## 🤖 Machine Learning Approach

AgroMind Nexus AI uses a supervised classification workflow for crop recommendation.

### Input Features

The model is designed around seven agricultural features.

| Feature | Description |
|---|---|
| `N` | Nitrogen content |
| `P` | Phosphorus content |
| `K` | Potassium content |
| `temperature` | Environmental temperature |
| `humidity` | Relative humidity |
| `ph` | Soil pH |
| `rainfall` | Rainfall measurement |

The expected names, order, units, and value ranges must match the dataset and the implementation in `backend/app/ml.py`.

### Training Workflow

The model training script is located at:

`backend/scripts/train_model.py`

The general training workflow includes:

1. Loading the training dataset.
2. Checking the required feature and target columns.
3. Preparing the input features and crop labels.
4. Training the configured classification algorithm.
5. Evaluating model performance, if implemented in the training script.
6. Saving the trained model artifact.
7. Making the artifact available to the prediction service.

The exact algorithm, preprocessing pipeline, hyperparameters, model filename, and evaluation results should be documented after verifying the implementation.

### Model Artifact

The backend training data directory is:

`backend/data/`

The directory contains a `README.md` file explaining the data directory. The trained model artifact and source dataset may need to be generated or supplied separately.

Do not assume the model has already been trained merely because the API server starts successfully.

### Model Evaluation

Useful classification metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Only publish actual scores produced by the training and evaluation pipeline. Performance should be evaluated on appropriate held-out data rather than inferred from successful application execution.

---

## 📊 Dataset Requirements

The training dataset must contain the seven input features and a target column representing the crop label.

A typical crop recommendation dataset may use the following columns:

```text
N, P, K, temperature, humidity, ph, rainfall, label
```

The exact column names must match the training script.

### Dataset Preparation Checklist

- Obtain a dataset appropriate for crop classification.
- Place it in the location expected by `train_model.py`.
- Check that all required columns are present.
- Validate missing and invalid values.
- Confirm numerical features have compatible units and ranges.
- Confirm the target column contains crop labels.
- Ensure training and inference use compatible preprocessing.
- Avoid committing large datasets or generated model artifacts unless repository policy requires them.

See `backend/data/README.md` for any project-specific dataset instructions.

---

## 📁 Project Structure

The repository is organized as follows:

```text
agromind-nexus-ai/
│
├── README.md
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── frontend/
│   ├── package.json
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       └── styles.css
│
└── backend/
    ├── requirements.txt
    ├── .env.example
    ├── data/
    │   └── README.md
    ├── scripts/
    │   └── train_model.py
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── schemas.py
    │   ├── db.py
    │   ├── ml.py
    │   ├── knowledge.py
    │   └── agents_crewai.py
    └── tests/
        └── test_api.py
```

### Directory Responsibilities

**`frontend/`**

Contains the TypeScript-based React application, Vite configuration, Tailwind CSS configuration, and frontend environment-variable example.

**`backend/app/`**

Contains the FastAPI application and supporting modules for request schemas, model inference, database connectivity, agricultural knowledge, and AI agents.

**`backend/scripts/`**

Contains scripts used to train the machine learning model.

**`backend/data/`**

Contains dataset documentation and serves as the designated location for data-related artifacts.

**`backend/tests/`**

Contains automated backend API tests.

**`Dockerfile` and `docker-compose.yml`**

Define the project's container build and multi-service execution configuration.

---

## 💻 Prerequisites

Install the following tools before running the project:

| Requirement | Purpose |
|---|---|
| Python | Backend and ML runtime |
| Node.js | Frontend runtime and build tools |
| npm | Frontend dependency management |
| Git | Source-code management |
| Docker Desktop | Containerized execution |
| Docker Compose | Running configured services |

Python 3.11 is a suitable target when the project's Docker configuration uses Python 3.11. For native execution, use a Python version supported by the installed dependencies.

Verify the installed tools:

```bash
python --version
node --version
npm --version
git --version
docker --version
docker compose version
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fairuzzahin/AgroMind_Nexus_AI.git
cd agromind-nexus-ai
```

If Git creates a directory with a different name, enter the directory created by the clone command.

### 2. Configure the Backend

From the project root, navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

Install the backend dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a dependency does not support the installed Python version, use a compatible Python environment or run the project through Docker.

### 3. Configure Backend Environment Variables

Copy the backend example file:

```cmd
copy .env.example .env
```

Edit `.env` and provide the configuration required by the application.

Possible configuration items include a database connection string, frontend origin, and any required external-service credentials. Use only the variables expected by the current source code.

### 4. Prepare the Dataset

Read the instructions in:

`backend/data/README.md`

Place the required dataset at the location expected by:

`backend/scripts/train_model.py`

The exact filename must match the training script's configuration.

### 5. Train the Model

From the `backend` directory, run:

```bash
python scripts/train_model.py
```

Confirm that training completes successfully and that the resulting model artifact is saved at the path expected by `backend/app/ml.py`.

### 6. Start the Backend

From the `backend` directory, start the API server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The local API base URL is:

`http://127.0.0.1:8000`

FastAPI interactive documentation is normally available at:

`http://127.0.0.1:8000/docs`

The actual routes are determined by `backend/app/main.py`.

### 7. Configure the Frontend

Open a second terminal and navigate to the project root, then enter the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Create the frontend environment file:

```cmd
copy .env.example .env
```

Configure the backend URL using the variable expected by the frontend source code. For example, if the project uses `VITE_API_BASE_URL`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Vite exposes variables prefixed with `VITE_` to client-side code. Do not store private secrets in these variables.

### 8. Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

Open the local URL printed by Vite, commonly:

`http://localhost:5173`

Keep the backend and frontend terminals running while testing the application.

---

## 🔐 Environment Configuration

The repository contains two environment templates:

- `frontend/.env.example`
- `backend/.env.example`

These templates should document the variables required by each application component.

### Frontend Configuration

The frontend generally needs the backend API's base URL.

Example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Use this variable name only if it matches the frontend implementation.

### Backend Configuration

Backend variables depend on the actual implementation and may include database configuration.

Illustrative example:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE_NAME
```

The database URL format and variable name must match `backend/app/db.py` and the relevant environment configuration.

### Security Rules

- Never commit `.env` files containing credentials.
- Keep production secrets in your hosting provider's environment settings.
- Never expose database passwords in the frontend.
- Avoid committing private API keys.
- Configure production CORS with the actual trusted frontend origin.
- Use separate settings for local development and production.

---

## 🧠 Model Training and Inference

Training and inference serve different purposes.

**Training** uses labeled agricultural data to create the model artifact.

**Inference** loads the trained artifact and predicts a crop for a new set of input features.

The training script is:

```bash
python scripts/train_model.py
```

The inference module is:

`backend/app/ml.py`

Before testing predictions, verify that:

1. The dataset is available.
2. Training completes successfully.
3. The model artifact is generated.
4. The inference module can load the artifact.
5. Input feature names and order are consistent.
6. The backend handles missing or incompatible model files appropriately.

If the API is running but the model is unavailable, the health endpoint or prediction endpoint should be checked for the actual model status and error response.

---

## 🐳 Docker Deployment

The repository includes:

- `Dockerfile`
- `docker-compose.yml`

These files define how the application is built and run in containers.

### 1. Start Docker Desktop

Ensure Docker Desktop is running before executing Docker commands.

Verify Docker:

```bash
docker --version
docker compose version
```

### 2. Build and Start the Application

From the project root, where `docker-compose.yml` is located, run:

```bash
docker compose up --build
```

To run in the background:

```bash
docker compose up --build -d
```

### 3. Check Service Status

```bash
docker compose ps
```

### 4. Inspect Logs

View logs from all services:

```bash
docker compose logs
```

Follow logs in real time:

```bash
docker compose logs -f
```

If the Compose service is named `backend`, inspect the backend logs with:

```bash
docker compose logs -f backend
```

### 5. Stop the Services

```bash
docker compose down
```

This stops the Compose-managed services and removes their containers and network.

To remove named volumes as well:

```bash
docker compose down -v
```

**Warning:** Removing volumes can permanently delete persistent database data.

### Docker Configuration Notes

- Run Docker commands from the project root.
- Verify that all configured services have the required environment variables.
- Ensure the backend can access the dataset and trained model.
- Use the correct service name when connecting between containers.
- Use the configured internal database hostname for container-to-container connections.
- Verify the exposed ports before opening the application in a browser.
- Check service logs when a container fails to start.

The exact service names, ports, database settings, and model-training behavior depend on the actual Docker configuration.

---

## 🔌 API Documentation

The FastAPI application is defined in:

`backend/app/main.py`

### Local API

```text
http://127.0.0.1:8000
```

### Interactive Documentation

```text
http://127.0.0.1:8000/docs
```

### Alternative Documentation

```text
http://127.0.0.1:8000/redoc
```

These documentation endpoints are provided by FastAPI by default unless disabled or customized.

### API Testing

Use the interactive documentation or an API client to inspect and test the actual endpoints.

Recommended checks:

- Verify the health endpoint.
- Submit a valid crop prediction request.
- Test missing required fields.
- Test invalid data types.
- Test invalid parameter ranges where validation is defined.
- Verify model-unavailable behavior.
- Check response status codes and JSON structures.
- Verify that the frontend can access the backend.
- Check CORS behavior.

Consult `backend/app/schemas.py` for the expected request and response structures and `backend/app/main.py` for the available routes.

---

## 🧪 Testing

Automated backend tests are located in:

`backend/tests/test_api.py`

### Install Test Dependencies

Activate the backend virtual environment and ensure that the dependencies required by the test suite are installed.

### Run Tests

From the `backend` directory:

```bash
pytest
```

To display more detailed test output:

```bash
pytest -v
```

To run the specific API test module:

```bash
pytest tests/test_api.py -v
```

The test results depend on the test cases, application configuration, and whether the required model and database resources are available.

### Recommended Test Coverage

| Test Area | Expected Verification |
|---|---|
| Health endpoint | API status is returned correctly |
| Request validation | Invalid requests are handled appropriately |
| Prediction endpoint | Valid inputs produce the expected response structure |
| Model loading | Missing or invalid artifacts are handled safely |
| Database integration | Configured database operations work correctly |
| Error handling | Appropriate HTTP status codes and error responses are returned |
| Frontend integration | The frontend can reach the backend API |
| Docker execution | Configured services start and communicate correctly |

---

## 🛠️ Troubleshooting

### Problem 1: Model Is Not Trained

**Possible cause:** The model artifact does not exist at the path expected by the backend.

**Solution:**

1. Navigate to the backend directory.
2. Verify that the dataset is available.
3. Run the training script:

   ```bash
   python scripts/train_model.py
   ```

4. Check the training logs.
5. Confirm that the model artifact is generated.
6. Restart the backend if necessary.

### Problem 2: Frontend Cannot Connect to the Backend

**Possible causes:**

- The backend is not running.
- The API base URL is incorrect.
- The frontend environment variable has the wrong name.
- CORS is not configured correctly.
- The deployed backend URL is incorrect.

**Solution:** Check the backend URL, browser developer console, backend logs, and CORS settings.

### Problem 3: Dependency Installation Fails

**Possible cause:** An installed Python or Node.js version is incompatible with the project's dependency requirements.

**Solution:** Review `backend/requirements.txt` and `frontend/package.json`, use compatible runtimes, and reinstall dependencies in the appropriate environment.

### Problem 4: Docker Container Fails to Start

**Solution:**

```bash
docker compose ps
docker compose logs
```

Check the failing service's logs and verify its environment variables, file paths, port configuration, and service dependencies.

### Problem 5: Database Connection Fails

**Possible causes:**

- Incorrect database credentials.
- Incorrect hostname or port.
- PostgreSQL is not running.
- The configured database does not exist.
- The backend is using the wrong database URL for the current environment.

**Solution:** Check `backend/app/db.py`, the backend environment variables, and the Docker Compose database service configuration.

---

## 🔒 Security Considerations

Security is important when deploying an AI-powered application.

- Keep private credentials out of version control.
- Use environment variables for deployment-specific configuration.
- Restrict production CORS to trusted origins.
- Validate and constrain user input.
- Avoid returning sensitive internal error details to users.
- Protect database access with appropriate credentials.
- Use HTTPS for public deployments.
- Review dependency vulnerabilities periodically.
- Do not assume crop predictions are guaranteed agricultural outcomes.

---

## 🚧 Future Improvements

Potential future enhancements include:

- **Explainable AI:** Explain which agricultural features influence a prediction.
- **Prediction Confidence:** Present confidence estimates only when they are appropriately supported by the model.
- **Weather Integration:** Incorporate verified weather data.
- **Regional Crop Recommendations:** Improve suitability using region-specific agricultural data.
- **Prediction History:** Save previous predictions when persistence is implemented.
- **AI Agricultural Assistant:** Extend the knowledge and agent modules with validated agricultural information.
- **Model Monitoring:** Track prediction quality and data drift.
- **Automated CI/CD:** Run tests and builds automatically when code changes.
- **Model Versioning:** Record training data versions and model metadata.
- **Expanded Testing:** Add unit, integration, and end-to-end tests.

These are potential extensions, not claims that the features are already implemented.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

### Contribution Workflow

1. Fork the repository.
2. Create a new feature branch.
3. Implement the change.
4. Run relevant tests.
5. Commit the changes with a meaningful message.
6. Open a pull request describing the changes.

Example:

```bash
git checkout -b feature/improve-crop-prediction
git add .
git commit -m "feat: improve crop prediction workflow"
git push origin feature/improve-crop-prediction
```

---

## 📄 License

No license has been specified in this README.

Add a `LICENSE` file if you intend to distribute the project under an open-source license. Ensure that the selected license is appropriate for the project's ownership, dependencies, and intended use.

---

## 👩‍💻 Author

**Fairuz Zahin Sneha**

- **GitHub Profile:** [@fairuzzahin](https://github.com/fairuzzahin)
- **Project Repository:** [AgroMind Nexus AI](https://github.com/fairuzzahin/AgroMind_Nexus_AI)
- **Deployment URL:** [AgroMind Nexus AI Live Demo](https://agromind-nexus-ai-9.onrender.com)
---


>>>>>>> origin/main
