from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
import logging
from datetime import datetime
import random
from pytz import UTC



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://anuragsingh2:Sejal%4022@cluster0.czzze.mongodb.net/Piyush?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def insert_document():
    with app.app_context():
        try:
            document = {
            "Username": "Piyush",
            "Logid": random.randint(1, 1000),
            "Timestamp": datetime.now(UTC),
            "Values": {
                "Type": "alert",
                "Case": "machine faulty",
                "Machine id": random.randint(1, 3),
                "Plantid": random.randint(1, 3)
                }
            }
            result = mongo.db.idk.insert_one(document)
            logging.info(f"Inserted document with _id: {result.inserted_id}")
        except Exception as e:
            logging.error(f"Error inserting scheduled document: {str(e)}")

# Schedule the insert_document function to run every 30 seconds
scheduler.add_job(id='scheduled_insertion', func=insert_document, trigger='interval', seconds=30)

@app.route("/")
def home():
    return "Flask app is running with scheduled document insertion every 30 seconds."

@app.route("/insert")
def manual_insert():
    try:
        result = mongo.db.idk.insert_one({'manual_insert': True, 'timestamp': datetime.now(UTC)})
        logging.info(f"Manually inserted document with _id: {result.inserted_id}")
        return jsonify({"message": "Document inserted successfully", "id": str(result.inserted_id)}), 200
    except Exception as e:
        logging.error(f"Error inserting document: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/count")
def count_documents():
    try:
        count = mongo.db.idk.count_documents({})
        return jsonify({"count": count}), 200
    except Exception as e:
        logging.error(f"Error counting documents: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logging.info("Starting the Flask application with scheduled document insertion...")
    app.run(debug=True, use_reloader=False)  # use_reloader=False to prevent scheduler from running twice