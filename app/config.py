import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# .envファイル読み込み
load_dotenv()


@dataclass
class HuggingFaceConfig:
    """HuggingFace設定"""

    # 感情分析モデル
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    # 多言語モデル（日本語対応）
    multilingual_model: str = "nlptown/bert-base-multilingual-uncased-sentiment"
    # HuggingFace APIキー（オプション：制限回避用）
    api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
    # キャッシュディレクトリ
    cache_dir: str = "./models_cache"


@dataclass
class AWSConfig:
    """AWS設定"""

    # リージョン
    region: str = os.getenv("AWS_REGION", "ap-northeast-1")
    # アクセスキー
    access_key: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Bedrock設定
    bedrock_region: str = os.getenv("BEDROCK_REGION", "us-east-1")
    nova_model_id: str = "amazon.nova-lite-v1:0"  # または nova-pro-v1:0

    # DynamoDB設定
    dynamodb_table: str = os.getenv("DYNAMODB_TABLE", "social-listening-results")

    # S3設定
    s3_bucket: str = os.getenv("S3_BUCKET", "social-listening-data")


@dataclass
class TwitterConfig:
    """Twitter API設定"""

    api_key: Optional[str] = os.getenv("TWITTER_API_KEY")
    api_secret: Optional[str] = os.getenv("TWITTER_API_SECRET")
    access_token: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")


@dataclass
class AppConfig:
    """アプリケーション設定"""

    # Gradio設定
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "7860"))
    share: bool = os.getenv("GRADIO_SHARE", "false").lower() == "true"

    # ログ設定
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # 開発/本番モード
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")


# 設定インスタンス作成
huggingface_config = HuggingFaceConfig()
aws_config = AWSConfig()
twitter_config = TwitterConfig()
app_config = AppConfig()


def get_model_config(model_type: str = "sentiment"):
    """モデル設定を取得"""
    model_configs = {
        "sentiment": huggingface_config.sentiment_model,
        "multilingual": huggingface_config.multilingual_model,
    }
    return model_configs.get(model_type, huggingface_config.sentiment_model)


def validate_config():
    """設定検証"""
    errors = []

    # AWS設定チェック
    if aws_config.access_key is None:
        errors.append("AWS_ACCESS_KEY_ID not set")

    # Twitter設定チェック（オプション）
    if twitter_config.bearer_token is None:
        print("Warning: TWITTER_BEARER_TOKEN not set - Twitter機能は無効")

    if errors:
        raise ValueError(f"設定エラー: {', '.join(errors)}")

    return True


# アプリ起動時の設定表示
def print_config():
    """設定表示（デバッグ用）"""
    if app_config.debug:
        print("=== アプリケーション設定 ===")
        print(f"Environment: {app_config.environment}")
        print(f"Host: {app_config.host}:{app_config.port}")
        print(f"HuggingFace Model: {huggingface_config.sentiment_model}")
        print(f"AWS Region: {aws_config.region}")
        print(f"Bedrock Model: {aws_config.nova_model_id}")
        print("=" * 30)
