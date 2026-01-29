"""
Background Scheduler for Streamlit Dashboard
---------------------------------------------
Runs weekly data collection in background while dashboard is active
"""

import streamlit as st
import threading
import schedule
import time
from datetime import datetime
from scheduler import collect_weekly_data, test_scheduler


def run_background_scheduler():
    """
    Scheduler running in background thread
    Doesn't block Streamlit app
    """
    # Schedule weekly data collection every Monday at midnight
    schedule.every().monday.at("00:00").do(collect_weekly_data)
    
    # For testing: run every 5 minutes
    # schedule.every(5).minutes.do(collect_weekly_data)
    
    # For testing: run every 30 seconds
    # schedule.every(30).seconds.do(test_scheduler)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


# Initialize scheduler in session state
if "scheduler_started" not in st.session_state:
    st.session_state.scheduler_started = False

# Start scheduler only once
if not st.session_state.scheduler_started:
    # Start background thread
    scheduler_thread = threading.Thread(
        target=run_background_scheduler,
        daemon=True  # Thread dies when main program exits
    )
    scheduler_thread.start()
    
    st.session_state.scheduler_started = True
    st.session_state.scheduler_start_time = datetime.now()
    
    print(f"✓ Background scheduler started at {st.session_state.scheduler_start_time}")


# Display scheduler status in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔄 Automated Scheduler")
    
    if st.session_state.scheduler_started:
        st.success("Running")
        st.caption(f"Started: {st.session_state.scheduler_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.caption("Schedule: Every Monday 12:00 AM")
        
        # Manual trigger button
        if st.button("🔄 Run Data Collection Now"):
            with st.spinner("Collecting data..."):
                result = collect_weekly_data()
                if result:
                    st.success("Data collection completed!")
                else:
                    st.error("Data collection failed")
    else:
        st.error("Not running")
