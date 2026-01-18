# How to Run StudyBot 🚀

This guide will help you set up and run the StudyBot project on your local machine.

## Prerequisites

Ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v16 or higher)
- [Python](https://www.python.org/) (v3.10 or higher)

---

## 1. Backend Setup 🐍

The backend handles the AI logic using FastAPI and Google Gemini.

1.  **Navigate to the backend folder:**
    Open a terminal and run:
    ```bash
    cd "IBM Project/backend"
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    - **Windows:** `venv\Scripts\activate`
    - **Mac/Linux:** `source venv/bin/activate`

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    - Create a file named `.env` in the `backend` folder.
    - Add your Google API Key:
      ```env
      GOOGLE_API_KEY=your_api_key_here
      ```

5.  **Run the Server:**
    ```bash
    python -m uvicorn backend.main:app --reload
    ```
    The backend will start at `http://localhost:8000`.

---

## 2. Frontend Setup ⚛️

The frontend is a React application built with Vite.

1.  **Open a new terminal** (keep the backend terminal running).

2.  **Navigate to the frontend folder:**
    ```bash
    cd "IBM Project/frontend"
    ```

3.  **Install Dependencies:**
    ```bash
    npm install
    ```

4.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    The frontend will start at `http://localhost:5173`.

---

## 3. Using the App 📚

1.  Open your browser and go to `http://localhost:5173`.
2.  You should see the StudyBot interface.
3.  Type a message or click a suggestion to start learning!

---

## Troubleshooting

-   **Backend Connection Error:** Ensure the backend terminal is running and shows "Application startup complete".
-   **API Errors:** Check your `.env` file in the `backend` folder and ensure your `GOOGLE_API_KEY` is valid.
-   **Port Conflicts:** If ports 8000 or 5173 are busy, the terminals will suggest alternative ports.
