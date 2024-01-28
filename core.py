import chardet
import os
import pandas as pd
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import requests


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
                return file_path

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
            return csv_file_path
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @staticmethod
    def get_headfile(file_path):
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.head()

    @staticmethod
    def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
        """ OCR.space API request with local file.
            Python3.5 - not tested on 2.7
        :param filename: Your file path & name.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        List of available language codes can be found on https://ocr.space/OCRAPI
                        Defaults to 'en'.
        :return: Result in JSON format.
        """

        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        return r.content.decode()

    @staticmethod
    def ocr_space_url(url, overlay=False, api_key='K82183368388957', language='eng'):
        """ OCR.space API request with remote file.
            Python3.5 - not tested on 2.7
        :param url: Image url.
        :param overlay: Is OCR.space overlay required in your response.
                        Defaults to False.
        :param api_key: OCR.space API key.
                        Defaults to 'helloworld'.
        :param language: Language code to be used in OCR.
                        List of available language codes can be found on https://ocr.space/OCRAPI
                        Defaults to 'en'.
        :return: Result in JSON format.
        """

        payload = {'url': url,
                   'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        r = requests.post('https://api.ocr.space/parse/image',
                          data=payload,
                          )
        return r.content.decode()


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

            if self.notebook.cells:
                del self.notebook.cells[-1]
            # Handle exceptions if any
            return {"error": str(e)}

        print(self.notebook.cells[-1].outputs)

        # Convert the executed notebook to HTML for display
        html_exporter = HTMLExporter()
        (body, resources) = html_exporter.from_notebook_node(self.notebook)

        return {"html": body, "metadata": resources}
