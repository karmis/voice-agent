import os
import openai

from config import SAMBANOVA_API_KEY

client = openai.OpenAI(
    api_key=SAMBANOVA_API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="DeepSeek-V3-0324",
    messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Hello"}],
    temperature=0.1,
    top_p=0.1
)

print(response.choices[0].message.content)