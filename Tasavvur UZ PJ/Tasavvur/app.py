from core import NotebookExecutor, UploadFile
from LLM_model import LLM

system_prompt = """
Твоя задача писать код который не взаимодействует с пользователем

"""

llm = LLM(system_prompt=system_prompt)
notebook_executor = NotebookExecutor()

try:
    while True:
        for chunk in llm.conversation(input_text=input("Enter: ")):
            print(chunk, end="")
        print('\n\n')
        code_from_text = llm.history[-1]['content']
        extracted_code = llm.extract_code_from_text(code_from_text)

        # if exist some code in list
        if extracted_code:
            for code in extracted_code:
                result = notebook_executor.execute_code(code)

                if "error" in result:
                    print(f"Execution failed: {result['error']}")
                else:
                    # HTML part
                    output_file_path = "output.html"
                    with open(output_file_path, "w", encoding="utf-8") as output_file:
                        output_file.write(result["html"])

                    print(f"HTML result saved to {output_file_path}")

except KeyboardInterrupt:
    print("exit")


