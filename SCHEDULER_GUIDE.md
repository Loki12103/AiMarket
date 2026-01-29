# Automated Scheduler Guide

## What is a Scheduler?

A scheduler automates tasks by running code at specific times or intervals without manual intervention.

### Use Cases
- ⏰ Run data collection every week
- 📊 Monitor sentiment/trends automatically
- 📧 Send automated reports
- 🔄 Keep data fresh and updated

## How It Works

### 1. Time-Based Scheduling

```python
import schedule

# Run every Monday at midnight
schedule.every().monday.at("00:00").do(collect_data)

# Run every 5 minutes
schedule.every(5).minutes.do(check_status)

# Run every day at 9 AM
schedule.every().day.at("09:00").do(send_report)
```

### 2. Background Threading

Threads allow tasks to run in the background without blocking your main program (Streamlit dashboard).

```python
import threading

# Start scheduler in background
thread = threading.Thread(target=run_scheduler, daemon=True)
thread.start()
```

**daemon=True**: Thread automatically stops when main program exits

## Project Implementation

### Files Created

1. **scheduler.py** - Main scheduler logic
   - Weekly data collection
   - Monitoring pipeline
   - Email notifications
   - Test functions

2. **streamlit_scheduler.py** - Streamlit integration
   - Background thread runner
   - Session state management
   - Manual trigger button
   - Status display

3. **advanced_dashboard.py** - Updated with scheduler import

## Configuration

### Scheduler Settings

Edit `scheduler.py`:

```python
# Production: Weekly on Monday midnight
schedule.every().monday.at("00:00").do(collect_weekly_data)

# Testing: Every 30 seconds
schedule.every(30).seconds.do(test_scheduler)

# Testing: Every 5 minutes
schedule.every(5).minutes.do(collect_weekly_data)

# Daily: Every day at 9 AM
schedule.every().day.at("09:00").do(collect_weekly_data)
```

### Schedule Options

| Pattern | Code |
|---------|------|
| Every N seconds | `schedule.every(10).seconds.do(func)` |
| Every N minutes | `schedule.every(5).minutes.do(func)` |
| Every N hours | `schedule.every(2).hours.do(func)` |
| Every day | `schedule.every().day.do(func)` |
| Every day at time | `schedule.every().day.at("09:00").do(func)` |
| Every Monday | `schedule.every().monday.do(func)` |
| Every Monday at time | `schedule.every().monday.at("00:00").do(func)` |
| Every week | `schedule.every().week.do(func)` |

## Workflow

```
┌─────────────────────────────────────────┐
│  Streamlit Dashboard Starts             │
│  (User opens dashboard)                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Background Scheduler Thread Starts     │
│  (Runs independently)                   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Wait for Scheduled Time                │
│  (Every Monday 12:00 AM)                │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  1. Collect Data (Reviews, News,        │
│     Reddit)                             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  2. Send Success/Failure Email          │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  3. Run Sentiment/Trend Monitoring      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  4. Send Alert Emails (if anomalies)    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│  Wait for Next Week...                  │
│  (Repeat)                               │
└─────────────────────────────────────────┘
```

## Installation

```bash
pip install schedule
```

## Usage

### Option 1: Run with Streamlit (Recommended)

The scheduler automatically starts when you run the dashboard:

```bash
streamlit run advanced_dashboard.py
```

Check sidebar for scheduler status and manual trigger button.

### Option 2: Run Standalone

For testing or running without Streamlit:

```bash
python scheduler.py
```

Press Ctrl+C to stop.

## Testing

### Test with 30 Second Interval

Edit `scheduler.py`:

```python
# Comment production schedule
# schedule.every().monday.at("00:00").do(collect_weekly_data)

# Uncomment test schedule
schedule.every(30).seconds.do(test_scheduler)
```

### Manual Trigger via Dashboard

1. Open Streamlit dashboard
2. Check sidebar for "🔄 Automated Scheduler"
3. Click "🔄 Run Data Collection Now"

