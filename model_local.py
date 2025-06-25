import subprocess

def ask_local(prompt):
    result = subprocess.run(
        ["C:\\Users\\vnkt5\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()