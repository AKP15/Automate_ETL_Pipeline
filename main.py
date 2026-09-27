import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from collect import city_weather_collector  # fixed: was "collector" (module didn't exist)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

if __name__ == "__main__":
        scheduler = BackgroundScheduler()
        scheduler.add_job(city_weather_collector, "interval", minutes=2)
        scheduler.start()
        logging.info("Scheduler started. Collecting weather data every 20 minutes.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
            logging.info("Scheduler stopped.")
