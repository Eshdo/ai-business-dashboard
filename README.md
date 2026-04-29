# 📊 AI Business Dashboard

An AI-powered business analytics dashboard that transforms raw data into actionable insights using interactive visualizations and large language models.

---

## 🚀 Live Demo

👉 https://ai-business-dashboard-a5dzhwkjlmf3plkgbsbwfp.streamlit.app/
---

## 📌 Overview

The **AI Business Dashboard** is a modern SaaS-style data analytics tool that allows users to:

* Upload business datasets (CSV)
* Explore data with interactive charts
* Apply dynamic filters
* View real-time KPI metrics
* Generate AI-driven insights

---

## ✨ Features

### 📂 Data Upload

* Upload CSV files بسهولة
* Automatic data preview

### 🔍 Smart Filters

* Dynamic filtering by categories (Region, Product, etc.)
* Real-time updates across dashboard

### 📊 KPI Metrics

* Total, Average, Max, Min
* Updates based on selected filters

### 📈 Interactive Charts

* Bar, Line, Pie charts
* Built using Plotly for modern UI

### 🏆 Top Performers

* Identify best-performing categories instantly

### 🤖 AI Insights Engine

* Uses Groq (LLM) to generate:

  * Key trends
  * Risks
  * Opportunities
  * Business recommendations

---

## 🛠️ Tech Stack

* **Frontend & Backend:** Streamlit
* **Data Processing:** Pandas
* **Visualization:** Plotly
* **AI Integration:** Groq API (LLM - LLaMA 3)

---

## 📁 Project Structure

```
ai-business-dashboard/
│
├── app.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml  (not included in repo)
```

---

## 🔐 Environment Variables

Create a `.streamlit/secrets.toml` file:

```
GROQ_API_KEY = "your_api_key_here"
```

⚠️ Do NOT upload this file to GitHub.

---

## ⚙️ Installation & Run Locally

```bash
# Clone the repo
git clone https://github.com/Eshdo/ai-business-dashboard.git

# Navigate to project
cd ai-business-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🌐 Deployment

Deployed using **Streamlit Cloud**

Steps:

1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Add secrets in dashboard settings
4. Deploy 🚀

---

## 🎯 Future Improvements

* 🔐 User authentication
* 📡 Real-time data integration
* 📊 Advanced analytics (forecasting)

---

## 👩‍💻 Author

**Eeshani Fernando**
Aspiring Data Analyst & AI Developer

---

## ⭐ Support

If you like this project:

* ⭐ Star this repo
* 🔗 Share on LinkedIn

---

## 📜 License

This project is open-source and available under the MIT License.
