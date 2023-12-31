"""Markdown gradio experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N8Kgpl3tlggmOTGtsqxR0x--oHW3i91y

When using conda I need to use `which` to be sure that I'm using the 
correct python and pip for installs. Sometimes I need to deactivate 
multiple times in order to get out of the base environment. Then I activate
the conda environment that I want and it uses the correct pip. See this link
https://github.com/ContinuumIO/anaconda-issues/issues/1429#issuecomment-1044871389

It helps to use the options python and pip when creating a new conda env
with the conda create command. 
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

# from pyngrok import ngrok

import mlflow
import pandas as pd
import argparse

# In theory I should be able to set the parameters as environment vars
# so that I don't need to re-enter them every time...
# such as if I want to run this via the command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process API key and website")
    parser.add_argument(
        "--api-key", type=str, required=True, help="API key for the application"
    )
    parser.add_argument(
        "--website", type=str, required=True, help="Website to summarize"
    )
    args = parser.parse_args()

    # NGROK_AUTH_TOKEN = set_api_key('NGROK_AUTH_TOKEN',
    # 'Enter your ngrok auth token: ')
    # ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    MY_API_KEY = args.api_key
    os.environ["OPENAI_API_KEY"] = MY_API_KEY

    website = args.website

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

    # Logging the table artifacts
    print()
    print("Logging the table artifacts")
    data_dict = {
        "prompts": prompts,
        "inputs": inputs,
        "outputs": outputs,
    }
    df = pd.DataFrame(data_dict)
    mlflow.log_table(data=df, artifact_file="prediction_results.json")
