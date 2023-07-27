from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import os
from append import append

directory_path = "./docs/"

def index(inputFileName, outputFileName):
    max_input_size = 4096
    num_outputs = 2048
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo-16k", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(input_files=[directory_path+inputFileName]).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk(outputFileName)

def construct_index(filename):
    if not os.path.exists("./index.json"):
        index(filename, "index.json")
    else:
        os.rename("index.json", "index1.json")
        index(filename, "index2.json")
        append()
        