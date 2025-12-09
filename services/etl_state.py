import datetime

last_etl_run = None

def update_last_run():
    global last_etl_run
    last_etl_run = datetime.datetime.now()

def get_last_etl_run():
    return last_etl_run