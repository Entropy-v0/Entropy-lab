from pathlib import Path

# Project Root (Relative to this config.py file)
# Assuming config.py is in the root of the project:
BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# DATA PATHS
# ==========================================
DATA_DIR = BASE_DIR / "data"

# Raw Data (Input)
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_NETFLIX_FILE = RAW_DATA_DIR / "netflix1.csv"

# Processed Data (Output)
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NETFLIX_CLEANED_FILE = PROCESSED_DATA_DIR / "netflix_cleaned.parquet"

# ==========================================
# OUTPUTS
# ==========================================
# Directory for saving plots/images
FIGURES_DIR = BASE_DIR / "01_Data_Intelligence/reports/figures"

# ==========================================
# SETUP
# ==========================================
# Ensure critical directories exist
def setup_directories():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    setup_directories()
    print(f"Project Configuration Loaded.")
    print(f"Base Directory: {BASE_DIR}")
    print(f"Raw Data File: {RAW_NETFLIX_FILE}")
