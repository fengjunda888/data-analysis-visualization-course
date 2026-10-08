from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "01_rfm_model.py",
    "02_funnel_analysis.py",
    "03_cohort_retention.py",
    "04_descriptive_statistics.py",
    "05_user_profile.py",
    "06_time_series_decomposition.py",
]


def main() -> None:
    scripts_dir = ROOT / "business_data_analysis"
    sys.path.insert(0, str(scripts_dir))
    for script in SCRIPTS:
        print(f"Running {script}...")
        runpy.run_path(str(scripts_dir / script), run_name="__main__")
    print("All business data analysis experiments completed.")


if __name__ == "__main__":
    main()
