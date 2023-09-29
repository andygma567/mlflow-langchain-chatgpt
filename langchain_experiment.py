"""Markdown gradio experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N8Kgpl3tlggmOTGtsqxR0x--oHW3i91y

When using conda I need to use `which` to be sure that I'm using the 
correct python and pip for installs. 

It helps to use the options python and pip when creating a new conda env
with the conda create command. 

I think the mlflow ui CLI command also works in the conda env but I may
need to be careful in the future about which mlflow I'm using...
"""
# Set the API key - if this key gets committed to a gitrepo then it gets
# disabled
import os
import textwrap

from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import TokenTextSplitter
from pyngrok import ngrok

import mlflow
import pandas as pd

# Set the API key - if this key gets committed to a gitrepo then it gets
# disabled
NGROK_AUTH_TOKEN = ""
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
MY_API_KEY = ""
os.environ["OPENAI_API_KEY"] = MY_API_KEY

website = "https://sites.google.com/view/mnovackmath/home"

# Instantiate the LLMChain and text splitter for use later
prompt = PromptTemplate.from_template("Summarize this content: {context}")
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain)
text_splitter = TokenTextSplitter(chunk_size=4000, chunk_overlap=0)

# Set up the experiment tracking
mlflow.set_tracking_uri("")
experiment = mlflow.set_experiment("Langchain + mlflow")
with mlflow.start_run():
    # Load the documents
    loader = WebBaseLoader(website)
    docs = loader.load_and_split(text_splitter=text_splitter)

    # Log the number of docs
    print("Logging the number of docs")
    params = {
        "num_docs": len(docs),
        "website": website,
    }
    mlflow.log_params(params)

    # Make prediction
    inputs = [docs[0].page_content]
    outputs = [stuff_chain.run(docs[:1])]
    prompts = [stuff_chain.llm_chain.prompt.template]

    print()
    print("ChatGPT output:")
    print(textwrap.fill(outputs[0]))

    # Log prediction
    print()
    print("Logging prediction")
    model_info = mlflow.llm.log_predictions(inputs, outputs, prompts)

    # log the model, I can use the infer signature later if I want
    print()
    print('Currently there is a bug with logging models')
    # logged_model = mlflow.langchain.log_model(
    #     llm_chain,
    #     "langchain_llm_chain",
    # )

    # Logging the table artifacts
    print()
    print("Logging the table artifacts")
    data_dict = {
        'prompts': prompts,
        'inputs': inputs,
        'outputs': outputs,
    }
    df = pd.DataFrame(data_dict)
    mlflow.log_table(data=df, artifact_file="prediction_results.json")

