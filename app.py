# """This was made with ChatGPT"""
# Gradio doesn't seem to work with conda environments so I don't think that
# I can use the reload mode mentioned in the gradio docs:
# https://www.gradio.app/guides/developing-faster-with-reload-mode
# https://www.gradio.app/guides/developing-faster-with-reload-mode

import gradio as gr

def markdown_output(text):
    # For this example, we'll just return the same text.
    # In practice, you might apply some transformation here.
    return text

# Define the Gradio interface
interface = gr.Interface(
    fn=markdown_output,  # Function to call on user input
    inputs=gr.Textbox(label="Input", placeholder="Enter some text..."), 
    outputs=[gr.Textbox(label="ChatGPT response",
                        show_label=True,
                        show_copy_button=True, max_lines=10)],
    # outputs=gr.Markdown(),  # Markdown output
    live=True,  # Update the output live as you type
    title="Markdown Generator",  # Title of the web page
    description="Enter text in the textbox to see its markdown version." 
)

interface.launch(debug=True)