# Deployment Guide: Study Guidance Bot

Since your **Backend** is already live at `https://ai-agent-9uef.onrender.com`, this guide focuses on deploying your **Frontend** so your entire application is accessible on the web.

## Phase 1: Prepare & Push to GitHub
Before deploying, your code needs to be on GitHub.

1.  **Initialize Git** (if not done):
    ```bash
    git init
    git add .
    git commit -m "Ready for deployment"
    ```
2.  **Create a Repo on GitHub**:
    *   Go to [GitHub.com/new](https://github.com/new).
    *   Name it `study-guidance-bot`.
    *   **Do not** initialize with README/gitignore (you already have them).
3.  **Push Code**:
    *   Copy the commands shown by GitHub (under "…or push an existing repository from the command line"), usually:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/study-guidance-bot.git
    git branch -M main
    git push -u origin main
    ```

## Phase 2: Deploy Frontend to Vercel
Vercel is the easiest place to host React/Vite apps.

1.  **Sign Up/Login**: Go to [vercel.com](https://vercel.com) and login with GitHub.
2.  **Add New Project**:
    *   Click **"Add New..."** -> **"Project"**.
    *   Import your `study-guidance-bot` repository.
3.  **Configure Project**:
    *   **Framework Preset**: It should auto-detect `Vite`.
    *   **Root Directory**: Click "Edit" and select `frontend` (since your react app is in the subfolder).
4.  **Environment Variables**:
    *   Expand the **"Environment Variables"** section.
    *   Add the following variable so your live frontend knows where your live backend is:
        *   **Name**: `VITE_API_URL`
        *   **Value**: `https://ai-agent-9uef.onrender.com`
5.  **Deploy**:
    *   Click **"Deploy"**.
    *   Wait a minute, and you will get a live URL (e.g., `https://study-bot-rho.vercel.app`).

## Phase 3: Verify
1.  Open your new Vercel URL.
2.  Try chatting with the bot.
3.  If it responds, congratulations! Your full stack app is live. 🚀

---

## Troubleshooting
*   **CORS Error**: If the bot doesn't reply, check your Backend (Render) logs. Ensure your backend code allows requests from your new Vercel domain.
    *   *Note*: Your current backend allows all origins (`allow_origins=["*"]`), so this should work immediately.
