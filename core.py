import chardet
import os
import pandas as pd
import nbformat
from IPython.core.display_functions import display
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter


class UploadFile:
    def __init__(self):
        pass

    @staticmethod
    def is_utf8_csv(file_path):
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)

                # Проверяем, что определенная кодировка - UTF-8, и ее уверенность более 0.8
                if result['encoding'].lower() == 'utf-8' and result['confidence'] > 0.8:
                    return True
                else:
                    return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    @staticmethod
    def convert_to_csv(file_path):
        data = None
        try:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            # Получение расширения файла
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == '.csv':
                print("The file is already in CSV format.")
                return

            # Обработка разных типов файлов
            if file_extension == '.xlsx':
                data = pd.read_excel(file_path)
            else:
                raise ValueError(
                    f"Unsupported file type: {file_extension}. This method supports only XLSX and PDF files.")

            # Получение имени файла без расширения
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]

            # Сохранение данных в CSV файл
            csv_file_path = f"{file_name_without_extension}.csv"
            data.to_csv(csv_file_path, index=False)

            print(f'Data has been successfully converted and saved to {csv_file_path}.')

            # Удаление исходного файла
            os.remove(file_path)
            print(f'The original file {file_path} has been deleted.')
        except Exception as e:
            print(f"An error occurred: {str(e)}")


class NotebookExecutor:
    def __init__(self):
        self.notebook = nbformat.v4.new_notebook()
        self.execution_count = 1

    def execute_code(self, code_str):
        # Create a new code cell with the provided code
        cell = nbformat.v4.new_code_cell(source=code_str, execution_count=self.execution_count)
        self.execution_count += 1

        # Append the code cell to the notebook
        self.notebook.cells.append(cell)

        # Create an ExecutePreprocessor
        executor = ExecutePreprocessor(timeout=-1, kernel_name='python3')

        # Execute the notebook
        try:
            executor.preprocess(self.notebook, {'metadata': {'path': '.'}})
        except Exception as e:
            # Handle exceptions if any
            return {"error": str(e)}

        if "text" in self.notebook.cells[-1].outputs:
            print(self.notebook.cells[-1].outputs)
        else:
            display(self.notebook.cells[-1].outputs)

        # Convert the executed notebook to HTML for display
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(self.notebook)

        return {"html": body, "metadata": resources}
