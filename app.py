"""Gradio UI: baseline lokal dan DistilBERT opsional."""

import gradio as gr

from core import MODEL, SAMPLES, decide, tokenize

_transformer = None


def analyze(text: str, mode: str, threshold: float):
    global _transformer
    if not text.strip():
        return {}, {"error": "Masukkan teks terlebih dahulu."}, []
    if mode not in {"Baseline lokal", "DistilBERT English"}:
        return {}, {"error": "Pilihan model tidak dikenal."}, []

    if mode == "DistilBERT English":
        try:
            if _transformer is None:
                from transformers import pipeline
                _transformer = pipeline(
                    "sentiment-analysis",
                    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
                )
            result = _transformer(text)[0]
            positive = float(result["score"]) if result["label"] == "POSITIVE" else 1 - float(result["score"])
            scores = {"positive": positive, "negative": 1 - positive}
        except ImportError:
            return {}, {"error": "Install requirements-transformer.txt untuk mode DistilBERT."}, []
        except (OSError, RuntimeError) as exc:
            return {}, {"error": f"Model opsional belum dapat dimuat: {type(exc).__name__}. Periksa internet/cache model."}, []
    else:
        scores = MODEL.predict_proba(text)

    decision = decide(scores["positive"], threshold)
    detail = {
        "model": mode,
        "decision": decision,
        "positive_probability": round(scores["positive"], 4),
        "threshold": threshold,
        "training_samples_baseline": len(SAMPLES),
        "note": "Baseline kelas dilatih dengan data kecil; angka probabilitas bukan jaminan akurasi.",
    }
    words = [[word, MODEL.word_counts["positive"][word], MODEL.word_counts["negative"][word]] for word in tokenize(text)[:20]]
    return scores, detail, words


with gr.Blocks(title="Cloud Notes Sentiment Lab") as demo:
    gr.Markdown("# Cloud Notes — Sentiment Demo\nBandingkan baseline Naive Bayes lokal dengan DistilBERT English opsional.")
    text_input = gr.Textbox(label="Teks", lines=3, placeholder="Contoh: layanan ini cepat dan membantu")
    mode = gr.Radio(["Baseline lokal", "DistilBERT English"], value="Baseline lokal", label="Model")
    threshold = gr.Slider(0.1, 0.9, value=0.5, step=0.05, label="Ambang positive")
    run_button = gr.Button("Analisis")
    labels = gr.Label(label="Probabilitas")
    details = gr.JSON(label="Detail")
    tokens = gr.Dataframe(headers=["Token", "Frekuensi +", "Frekuensi -"], label="Token yang terlihat baseline")
    gr.Examples(["layanan ini cepat dan membantu", "aplikasi sering gagal dibuka", "this service is fast"], inputs=text_input)
    run_button.click(analyze, inputs=[text_input, mode, threshold], outputs=[labels, details, tokens])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
