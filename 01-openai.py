import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "¿Puedes explicar qué es una API en términos sencillos?"}
  ]
)

print(response.choices[0].message.content)