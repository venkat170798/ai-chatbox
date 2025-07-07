# model_router.py

from config import MODE

if MODE == "openai":
    from model_openai import ask_openai as get_response
elif MODE == "ollama":
    from model_local import ask_local as get_response
else:
    raise ValueError("Invalid MODE in config.py. Use 'openai' or 'ollama'.")
