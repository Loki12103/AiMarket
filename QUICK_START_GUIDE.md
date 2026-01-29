# 🚀 Quick Start Guide - AI Market Sentiment Analysis

This guide will get you up and running with the complete automated market intelligence system.

## 📋 Prerequisites

1. **Python Environment**
   ```powershell
   # Activate virtual environment
   .\env\Scripts\activate
   ```

2. **Environment Variables**
   
   Create a `.env` file in the project root:
   ```env
   # Gmail SMTP Configuration
   sender=your-email@gmail.com
   gmail_password=your-app-password
   reciver=recipient@gmail.com
   
   # Gemini API Key
   Gemini_Api_key=your-gemini-api-key
   
   # Slack Webhook (Optional)
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```

3. **Get Gmail App Password**
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Search "App passwords"
   - Generate new app password
   - Copy and paste into `.env` file

## 🎯 Running the Dashboard

### Option 1: Dashboard with Background Automation (Recommended)

```powershell
streamlit run advanced_dashboard.py
```

**What happens:**
- ✅ Dashboard opens at http://localhost:8501
- ✅ Background scheduler starts automatically
- ✅ Weekly automation runs every Monday at 00:00
- ✅ Sidebar shows automation status
- ✅ Manual trigger button available

### Option 2: Updated Dashboard (Latest Version)

```powershell
streamlit run advanced_dashboard_updated.py
```

This version has cleaner code with the same functionality.

## 🤖 Testing the Automation

### Quick Test (30 seconds)

Edit [scheduler.py](scheduler.py) line 95:
```python
# Change this:
schedule.every().monday.at("00:00").do(collect_weekly_data)

# To this (for testing):
schedule.every(30).seconds.do(collect_weekly_data)
```

Then run:
```powershell
python scheduler.py
```

You'll receive an email in 30 seconds!

### Manual Test (Immediate)

```powershell
python weekly_automation.py
```

This runs the complete pipeline immediately:
1. Collects data from all sources
2. Analyzes sentiment spikes
3. Detects trend shifts
4. Sends email notifications

## 📧 Understanding Notifications

### You will receive 5 types of emails:

1. **Sentiment Spike Alert** 
   - When sentiment changes by 15%+
   - Subject: "⚠️ POSITIVE/NEGATIVE Sentiment Spike - [Category]"

2. **Trend Shift Alert**
   - When category mentions change by 20%+
   - Subject: "📈 Trend Shift UP/DOWN - [Category]"

3. **Data Collection Summary**
   - After each automation run
   - Subject: "✓ Weekly Data Collection - Success"

4. **Pipeline Error Alert**
   - When analysis fails
   - Subject: "✗ Pipeline Error - [Pipeline Name]"

5. **Critical Error Alert**
   - When entire automation fails
   - Subject: "✗ CRITICAL: Weekly Automation Failed"

## 🔍 Dashboard Features

### Main Dashboard
- **Key Metrics**: Total reviews, sentiment percentages
- **Sentiment Distribution**: Pie chart
- **Category Comparison**: Bar charts
- **Time Trends**: Weekly sentiment, monthly demand
- **Topic Insights**: LDA topic distribution
- **Reddit Trends**: Category popularity
- **News Sentiment**: Latest news analysis
- **Cross-Source Comparison**: Reviews vs Reddit vs News

### AI Insight Panel (Right Sidebar)
- Ask questions about the data
- Powered by FAISS vector database
- Uses Gemini 2.5 Flash for intelligent responses
- Examples:
  - "What are customers saying about electronics?"
  - "Which category has declining sentiment?"
  - "What are the main complaints in beauty products?"

### Automation Status (Sidebar)
- Shows if scheduler is running
- Displays start time
- Lists automated tasks
- Manual trigger button

## 📊 Data Files

The system uses these data files from `final data/`:

| File | Description |
|------|-------------|
| category_wise_lda_output_with_topic_labels.csv | Product reviews with sentiment & topics |
| reddit_category_trend_data.xlsx | Reddit posts by category |
| news_data_with_sentiment.csv | News articles with sentiment |

## 🛠️ Customization

### Change Schedule

Edit [scheduler.py](scheduler.py):

```python
# Weekly (Production)
schedule.every().monday.at("00:00").do(collect_weekly_data)

# Daily
schedule.every().day.at("09:00").do(collect_weekly_data)

# Every 6 hours
schedule.every(6).hours.do(collect_weekly_data)

# Every 30 minutes (Testing)
schedule.every(30).minutes.do(collect_weekly_data)
```

### Change Alert Thresholds

Edit [weekly_automation.py](weekly_automation.py):

