import subprocess

def get_response(prompt):
    print("🤖 Sending to model:", prompt[:100])  # For debug

    result = subprocess.run(
        "ollama run mistral",
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True  # Important for Windows
    )

    output = result.stdout.decode("utf-8").strip()
    error = result.stderr.decode("utf-8").strip()

    print("🟢 Output:", output)
    print("🔴 Errors:", error)

    return output or "⚠️ No response from model"
