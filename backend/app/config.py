import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"

# Database
DATABASE_URL = os.environ["DATABASE_URL"]

# Models
EXTRACTION_MODEL = os.getenv("EXTRACTION_MODEL", "gpt-5.4-mini")
EXTRACTION_REASONING = os.getenv("EXTRACTION_REASONING", "low")

# Uploads
MAX_UPLOAD_MB = 4
SUPPORTED_TYPES = ("application/pdf", "image/jpeg", "image/png")
UPLOAD_RETENTION_DAYS = 7
MAX_PDF_PAGES = 5

# Visitors
VISITOR_COOKIE = "docket_visitor"
VISITOR_COOKIE_DAYS = 180

# Public demo
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
DAILY_EXTRACTIONS_PER_VISITOR = int(os.getenv("DAILY_EXTRACTIONS_PER_VISITOR", "10"))
DAILY_EXTRACTIONS_TOTAL = int(os.getenv("DAILY_EXTRACTIONS_TOTAL", "150"))