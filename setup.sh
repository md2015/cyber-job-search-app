#!/bin/bash
# setup.sh — One-time setup for CyberJobs Intelligence on Kali Linux
# Run: chmod +x setup.sh && ./setup.sh

set -e
echo "============================================"
echo "  CyberJobs Intelligence — Setup Script"
echo "============================================"

# 1. Create virtual environment
echo ""
echo "[1/5] Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
echo "[2/5] Installing Python packages..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "      Packages installed."

# 3. Create .env from template if not present
echo "[3/5] Checking environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "      Created .env file. Edit it to add your API key."
else
    echo "      .env already exists."
fi

# 4. Ensure secrets.toml exists (for local dev)
echo "[4/5] Checking Streamlit secrets..."
if [ ! -f .streamlit/secrets.toml ]; then
    mkdir -p .streamlit
    cp .env.example .streamlit/secrets.toml
    echo "      Created .streamlit/secrets.toml"
fi

# 5. Done
echo "[5/5] Setup complete."
echo ""
echo "============================================"
echo "  NEXT STEPS:"
echo "  1. Edit .env and add your JSearch API key"
echo "     (get one free at rapidapi.com/jsearch)"
echo ""
echo "  2. Activate the venv:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Run the app:"
echo "     streamlit run app.py"
echo "============================================"