### Direct Test

```python
from scheduler import collect_weekly_data

# Run immediately
collect_weekly_data()
```

## Email Notifications

The scheduler sends emails for:

1. ✓ **Data Collection Success**
   - Record counts
   - Timestamp
   - Summary

2. ✗ **Data Collection Failure**
   - Error message
   - Troubleshooting info

3. ⚠️ **Monitoring Alerts**
   - Sentiment spikes
   - Trend shifts
   - Pipeline errors

## Monitoring Integration

After data collection, the scheduler automatically runs:

```python
from sentiment_trend_monitor import run_weekly_monitoring

results = run_weekly_monitoring()
```

This detects:
- Sentiment spikes (15%+ change)
- Trend shifts (20%+ change)
- Sends real-time alerts

## Best Practices

### 1. Test Before Production

Always test with short intervals first:
```python
schedule.every(30).seconds.do(test_scheduler)
```

### 2. Monitor Logs

Check console output for scheduler activity:
```
✓ Background scheduler started at 2026-01-23 10:30:00
✓ Reviews collected: 1500
✓ News articles collected: 850
✓ Reddit posts collected: 420
```

### 3. Set Reasonable Intervals

- **Too frequent**: Wastes resources, hits API limits
- **Too infrequent**: Data becomes stale

Recommended: **Weekly** for this project

### 4. Handle Errors Gracefully

Scheduler includes try-except blocks and sends error notifications

### 5. Use daemon Threads

Always set `daemon=True` so threads don't prevent app shutdown

## Troubleshooting

### Scheduler Not Running

**Check:**
- Is `streamlit_scheduler.py` imported in dashboard?
- Check sidebar status indicator
- Look for "Background scheduler started" in console

**Fix:**
```python
# In advanced_dashboard.py
import streamlit_scheduler  # Add this line
```

### Emails Not Sending

**Check:**
- `.env` file configured correctly
- Email credentials valid
- Internet connection active

**Test:**
```python
from notification import send_mail
send_mail("Test", "Test Subject")
```

### Schedule Not Triggering

**Check:**
- Time format correct: `"HH:MM"` (24-hour)
- Streamlit app still running
- Thread still alive

**Verify:**
```python
# Add debug print in scheduler.py
print(f"Next run: {schedule.next_run()}")
```

### Dashboard Freezing

**Cause:** Scheduler running in main thread instead of background

**Fix:** Ensure using `daemon=True`:
```python
threading.Thread(target=run_scheduler, daemon=True).start()
```

## Advanced: Windows Task Scheduler

For production without Streamlit:

### Create Batch File `run_scheduler.bat`

```batch
@echo off
cd "d:\Infosys springboard\AIMarket"
call .\env\Scripts\activate
python scheduler.py
```

### Schedule in Windows

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly (Monday, 12:00 AM)
4. Action: Start Program → `run_scheduler.bat`
5. Settings: Run whether user is logged in or not

## Schedule Examples

### Multiple Jobs

```python
# Weekly data collection
schedule.every().monday.at("00:00").do(collect_weekly_data)

# Daily monitoring
schedule.every().day.at("09:00").do(run_monitoring)

# Hourly health check
schedule.every().hour.do(check_system_health)
```

### Conditional Execution

```python
def collect_if_weekday():
    if datetime.now().weekday() < 5:  # Monday=0, Friday=4
        collect_weekly_data()

schedule.every().day.at("09:00").do(collect_if_weekday)
```

### Clear Schedule

```python
# Clear all jobs
schedule.clear()

# Clear specific job
schedule.clear('collect_weekly_data')
```

## Next Steps

- [ ] Implement actual data collection APIs
- [ ] Add data validation after collection
- [ ] Create daily digest reports
- [ ] Add Slack integration
- [ ] Set up database for historical tracking
- [ ] Create admin dashboard for scheduler control
