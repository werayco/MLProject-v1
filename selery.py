import ollama
import time
start = time.time()
client = ollama.Client(host="http://127.0.0.1:11434")

response = client.generate(
    model="gemma3:1b",  
    prompt="tell me a joke"
)
final = time.time() - start
print(f"it takes {final:.1f}secs for inferecing")
print(response['response'])
