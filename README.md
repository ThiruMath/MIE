# Mistake Intelligence Engine (MIE)

The Mistake Intelligence Engine (MIE) is a Pedagogical Chain-of-Thought (PedCoT) dashboard built with Streamlit and powered by Google Gemini Pro. It analyzes student math steps to identify "thinking mistakes" (cognitive bugs) rather than just grading answers as right or wrong.

## Core Features
1. **Diagnostic AI Engine**: Categorizes math errors as **Factual** (wrong facts), **Procedural** (wrong steps), or **Conceptual** (misunderstanding underlying principles).
2. **Mastery Heatmap**: Visualizes the class's understanding of different mathematical concepts.
3. **Risk Radar**: A chart highlighting students who exhibit recurring mistake patterns over time.
4. **Live Tutor Diagnosis**: A real-time playground to test the Gemini PedCoT engine.

---

## 🚀 How to Run Locally

### 1. Prerequisites
- Python 3.9+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### 2. Setup environment and install dependencies
```bash
# Option 1: Using pip
pip install -r requirements.txt
```

### 3. Add Your Secrets
Create a `.streamlit/secrets.toml` file in the root directory (using the provided template) and add your API key:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR-API-KEY-HERE"
```

### 4. Create your Synthetic Data
If `student_logs.csv` doesn't exist, generate the dataset:
```bash
python synthetic_data_generator.py
```

### 5. Run the Engine!
```bash
streamlit run app.py
```

---

## 🌐 Deploying to Streamlit Community Cloud (streamlit.app)

To share this portfolio project publicly:

1. **Commit to GitHub**: Push this repository to a public GitHub repo.
2. **Log into Streamlit**: Go to [share.streamlit.io](https://share.streamlit.io/) and connect your GitHub account.
3. **Deploy App**: Click "New app", select your repository, branch, and point the "Main file path" to `app.py`.
4. **Configure Secrets**: Before clicking Deploy, click **Advanced Settings**. In the "Secrets" box, paste your `GEMINI_API_KEY`:
    ```toml
    GEMINI_API_KEY = "YOUR-API-KEY-HERE"
    ```
5. Click **Deploy!** Your app will be live at a sharable URL.
