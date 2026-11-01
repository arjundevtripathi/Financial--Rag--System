import os, logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/rag.log", level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger = logging.getLogger("financial_rag")
logger.addHandler(console)
