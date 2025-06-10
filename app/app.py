from datetime import datetime

import gradio as gr
import pandas as pd
import plotly.express as px
from transformers import pipeline

# HuggingFace感情分析パイプライン
sentiment_pipeline = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


def analyze_sentiment(text):
    """感情分析メイン関数"""
    if not text:
        return "テキストを入力してください"

    # HuggingFace推論
    result = sentiment_pipeline(text)

    return {
        "sentiment": result[0]["label"],
        "confidence": round(result[0]["score"], 3),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def create_dashboard():
    """ダッシュボード作成"""
    # サンプルデータ
    data = {"sentiment": ["POSITIVE", "NEGATIVE", "NEUTRAL"], "count": [65, 20, 15]}
    df = pd.DataFrame(data)

    fig = px.bar(df, x="sentiment", y="count", title="感情分析結果")
    return fig


# Gradio UI定義
with gr.Blocks(title="ソーシャルリスニング") as demo:
    gr.Markdown("# 🎯 ソーシャルリスニング ダッシュボード")

    with gr.Tab("感情分析"):
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="テキスト入力",
                    placeholder="分析したいテキストを入力...",
                    lines=5,
                )
                analyze_btn = gr.Button("分析開始", variant="primary")

            with gr.Column():
                result_output = gr.JSON(label="分析結果")

    with gr.Tab("ダッシュボード"):
        plot_output = gr.Plot(label="感情分析統計")
        refresh_btn = gr.Button("更新")

    # イベント設定
    analyze_btn.click(fn=analyze_sentiment, inputs=text_input, outputs=result_output)

    refresh_btn.click(fn=create_dashboard, outputs=plot_output)

    # 自動でダッシュボード表示
    demo.load(fn=create_dashboard, outputs=plot_output)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Docker対応 # nosec B104
        server_port=7860,
        share=False,  # 本番では False
    )
