import logging  # Python’s built-in logging module for tracking events
import os       # For handling filesystem paths
from datetime import datetime  # To create timestamped log filenames

# 1️⃣ Create a timestamped log filename
# Example: "10_01_2025_13_30_45.log"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2️⃣ Define the logs directory path
# os.getcwd() gets the current working directory
log_path = os.path.join(os.getcwd(), "logs")

# 3️⃣ Ensure the 'logs' directory exists; create if it doesn't
os.makedirs(log_path, exist_ok=True)

# 4️⃣ Full path for the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# 5️⃣ Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Capture all levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # Format explained:
    # %(asctime)s → Timestamp of the log
    # %(lineno)d   → Line number where logging call was made
    # %(name)s    → Logger name/module
    # %(levelname)s → Log level (DEBUG/INFO/ERROR)
    # %(message)s  → Actual log message
    handlers=[
        logging.FileHandler(LOG_FILEPATH),  # Write logs to file
        logging.StreamHandler()             # Also output logs to console
    ]
)

# ✅ Summary:
# - All logs go to both console and a timestamped file in /logs/
# - Format provides detailed info (time, line, module, level, message)
# - Directory is created automatically if missing
