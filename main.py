import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from logging.config import dictConfig
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Load configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "your_database_name")

logger = logging.getLogger(__name__)

# Connect to your MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Define the collections for each log level
collections = {
    "info": db.info_logs,
    "error": db.error_logs,
    "success": db.success_logs,
}

app = FastAPI()

# Pydantic model for the log entry
class LogEntry(BaseModel):
    level: str
    log_string: str
    timestamp: str
    metadata: dict

# Helper function to convert MongoDB documents to Pydantic models
def log_entry_from_mongo(log):
    return LogEntry(
        level=log["level"],
        log_string=log["log_string"],
        timestamp=log["timestamp"],
        metadata=log["metadata"]
    )

# Endpoint to search logs by level
@app.get("/logs/level/{level}", response_model=List[LogEntry])
def get_logs_by_level(level: str):
    try:
        logger.info(f"Fetching logs with level: {level}")
        collection = collections.get(level.lower())
        if not collection:
            raise HTTPException(status_code=400, detail=f"Invalid log level: {level}")
        logs_cursor = collection.find()
        logs = [log_entry_from_mongo(log) for log in logs_cursor]
        logger.info(f"Results: {json.dumps([log.dict() for log in logs], indent=2)}")
        return logs
    except Exception as e:
        logger.error(f"Error fetching logs by level: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to search logs by log_string
@app.get("/logs/log_string", response_model=List[LogEntry])
def get_logs_by_log_string(log_string: str):
    try:
        logger.info(f"Fetching logs with log_string: {log_string}")
        logs = []
        for collection in collections.values():
            logs_cursor = collection.find({"log_string": log_string})
            logs.extend([log_entry_from_mongo(log) for log in logs_cursor])
        logger.info(f"Results: {json.dumps([log.dict() for log in logs], indent=2)}")
        return logs
    except Exception as e:
        logger.error(f"Error fetching logs by log_string: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to search logs by timestamp
@app.get("/logs/timestamp", response_model=List[LogEntry])
def get_logs_by_timestamp(timestamp: str):
    try:
        logger.info(f"Fetching logs with timestamp: {timestamp}")
        logs = []
        for collection in collections.values():
            logs_cursor = collection.find({"timestamp": timestamp})
            logs.extend([log_entry_from_mongo(log) for log in logs_cursor])
        logger.info(f"Results: {json.dumps([log.dict() for log in logs], indent=2)}")
        return logs
    except Exception as e:
        logger.error(f"Error fetching logs by timestamp: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to search logs by metadata.source
@app.get("/logs/metadata/source", response_model=List[LogEntry])
def get_logs_by_metadata_source(source: str):
    try:
        logger.info(f"Fetching logs with metadata.source: {source}")
        logs = []
        for collection in collections.values():
            logs_cursor = collection.find({"metadata.source": source})
            logs.extend([log_entry_from_mongo(log) for log in logs_cursor])
        logger.info(f"Results: {json.dumps([log.dict() for log in logs], indent=2)}")
        return logs
    except Exception as e:
        logger.error(f"Error fetching logs by metadata.source: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to insert multiple log entries
@app.post("/logs", response_model=List[LogEntry])
def create_logs(log_entries: List[LogEntry]):
    try:
        inserted_logs = []
        for log_entry in log_entries:
            logger.info(f"Inserting log entry: {log_entry}")
            # Determine the collection based on the log level
            collection = collections.get(log_entry.level.lower())
            if not collection:
                raise HTTPException(status_code=400, detail=f"Invalid log level: {log_entry.level}")

            # Insert the new log entry into the appropriate collection
            result = collection.insert_one(log_entry.dict())
            if result.acknowledged:
                inserted_logs.append(log_entry)
            else:
                logger.error(f"Failed to insert log entry: {log_entry}")

        logger.info(f"Inserted logs: {json.dumps([log.dict() for log in inserted_logs], indent=2)}")
        return inserted_logs
    except Exception as e:
        logger.error(f"Error inserting log entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)