"""Markdown gradio experiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N8Kgpl3tlggmOTGtsqxR0x--oHW3i91y
"""
# Set the API key - if this key gets committed to a gitrepo then it gets 
# disabled
# import os
# MY_API_KEY = ''
# os.environ['OPENAI_API_KEY'] = MY_API_KEY
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import TokenTextSplitter
import textwrap

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

text_splitter = TokenTextSplitter(chunk_size=4000, chunk_overlap=0)
docs = loader.load_and_split(text_splitter=text_splitter)

print(f"Number of docs: {len(docs)}")
print()
print(textwrap.fill(docs[0].page_content, max_lines=10))

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
chain = load_summarize_chain(llm, chain_type="map_reduce")
output = chain.run(docs)

print()
print("ChatGPT output:")
print(textwrap.fill(output))

# """This was made with ChatGPT"""
# Gradio doesn't seem to work with conda environments so I don't think that
# I can use the reload mode mentioned in the gradio docs:
# https://www.gradio.app/guides/developing-faster-with-reload-mode
# https://www.gradio.app/guides/developing-faster-with-reload-mode

# import gradio as gr

# def markdown_output(text):
#     # For this example, we'll just return the same text.
#     # In practice, you might apply some transformation here.
#     return text

# # Define the Gradio interface
# interface = gr.Interface(
#     fn=markdown_output,  # Function to call on user input
#     inputs=gr.Textbox(label="Input", placeholder="Enter some text..."),  # Textbox input
#     outputs=[gr.Textbox(label="ChatGPT response",
#                         show_label=True,
#                         show_copy_button=True, max_lines=10)],
#     # outputs=gr.Markdown(),  # Markdown output
#     live=True,  # Update the output live as you type
#     title="Markdown Generator",  # Title of the web page
#     description="Enter text in the textbox to see its markdown version."  # Description
# )

# interface.launch(debug=True)
