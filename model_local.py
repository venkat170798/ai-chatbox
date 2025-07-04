import subprocess

def ask_local(prompt):
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()