"""Naive Bayes kecil sebagai baseline ML yang bisa dilatih tanpa akun/API."""

from collections import Counter
from math import exp, log
from pathlib import Path
import re

TOKEN_PATTERN = re.compile(r"[\w]+", re.UNICODE)
LABELS = ("positive", "negative")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.casefold())


def load_training(path: Path = Path(__file__).with_name("training.tsv")) -> list[tuple[str, str]]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines()[1:], 2):
        if not line.strip():
            continue
        if "\t" not in line:
            raise ValueError(f"Baris {number} harus berisi label dan teks dipisahkan tab")
        label, text = line.split("\t", 1)
        if label not in LABELS or not text.strip():
            raise ValueError(f"Baris {number} membutuhkan label positive/negative dan teks")
        rows.append((label, text))
    if {label for label, _ in rows} != set(LABELS):
        raise ValueError("Data latihan harus memuat label positive dan negative")
    return rows


def decide(positive_probability: float, threshold: float) -> str:
    """Aturan keputusan bisnis dipisahkan dari probabilitas model."""
    if not 0 <= positive_probability <= 1 or not 0 <= threshold <= 1:
        raise ValueError("Probabilitas dan ambang harus berada di antara 0 dan 1")
    return "positive" if positive_probability >= threshold else "negative"


class NaiveBayes:
    def __init__(self, samples: list[tuple[str, str]]):
        self.document_counts = Counter(label for label, _ in samples)
        self.word_counts = {label: Counter() for label in LABELS}
        for label, text in samples:
            self.word_counts[label].update(tokenize(text))
        self.vocabulary = set().union(*(set(words) for words in self.word_counts.values()))
        self.total_words = {label: sum(self.word_counts[label].values()) for label in LABELS}
        self.total_documents = len(samples)

    def predict_proba(self, text: str) -> dict[str, float]:
        tokens = tokenize(text)
        if not tokens:
            return {label: 0.5 for label in LABELS}
        log_scores = {}
        for label in LABELS:
            score = log(self.document_counts[label] / self.total_documents)
            denominator = self.total_words[label] + len(self.vocabulary)
            for token in tokens:
                score += log((self.word_counts[label][token] + 1) / denominator)
            log_scores[label] = score
        max_score = max(log_scores.values())
        scaled = {label: exp(score - max_score) for label, score in log_scores.items()}
        total = sum(scaled.values())
        return {label: value / total for label, value in scaled.items()}


SAMPLES = load_training()
MODEL = NaiveBayes(SAMPLES)


if __name__ == "__main__":
    assert MODEL.predict_proba("cepat dan membantu")["positive"] > 0.5
    assert MODEL.predict_proba("lambat dan buruk")["negative"] > 0.5
    print("Baseline terlatih; sanity check lulus.")