```python
# Line 104: Sentiment spike threshold
threshold = 0.15  # Change to 0.10 for 10%, 0.20 for 20%

# Line 157: Trend shift threshold
threshold = 0.20  # Change to 0.15 for 15%, 0.25 for 25%
```

### Add More Alert Recipients

Edit `.env`:
```env
# Use comma-separated emails
reciver=admin1@company.com,admin2@company.com,team@company.com
```

Then update [notification.py](notification.py) to split and send to multiple recipients.

## 🧪 Testing Components

### Test Email System
```powershell
python notification.py
```

### Test Scheduler (without running automation)
```powershell
python -c "from scheduler import test_scheduler; test_scheduler()"
```

### Test Vector Database
```powershell
python ask_vector_db.py
```

### Test Monitoring
```powershell
python -c "from weekly_automation import WeeklyAutomation; WeeklyAutomation().run_weekly_pipeline()"
```

## 📁 Project Structure

```
AIMarket/
├── advanced_dashboard.py          # Main dashboard (with scheduler)
├── advanced_dashboard_updated.py  # Updated dashboard (cleaner code)
├── weekly_automation.py           # Complete automation pipeline
├── scheduler.py                   # Scheduler logic
├── streamlit_scheduler.py         # Background scheduler for Streamlit
├── notification.py                # Email notification system
├── ask_vector_db.py              # Standalone Q&A tool
├── final data/                    # Data directory
│   ├── category_wise_lda_output_with_topic_labels.csv
│   ├── reddit_category_trend_data.xlsx
│   └── news_data_with_sentiment.csv
├── consumer_sentiment_faiss1/     # Vector database
├── .env                           # Environment variables (create this)
└── env/                           # Virtual environment
```

## ⚙️ Production Deployment

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly, Monday, 00:00
4. Action: Start a program
   - Program: `C:\Path\to\Python\python.exe`
   - Arguments: `C:\Path\to\scheduler.py`
   - Start in: `C:\Path\to\AIMarket`

### Keep Dashboard Running 24/7

```powershell
# Install pm2-like tool for Python
pip install supervisor

# Or use simple batch script
# create run_dashboard.bat:
@echo off
:loop
streamlit run advanced_dashboard.py
timeout /t 5
goto loop
```

## 🐛 Troubleshooting

### Email not sending
- ✅ Check `.env` file exists and has correct credentials
- ✅ Verify Gmail app password (not regular password)
- ✅ Enable "Less secure app access" if using old Gmail
- ✅ Check sender email matches the one in Google Account

### Scheduler not running
- ✅ Check if `streamlit_scheduler.py` imported in dashboard
- ✅ Verify session state shows "Scheduler Running"
- ✅ Check terminal for error messages
- ✅ Test with 30-second interval first

### Dashboard not loading
- ✅ Activate virtual environment
- ✅ Install missing packages: `pip install -r requirements.txt`
- ✅ Check data files exist in `final data/` directory
- ✅ Verify FAISS vector database exists

### Vector database errors
- ✅ Make sure `consumer_sentiment_faiss1/` folder exists
- ✅ Check HuggingFace embeddings model downloaded
- ✅ Set `allow_dangerous_deserialization=True` in FAISS.load_local()

### Gemini API errors
- ✅ Verify `Gemini_Api_key` in `.env`
- ✅ Check API quota/limits
- ✅ Test with simple prompt first

## 📝 Next Steps

1. ✅ **Test the system** - Run dashboard and verify automation
2. ✅ **Check email alerts** - Trigger manual run to test notifications
3. ⬜ **Merge data cleaning** - Integrate preprocessing into pipeline
4. ⬜ **Implement live APIs** - Replace placeholder data collection
5. ⬜ **Generate reports** - Add PDF/Excel export
6. ⬜ **Push to GitHub** - Version control
7. ⬜ **Create presentation** - Demo slides

## 📚 Additional Documentation

- [NOTIFICATION_GUIDE.md](NOTIFICATION_GUIDE.md) - Detailed notification setup
- [SCHEDULER_GUIDE.md](SCHEDULER_GUIDE.md) - Scheduler configuration
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Complete task tracking
- [ZEROSHOT_GUIDE.md](ZEROSHOT_GUIDE.md) - Zero-shot classification
- [api_examples/API_GUIDE.md](api_examples/API_GUIDE.md) - API integration

## 🎉 You're All Set!

Run the dashboard and watch the magic happen:

```powershell
streamlit run advanced_dashboard.py
```

Your automated market intelligence system is now:
- 📊 Visualizing multi-source sentiment data
- 🤖 Answering questions with AI
- 📧 Sending real-time alerts
- ⏰ Running weekly automation
- 📈 Detecting trends and spikes

**Happy analyzing! 🚀**
