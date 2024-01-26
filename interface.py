import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import gradio as gr
import os
import time


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    return history


def bot(history):
    response = history[-1][0]
    history[-1][1] = ""
    print(history)
    for character in response:
        history[-1][1] += character
        time.sleep(0.01)
        yield history


def execute_code(history):
    code = history[-1][0]
    try:
        # Create a notebook with a code cell
        notebook = nbformat.v4.new_notebook()
        notebook.cells.append(nbformat.v4.new_code_cell(code))

        # Execute the notebook
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(notebook, {'metadata': {'path': './'}})

        # Get the output from the executed code cell
        output = notebook.cells[0].outputs
        if output:
            result = output[0].get('text', '').strip()
        else:
            result = "No output"

        history[-1][1] = result
        yield history
    except Exception as e:
        print(e)
        history[-1][1] = f"Error: {e}"
        yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="TASAVVUR",
        label="TASAVVUR",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        code_input = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter code and press enter",
            container=False,
        )

    code_msg = code_input.submit(add_text, [chatbot, code_input], [chatbot, code_input], queue=False).then(
        execute_code, chatbot, chatbot, api_name="code_execution"
    )
    code_msg.then(lambda: gr.Textbox(interactive=True), None, [code_input], queue=False)

demo.queue()
demo.launch(share=True)
