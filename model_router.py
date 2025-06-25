from config import MODE
from model_local import ask_local

try:
    from model_openai import ask_openai
except:
    ask_openai = lambda x: "OpenAI module not available."

def get_response(prompt):
    if MODE == "openai":
        return ask_openai(prompt)
    return ask_local(prompt)