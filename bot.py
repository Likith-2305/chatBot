from gpt_index import GPTSimpleVectorIndex
import os
import openai
from config import openAiSecrets
key = openAiSecrets()
os.environ["OPENAI_API_KEY"] = key
openai.api_key = key
def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode="default")
    return response.response
