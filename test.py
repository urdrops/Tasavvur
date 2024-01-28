from core import UploadFile

uf = UploadFile()

# Use examples:
test_file = uf.ocr_space_file(filename='img.png', language='pol')
print(test_file)