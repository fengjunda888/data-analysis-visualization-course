from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "business_data_analysis_outputs"


def setup_output() -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR


def save_plot(fig, filename: str) -> Path:
    output = setup_output() / filename
    fig.tight_layout()
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return output


def set_chinese_font() -> None:
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False


set_chinese_font()

