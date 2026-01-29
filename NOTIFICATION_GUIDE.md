# AI Market Trend Monitoring & Notification System

## Real-Time Notification System

This system provides automated alerts for sentiment spikes, trend shifts, and pipeline issues via Email and Slack.

## Features

### 1. Email Alerts (SMTP)
- Sentiment spike notifications
- Trend shift alerts
- Data ingestion status
- Pipeline error notifications
- Customizable recipients

### 2. Slack Notifications
- Real-time channel alerts
- Color-coded messages (success, warning, error)
- Timestamp tracking
- Bot customization

## Setup Instructions

### Email Setup (Gmail)

1. **Enable 2-Step Verification**
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Search "App Password" in Google Account
   - Create new app password
   - Save the 16-character password

3. **Update Configuration**
   - Edit `notification_config.py`
   - Set `EMAIL_SENDER` to your Gmail
   - Set `EMAIL_PASSWORD` to app password
   - Add recipient emails to `EMAIL_RECEIVERS`

### Slack Setup

1. **Create Slack Workspace**
   - Visit https://slack.com/get-started
   - Create workspace and channel (e.g., #market-alerts)

2. **Add Incoming Webhooks**
   - Click workspace name → Tools → Apps
   - Search "Incoming Webhooks"
   - Add to workspace
   - Select channel
   - Copy webhook URL

3. **Update Configuration**
   - Edit `notification_config.py`
   - Set `SLACK_WEBHOOK_URL` to your webhook
   - Customize bot name and emoji

## File Structure

```
notification_config.py       # Configuration settings
notification_service.py      # Email & Slack service
sentiment_trend_monitor.py   # Monitoring & detection
test_notifications.py        # Test suite
```

## Usage

### Test Notifications

```python
python test_notifications.py
```

### Run Weekly Monitoring

```python
python sentiment_trend_monitor.py
```

### Manual Alert

```python
from notification_service import NotificationService

notifier = NotificationService()
notifier.send_alert(
    alert_type="SENTIMENT_SPIKE_POSITIVE",
    message="Positive sentiment increased by 25% in Mobile category",
    email=True,
    slack=True
)
```

## Alert Types

1. **SENTIMENT_SPIKE_POSITIVE** - Positive sentiment increase
2. **SENTIMENT_SPIKE_NEGATIVE** - Negative sentiment increase  
3. **TREND_SHIFT_UP** - Category demand increasing
4. **TREND_SHIFT_DOWN** - Category demand decreasing
5. **DATA_INGESTION_SUCCESS** - Data fetched successfully
6. **DATA_INGESTION_FAILURE** - Data fetch failed
7. **PIPELINE_ERROR** - Processing error
8. **INCOMPLETE_DATA** - Missing data warning

## Thresholds (Configurable)

- **Sentiment Spike**: 15% change
- **Trend Shift**: 20% change
- **Minimum Data Points**: 10 records

## SMTP Servers Reference

| Provider | SMTP Server | Port |
|----------|-------------|------|
| Gmail | smtp.gmail.com | 587 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 465 |
| Zoho | smtp.zoho.com | 587 |

## Security Best Practices

1. Never commit passwords to Git
2. Use environment variables for credentials
3. Rotate app passwords regularly
4. Limit email recipients to authorized personnel
5. Monitor webhook usage

## Troubleshooting

### Email Not Sending
- Check app password (not regular Gmail password)
- Verify 2-Step Verification is enabled
- Check SMTP server and port
- Verify sender email is correct

### Slack Not Working
- Verify webhook URL is correct
- Check channel permissions
- Ensure Incoming Webhooks app is installed
- Test webhook with curl:
  ```bash
  curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test"}' YOUR_WEBHOOK_URL
  ```

### No Alerts Triggered
- Check data thresholds in `notification_config.py`
- Verify data has sufficient records
- Check date filtering in monitoring script
- Review error logs

## Automation

### Weekly Scheduled Job (Windows)

Create batch file `run_monitoring.bat`:
```batch
cd "d:\Infosys springboard\AIMarket"
.\env\Scripts\activate
python sentiment_trend_monitor.py
```

Schedule using Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Weekly (Monday 9 AM)
4. Action: Start Program → run_monitoring.bat

### Linux/Mac (Cron)

```bash
0 9 * * 1 cd /path/to/project && ./env/bin/python sentiment_trend_monitor.py
```

## Next Steps

- [ ] Add PDF report generation
- [ ] Implement dashboard integration
- [ ] Add historical trend visualization
- [ ] Create mobile app notifications
- [ ] Add Microsoft Teams support
- [ ] Implement alert aggregation (daily digest)
