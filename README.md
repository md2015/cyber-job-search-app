# CyberJobs Intelligence Dashboard

A real-time cybersecurity job search and qualification matcher.
Built with Streamlit, Python, JSearch API, Pandas, and Plotly.

---

## What This App Does

1. Searches real job listings from 100+ cybersecurity companies.
2. Extracts: job title, location, salary, education required, certs, skills.
3. Compares each job against your education and certification profile.
4. Shows a match status: **Yes / Partial Match / No** with a score.
5. Displays charts and a dashboard for career gap analysis.
6. Exports everything to Excel with multiple filtered sheets.

---

## Folder Structure

```
cyberjobs/
├── app.py                    ← Main entry point (run this)
├── requirements.txt          ← Python packages
├── setup.sh                  ← One-time setup script
├── .env.example              ← Copy to .env and add your API key
├── .gitignore
├── .streamlit/
│   ├── config.toml           ← Dark theme settings
│   └── secrets.toml          ← API keys for cloud deployment (never commit)
├── data/
│   ├── companies.py          ← Master list of 100+ companies
│   └── profile.py            ← User profile defaults and degree/cert mappings
├── pages/
│   ├── search.py             ← Job search UI
│   ├── dashboard.py          ← Charts and analytics
│   ├── profile.py            ← Profile editor
│   └── export_page.py        ← Table view and Excel/CSV download
└── utils/
    ├── api_client.py         ← JSearch API integration
    ├── matcher.py            ← Education qualification matching algorithm
    └── exporter.py           ← Excel export logic
```

---

## Step-by-Step Setup on Kali Linux

### Step 1 — Get a Free JSearch API Key

1. Go to https://rapidapi.com
2. Create a free account.
3. Search for **JSearch** by letscrape.
4. Click Subscribe → select the **Free plan** (200 requests/month).
5. Copy your `X-RapidAPI-Key`.

### Step 2 — Clone or Create the Project

```bash
cd ~/Desktop
git clone https://github.com/YOUR_USERNAME/cyberjobs.git
cd cyberjobs
```

Or if starting fresh:
```bash
mkdir cyberjobs && cd cyberjobs
# Copy all files from VS Code into this folder
```

### Step 3 — Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

### Step 4 — Add Your API Key

Open the `.env` file:
```bash
nano .env
```

Replace the placeholder:
```
JSEARCH_API_KEY=paste_your_key_here
```

Save: `Ctrl+O`, Enter, `Ctrl+X`.

### Step 5 — Run the App

```bash
source venv/bin/activate
streamlit run app.py
```

Your browser will open at **http://localhost:8501**.

---

## How to Use the App

1. **My Profile page** — Verify your degrees, certs, and skills are correct.
2. **Job Search page** — Select 3–5 companies (to stay within free API limits).
3. Click **Search Companies**.
4. View job cards with match status and score breakdown.
5. Go to **Dashboard** for charts and gap analysis.
6. Go to **Export Results** to download your Excel report.

---

## Match Score Formula

| Component | Weight | How It Works |
|-----------|--------|-------------|
| Degree    | 35%    | Compares your degree tier to the job requirement |
| Certs     | 30%    | Fuzzy-matches your certifications to job requirements |
| Skills    | 35%    | Counts skill mentions in job description vs your profile |

- **75–100%** → ✅ Yes (fully qualified)
- **45–74%** → ⚠️ Partial Match
- **0–44%** → ❌ No

---

## Deploying to Streamlit Community Cloud (Free)

1. Push your project to GitHub (make sure `.gitignore` excludes `.env` and `secrets.toml`).
2. Go to https://streamlit.io/cloud and sign in with GitHub.
3. Click **New app** → select your repo → set main file to `app.py`.
4. In **Advanced settings → Secrets**, paste:
   ```toml
   JSEARCH_API_KEY = "your_key_here"
   ```
5. Click Deploy. Your app gets a public URL instantly.

---

## Scaling to All 341 Companies

The `data/companies.py` file currently has ~100 companies.
To add more:
1. Open `data/companies.py`.
2. Add company names to the `COMPANIES` list.
3. The search page will automatically include them.

To avoid hitting the free API limit, search 5–10 companies per session
or upgrade to a paid JSearch plan.

---

## API Used

**JSearch by letscrape** via RapidAPI
- Free tier: 200 requests/month
- Endpoint: `https://jsearch.p.rapidapi.com/search`
- Covers: LinkedIn, Indeed, Glassdoor, ZipRecruiter, and more aggregated together

---

## Author

Md Shafiqul Baten Sumon
Adjunct Lecturer, Cybersecurity — Bronx Community College, CUNY
GitHub: github.com/mdshafiqulbaten
