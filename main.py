import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from scheduler.jobs import fetch_and_push_job, cleanup_job
from storage import dedup
from config import settings

def main():
    # Initialize DB on startup
    dedup.init_db(settings.DB_PATH)
    
    scheduler = BlockingScheduler()
    
    # Schedule fetch jobs: 使用配置的推送时间
    push_hours = settings.PUSH_HOURS
    scheduler.add_job(fetch_and_push_job, CronTrigger(hour=push_hours, minute=0))
    
    # Schedule cleanup job: Weekly on Sunday at 02:00
    scheduler.add_job(cleanup_job, CronTrigger(day_of_week='sun', hour=2, minute=0))
    
    # 格式化显示时间
    hours_display = ', '.join([f'{int(h):02d}:00' for h in push_hours.split(',')])
    print("🚀 aiBox Service Started...")
    print(f"📅 Fetch Schedule: Daily at {hours_display}")
    print(f"🧹 Cleanup Schedule: Sundays at 02:00 (Retain {settings.CLEANUP_DAYS_RETAIN} days)")
    
    # Uncomment to run immediately for testing
    # fetch_and_push_job()
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Service Stopped")

if __name__ == "__main__":
    main()
