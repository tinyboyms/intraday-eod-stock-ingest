# 📈 Stock Market EOD Data Pipeline

A Python project to fetch, clean, and store End-of-Day (EOD) stock market data from the **Marketstack API** into a **PostgreSQL** database. The focus is on secure API usage, clean data handling, and reliable daily storage.

---

## 🚀 Features

- ✅ Fetches daily EOD stock prices and volumes  
- 🧹 Cleans and processes data using **Pandas**  
- 💾 Stores data efficiently in **PostgreSQL**  
- 🔐 Uses environment variables to secure API keys and credentials  
- 🔧 Modular structure for easy extension and maintenance  

---

## ⚙️ Setup

### 1. Clone the Repository

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables
Create a .env file (copy from .env.example) and set your credentials:
MARKETSTACK_API_KEY=your_api_key_here
PG_HOST=localhost
PG_PORT=5432
PG_USER=your_postgres_user
PG_PASSWORD=your_password
PG_DATABASE=your_database

### 4. Run the Pipeline
python main.py

🔮 Future Plans
- ⏰ Automate daily data fetching using scheduled jobs (e.g., cron or cloud tasks)
- 🛠 Add robust error handling and logging for reliability
- 🔄 Implement incremental updates to avoid duplicates
- ⏱ Extend support to intraday data and ticker metadata
- ⚙️ Improve configuration management for easier deployment
- 📚 Document the project thoroughly and credit contributors

📝 Notes
- Ensure PostgreSQL is running and properly configured
- Keep your .env file secure — never commit API keys or passwords to GitHub
- The pipeline is designed to be extendable for additional data sources and types


