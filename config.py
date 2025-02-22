import os

# API Configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Crawler Constants
MAX_PAGES = 10
CONCURRENCY_LEVEL = 3
DEFAULT_CSS_SELECTOR = "div.storyline-detail__summary"

# Model Configurations
GROQ_MODEL = "qwen-2.5-32b"
GEMINI_MODEL = "gemini-2.0-flash-exp"