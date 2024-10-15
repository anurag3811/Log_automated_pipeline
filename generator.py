import logging
import json
from datetime import datetime
import random
import time
from threading import Timer
from pytz import UTC

# Create a custom logging handler
class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        log_entry = self.format(record)
        with open(self.baseFilename, 'a') as f:
            f.write(log_entry + '\n')

# # Set up the logger
logger = logging.getLogger('jsonLogger')
logger.setLevel(logging.DEBUG)

# # Create a file handler that logs messages in JSON format
json_handler = JsonFileHandler('json_logs.log')
json_handler.setLevel(logging.DEBUG)

# # Create a custom formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'Username': record.username,
            'Log_id': record.log_id,
            'Timestamp': datetime.now(UTC).isoformat(),
            'Values': record.values
        }
        return json.dumps(log_record)

json_handler.setFormatter(JsonFormatter())
logger.addHandler(json_handler)

# Log messages with the fixed JSON structure
def log_calculation(username, log_id, age, income, deductions, old_tax, new_tax):
    logger.info('', extra={
        'username': username,
        'log_id': log_id,
        'values': {
            'Type': 'calculation',
            'age': age,
            'income': income,
            'deductions': deductions,
            'old regime tax': old_tax,
            'new regime tax': new_tax
        }
    })

def log_appointment(username, log_id, age, income, deductions, old_tax, new_tax, tax_advisor_id):
    logger.info('', extra={
        'username': username,
        'log_id': log_id,
        'values': {
            'Type': 'appointment',
            'age': age,
            'income': income,
            'deductions': deductions,
            'old regime tax': old_tax,
            'new regime tax': new_tax,
            'tax_advisor_id': tax_advisor_id
        }
    })

# Function to generate random values and log them
def generate_logs():
    username = "Sanchari"
    log_id = random.randint(1, 1000)
    age = random.randint(20, 60)
    income = random.randint(30000, 100000)
    deductions = random.randint(1000, 20000)
    old_tax = random.randint(2000, 10000)
    new_tax = random.randint(1500, 9000)
    
    if random.choice([True, False]):
        log_calculation(username, log_id, age, income, deductions, old_tax, new_tax)
    else:
        tax_advisor_id = f"advisor{random.randint(1, 100)}"
        log_appointment(username, log_id, age, income, deductions, old_tax, new_tax, tax_advisor_id)

# Scheduler to generate logs every 10 seconds
def scheduler():
    generate_logs()
    Timer(10.0, scheduler).start()

# Start the scheduler
scheduler()

