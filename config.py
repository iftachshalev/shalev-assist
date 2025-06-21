import os

# Keep your existing constants here:
MODEL_NAME = "gpt-3.5-turbo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dynamically build playground path relative to config.py file
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYGROUND_PATH = os.path.join(ROOT_DIR, "playground")
