from core import NotebookExecutor, UploadFile
from agent import LLM
import pandas as pd
import re

system_prompt = """
You are Tasavvur, an artificial intelligence analyst in Uzbekistan. Your task is to write code to fulfill requests from users or interpreters. You must execute these requests using Python code processed in the Jupyter environment.
"""

uf = UploadFile()
llm = LLM(system_prompt=system_prompt)
notebook_executor = NotebookExecutor()


try:

    file_path = input("Enter file path: ")
    file_path = uf.convert_to_csv(file_path)
    content = f"Head of {file_path} uploaded from user and extracted using pandas ```{uf.get_headfile(file_path)}```"

    llm.add_system_prompt({"role": "system", "content": content})

    continue_flag = 0
    input_text = None
    while True:
        if not continue_flag:
            input_text = input("Enter: ")

        for chunk in llm.conversation(input_text=input_text):
            print(chunk, end="")
        print('\n\n')
        code_from_text = llm.history[-1]['content']
        extracted_code = llm.extract_code_from_text(code_from_text)

        # if exist some code in list
        if extracted_code:
            for code in extracted_code:
                result = notebook_executor.execute_code(code)

                if "error" in result:
                    short_result = llm.last_100_words(re.sub(r'\033\[[0-9;]+m', '', result['error']))
                    print(f"Execution failed: {short_result}")
                    input_text = short_result
                    continue_flag = 1
                    break
                else:

                    if "text" in result:
                        print("added text result")
                        llm.add_system_prompt({"role": "system", "content": f"Result of your code: {result['text']}"})

                    # HTML part
                    output_file_path = "output.html"
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(result["html"])
                    print(f"HTML result saved to {output_file_path}")
                    continue_flag = 0
except KeyboardInterrupt:
    print(llm.history)
    print("exit")
