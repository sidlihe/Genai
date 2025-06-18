from langchain.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
import warnings
warnings.filterwarnings("ignore")

# Initialize Ollama LLM (make sure Ollama is running locally)
llm = Ollama(model="mistral")

# First prompt: Summarize text
summary_prompt = PromptTemplate(
    input_variables=["input_text"],
    template="Summarize the following text:\n{input_text}"
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")

# Second prompt: Generate a title
title_prompt = PromptTemplate(
    input_variables=["summary"],
    template="Write a short, catchy title for this summary:\n{summary}"
)
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key="title")

# Sequential chain: summary -> title
sequential_chain = SequentialChain(
    chains=[summary_chain, title_chain],
    input_variables=["input_text"],
    output_variables=["summary", "title"]
)

# Example usage
input_text = "the domain language of maharashtra is?"
result = sequential_chain({"input_text": input_text})

print("Summary:", result["summary"])
print("Title:", result["title"])