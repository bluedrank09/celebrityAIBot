# importing libraries
import os # used to get api key
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, GPTListIndex, LLMPredictor, PromptHelper


openai_api_key = os.environ.get('OPENAI_API_KEY')

def construct_index(directory_path): # contructing nodes and grouping them to use later for KNN. we need drectry pat to get to te pdfs
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents)

    index.save_to_disk("index.json") 

    return(index)

def chatBot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text, response_mode = 'compact')
    
    return(response.response)

index = construct_index("docs")
