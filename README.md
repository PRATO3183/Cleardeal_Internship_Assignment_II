# AI Lead Scoring Dashboard

This project is a full-stack web application built to fulfill the requirements of the ClearDeals AI Lead Scoring assignment. It predicts lead intent using a machine learning model and a rule-based re-ranker, delivered through a FastAPI backend and a responsive vanilla JavaScript frontend.

**Live Application URL:** `https://lead-generation-project.netlify.app/`

**Live API Documentation:** `https://cleardeal-internship-assignment-ii-lead.onrender.com/docs`

# **The URL won't stay active for a long time as the deployment plan was under the free Subscription on Render**

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup and Local Installation](#setup-and-local-installation)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Re-training the Model](#re-training-the-model)

---

## Project Overview

The goal of this application is to solve the problem of sales brokers wasting time on low-intent leads. It provides an "Intent Score" (from 0-100) to help prioritize prospects who are more likely to convert. The system uses a `GradientBoostingClassifier` for an initial score based on structured data and then applies a rule-based re-ranker to adjust this score based on unstructured text comments, simulating the contextual understanding of an LLM.

## Key Features

-   **ML-Powered Scoring:** Generates an initial intent score using a Scikit-learn model trained on a synthetic dataset with meaningful patterns.
-   **Rule-Based Re-ranking:** Adjusts the initial score based on positive ("urgent", "asap") and negative ("not interested") keywords in user comments.
-   **RESTful API:** A robust backend built with FastAPI serves predictions, handles data validation with Pydantic, and provides interactive documentation.
-   **Responsive Frontend:** A clean and intuitive UI built with vanilla HTML, CSS, and JavaScript that works seamlessly on desktop and mobile devices.
-   **Dynamic Results Table:** Scored leads are dynamically added to a results table, sorted by the highest reranked score to immediately show the highest-priority leads.

## Architecture

The application follows a decoupled, three-tier architecture:

1.  **Frontend (Client):** A static single-page application built with vanilla JS, HTML, and CSS, deployed on Netlify. It is responsible for user interaction and API communication.
2.  **Backend (Server):** A Python API built with FastAPI and deployed on Render. It handles business logic, serves the ML model, and validates data.
3.  **Model & Data:** The trained Scikit-learn model (`.pkl` file) and the synthetic dataset (`.csv` file) are stored within the backend's directory structure and accessed by a dedicated `ScoringService`.

## Project Structure

/lead-scoring-dashboard
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           └── score.py
│   │   ├── models/
│   │   │   └── lead.py
│   │   ├── services/
│   │   │   └── scoring_service.py
│   │   └── main.py
│   ├── data/
│   │   └── synthetic_leads.csv
│   ├── model/
│   │   └── intent_model_pipeline.pkl
│   ├── scripts/
│   │   ├── generate_data.py
│   │   └── train_model.py
│   ├── venv/
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── deliverables/
│   └── (Your PDF Report)
│
└── README.md

## Technologies Used

-   **Backend:** Python, FastAPI, Uvicorn, Scikit-learn, Pandas, Joblib
-   **Frontend:** HTML5, CSS3, Vanilla JavaScript
-   **Deployment:** Render (for Backend), Netlify (for Frontend)
-   **Development:** Git, GitHub, Visual Studio Code

## Setup and Local Installation

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Python 3.9+
-   A virtual environment tool like `venv`
-   A web browser
-   VS Code with the "Live Server" extension (recommended for frontend)

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[your-github-username]/lead-scoring-dashboard.git
    cd lead-scoring-dashboard/backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (Windows)
    .\venv\Scripts\activate

    # Activate it (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the FastAPI server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will now be running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Update the API URL:** Open `frontend/script.js` and ensure the `API_BASE_URL` constant points to your local backend server:
    ```javascript
    const API_BASE_URL = '[http://127.0.0.1:8000](http://127.0.0.1:8000)';
    ```

2.  **Launch the frontend:**
    -   Right-click the `frontend/index.html` file in VS Code and select "Open with Live Server".
    -   Alternatively, open the `index.html` file directly in your web browser.

## Re-training the Model

If you wish to generate new data or re-train the model, run the following scripts from within the `backend` directory (with your virtual environment activated):

1.  **Generate a new synthetic dataset:**
    ```bash
    python scripts/generate_data.py
    ```

2.  **Train a new model on the dataset:**
    ```bash
    python scripts/train_model.py
    ```
    This will overwrite the existing `intent_model_pipeline.pkl` file in the `backend/model/` directory.