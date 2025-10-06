import os
from openai import OpenAI

def get_client():
    base_url = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    return OpenAI(api_key=api_key, base_url=base_url)

if __name__ == "__main__":
    client = get_client()
    response = client.responses.create(
        model="gpt-4o",
        input="This is a test.",
    )

    print(response.model_dump_json(indent=2))