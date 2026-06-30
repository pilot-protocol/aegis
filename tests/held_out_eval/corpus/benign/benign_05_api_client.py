# LABEL: BENIGN
# Anthropic API client — mentions ANTHROPIC_API_KEY and makes HTTP calls (legitimate SDK use)
import os
import anthropic

def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY in your environment")
    return anthropic.Anthropic(api_key=api_key)

def summarize(text: str) -> str:
    client = get_client()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Summarize: {text}"}]
    )
    return response.content[0].text

if __name__ == "__main__":
    sample = "AEGIS is a local security daemon for AI agents."
    print(summarize(sample))
