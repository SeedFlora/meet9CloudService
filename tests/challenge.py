"""Pemeriksaan kasus moderasi Lab 09; tidak mengunduh model opsional."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import analyze  # noqa: E402
from core import MODEL, SAMPLES, decide, load_training, tokenize  # noqa: E402

checks = 0


def check(label: str, condition: bool) -> None:
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1
    print(f"PASS {label}")


check("data memuat dua label dan 24 contoh", len(SAMPLES) == 24 and {x[0] for x in SAMPLES} == {"positive", "negative"})
check("tokenisasi tidak peka huruf besar", tokenize("LAYANAN Cepat") == ["layanan", "cepat"])
positive = MODEL.predict_proba("layanan ini cepat dan membantu")
negative = MODEL.predict_proba("aplikasi sering gagal dibuka")
check("probabilitas positif terukur", positive["positive"] > 0.5)
check("probabilitas negatif terukur", negative["negative"] > 0.5)
check("ambang bisnis mengubah keputusan tanpa melatih ulang", decide(positive["positive"], 0.9) == "negative")
scores, details, tokens = analyze("layanan ini cepat dan membantu", "Baseline lokal", 0.9)
check("UI mengembalikan keputusan dan token", details["decision"] == "negative" and len(tokens) > 0 and scores == positive)
_, empty, _ = analyze("  ", "Baseline lokal", 0.5)
check("input kosong diberi pesan", "error" in empty)
_, invalid, _ = analyze("uji", "model tak dikenal", 0.5)
check("model tak dikenal ditolak", "error" in invalid)
check("data TSV dapat dimuat lagi", load_training(ROOT / "training.tsv") == SAMPLES)
print(f"challenge: {checks} PASS, 0 FAIL")
