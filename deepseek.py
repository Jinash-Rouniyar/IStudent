# Python script for Ollama interaction
import requests
import json

class OllamaClient:
    def __init__(self, base_url="http://10.49.34.10:11434"):
        self.base_url = base_url

    def generate(self, prompt, model="deepseek-r1:32b-qwen-distill-q8_0", stream=False):
        """
        Generate a response from the model.
        
        Args:
            prompt (str): The input prompt
            model (str): Model name to use
            stream (bool): Whether to stream the response
        """
        if stream:
            return self._generate_streaming(prompt, model)
        else:
            return self._generate_non_streaming(prompt, model)

    def _generate_non_streaming(self, prompt, model):
        """Handle non-streaming response."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url, json=payload)
        return response.json()

    def _generate_streaming(self, prompt, model):
        """Handle streaming response."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        response = requests.post(url, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                yield json.loads(line)

    def list_models(self):
        """List available models."""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        return response.json()

# Example usage
def main():
    client = OllamaClient()
    
    # List available models
    print("Available models:")
    models = client.list_models()
    print(json.dumps(models, indent=2))
    
    # Generate response (non-streaming)
    print("\nGenerating response:")
    response = client.generate("What is the capital of France?")
    print(json.dumps(response, indent=2))
    
    # Generate response (streaming)
    print("\nStreaming response:")
    for chunk in client.generate("Tell me a short story.", stream=True):
        if "response" in chunk:
            print(chunk["response"], end="")

if __name__ == "__main__":
    main()
