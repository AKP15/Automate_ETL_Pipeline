import time
from apscheduler.schedulers.background import BackgroundScheduler
from collector import city_wealther_collector

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(city_wealther_collector, 'interval', minutes=20)
    scheduler.start()
    print("Scheduler started. Collecting weather data every 5 minutes.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()
                                                                                                                                

                                                    
