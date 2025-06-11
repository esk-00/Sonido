# import logging
# from datetime import datetime

# import gradio as gr
# import pandas as pd
# import plotly.express as px

# # from config import (app_config, get_model_config, huggingface_config,
# #                     print_config, validate_config)
# # from transformers import pipeline

# # ロギング設定
# logging.basicConfig(level=getattr(logging, app_config.log_level))
# logger = logging.getLogger(__name__)

# # グローバル変数
# sentiment_pipeline = None
# analysis_history = []


# def initialize_models():
#     """モデルの初期化"""
#     global sentiment_pipeline

#     try:
#         logger.info("HuggingFaceモデルを読み込んでいます...")

#         # 感情分析パイプライン初期化
#         model_name = get_model_config("sentiment")
#         sentiment_pipeline = pipeline(
#             "sentiment-analysis",
#             model=model_name,
#             cache_dir=huggingface_config.cache_dir,
#         )

#         logger.info(f"モデル読み込み完了: {model_name}")
#         return True

#     except Exception as e:
#         logger.error(f"モデル初期化エラー: {str(e)}")
#         return False


# def analyze_sentiment(text):
#     """感情分析メイン関数"""
#     if not text or not text.strip():
#         return {
#             "error": "テキストを入力してください",
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }

#     try:
#         # HuggingFace推論
#         result = sentiment_pipeline(text)

#         # 結果を履歴に保存
#         analysis_result = {
#             "text": text[:100] + "..." if len(text) > 100 else text,
#             "sentiment": result[0]["label"],
#             "confidence": round(result[0]["score"], 3),
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }

#         analysis_history.append(analysis_result)

#         # 履歴は最新100件まで保持
#         if len(analysis_history) > 100:
#             analysis_history.pop(0)

#         logger.info(f"感情分析完了: {result[0]['label']} ({result[0]['score']:.3f})")

#         return analysis_result

#     except Exception as e:
#         logger.error(f"感情分析エラー: {str(e)}")
#         return {
#             "error": f"分析エラー: {str(e)}",
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }


# def create_dashboard():
#     """ダッシュボード作成"""
#     if not analysis_history:
#         # サンプルデータ
#         data = {"sentiment": ["POSITIVE", "NEGATIVE", "NEUTRAL"],
#                   "count": [65, 20, 15]}
#     else:
#         # 実際の分析履歴から統計作成
#         sentiments = [item["sentiment"] for item in analysis_history]
#         sentiment_counts = pd.Series(sentiments).value_counts()

#         data = {
#             "sentiment": sentiment_counts.index.tolist(),
#             "count": sentiment_counts.values.tolist(),
#         }

#     df = pd.DataFrame(data)

#     fig = px.bar(
#         df,
#         x="sentiment",
#         y="count",
#         title=f"感情分析結果統計 (分析数: {len(analysis_history)})",
#         color="sentiment",
#         color_discrete_map={
#             "POSITIVE": "#2E8B57",
#             "NEGATIVE": "#DC143C",
#             "NEUTRAL": "#4682B4",
#         },
#     )

#     fig.update_layout(xaxis_title="感情", yaxis_title="件数", showlegend=False)

#     return fig


# def get_recent_history():
#     """最近の分析履歴を取得"""
#     if not analysis_history:
#         return "まだ分析履歴がありません"

#     recent = analysis_history[-10:]  # 最新10件
#     history_text = "=== 最近の分析結果 ===\n\n"

#     for item in reversed(recent):
#         history_text += f"📝 {item['text']}\n"
#         history_text += f"💭 {item['sentiment']} (信頼度: {item['confidence']})\n"
#         history_text += f"🕒 {item['timestamp']}\n\n"

#     return history_text


# def create_gradio_interface():
#     """Gradio UI作成"""

#     # カスタムCSS
#     custom_css = """
#     .gradio-container {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }
#     .gr-button-primary {
#         background: linear-gradient(45deg, #2E8B57, #228B22) !important;
#     }
#     """

#     with gr.Blocks(
#         title="ソーシャルリスニング", css=custom_css, theme=gr.themes.Soft()
#     ) as demo:

#         gr.Markdown(
#             """
#         # 🎯 ソーシャルリスニング ダッシュボード
#         HuggingFace + AWS Nova による高精度感情分析システム
#         """
#         )

#         with gr.Tab("🔍 感情分析"):
#             with gr.Row():
#                 with gr.Column(scale=2):
#                     text_input = gr.Textbox(
#                         label="📝 分析対象テキスト",
#                         placeholder="分析したいテキストを入力してください...\n例: 今日は素晴らしい天気ですね！",
#                         lines=5,
#                         max_lines=10,
#                     )

#                     with gr.Row():
#                         analyze_btn = gr.Button(
#                             "🚀 分析開始", variant="primary", scale=2
#                         )
#                         clear_btn = gr.Button("🗑️ クリア", scale=1)

#                 with gr.Column(scale=2):
#                     result_output = gr.JSON(label="📊 分析結果", show_label=True)

#         with gr.Tab("📈 ダッシュボード"):
#             with gr.Row():
#                 with gr.Column():
#                     plot_output = gr.Plot(label="📊 感情分析統計")
#                     refresh_btn = gr.Button("🔄 更新", variant="secondary")

#                 with gr.Column():
#                     history_output = gr.Textbox(
#                         label="📜 分析履歴", lines=15, max_lines=20, interactive=False
#                     )
#                     history_btn = gr.Button("📋 履歴更新", variant="secondary")

#         with gr.Tab("⚙️ 設定情報"):
#             gr.Markdown(
#                 f"""
#             ### 🔧 現在の設定
#             - **環境**: {app_config.environment}
#             - **モデル**: {get_model_config('sentiment')}
#             - **ホスト**: {app_config.host}:{app_config.port}
#             - **デバッグモード**: {app_config.debug}
#             - **分析履歴**: {len(analysis_history)} 件

#             ### 📝 使用方法
#             1. **感情分析タブ**: テキストを入力して感情を分析
#             2. **ダッシュボードタブ**: 分析結果の統計を表示
#             3. **設定情報タブ**: システム情報を確認
#             """
#             )

#         # イベント設定
#         analyze_btn.click(
#             fn=analyze_sentiment, inputs=text_input, outputs=result_output
#         )

#         clear_btn.click(fn=lambda: "", outputs=text_input)

#         refresh_btn.click(fn=create_dashboard, outputs=plot_output)

#         history_btn.click(fn=get_recent_history, outputs=history_output)

#         # 起動時の初期表示
#         demo.load(fn=create_dashboard, outputs=plot_output)

#         demo.load(fn=get_recent_history, outputs=history_output)

#     return demo


# def main():
#     """メイン関数"""
#     try:
#         # 設定検証
#         print_config()
#         # validate_config()  # AWS設定が不完全な場合はコメントアウト

#         # モデル初期化
#         if not initialize_models():
#             logger.error("モデル初期化に失敗しました")
#             return

#         # Gradio UI起動
#         demo = create_gradio_interface()

#         logger.info(
#             f"アプリケーションを起動しています: http://{app_config.host}:{app_config.port}"
#         )

#         demo.launch(
#             server_name=app_config.host,
#             server_port=app_config.port,
#             share=app_config.share,
#             show_error=app_config.debug,
#         )

#     except Exception as e:
#         logger.error(f"アプリケーション起動エラー: {str(e)}")
#         raise


# if __name__ == "__main__":
#     main()
