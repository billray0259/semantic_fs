import os
from PyPDF2 import PdfReader


def read_txt(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def read_pdf(file_path):
    # read every page and concatenate them
    pdf = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in pdf.pages])


def get_file_readers():
    return {
        '.txt': read_txt,
        '.pdf': read_pdf
    }


def iter_supported_files(directory):
    supported_file_types = get_file_readers()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in supported_file_types:
                yield os.path.join(root, file)


def iter_texts(directory):
    supported_file_types = get_file_readers()
    for file in iter_supported_files(directory):
        try:
            yield (file, supported_file_types[os.path.splitext(file)[1]](file))
        except Exception as e:
            print(f"Error reading file {file}: {e}")