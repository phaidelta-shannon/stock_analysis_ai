import logging
import sys
from pathlib import Path

# Ensure logs directory exists
Path("logs").mkdir(parents=True, exist_ok=True)

# Set up basic logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),     # Logs are written to this file
        logging.StreamHandler(sys.stdout)        # And also printed to console
    ]
)

logger = logging.getLogger(__name__)