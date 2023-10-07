from PyPDF2 import PdfReader

def pdfanalysis(pdf_path):
    try:
        with (open(pdf_path, 'rb') as f):
            pdf = PdfReader(f)
            metadata = pdf.metadata
            number_of_pages = len(pdf.pages)
            author = metadata.get('/Author', 'N/A')
            creator = metadata.get('/Creator', 'N/A')
            producer = metadata.get('/Producer', 'N/A')
            creation_date = metadata.get('/CreationDate', 'N/A')
            modified_date = metadata.get('/ModDate', 'N/A')

            result = f"                        \n" \
                     f"Author        : {author}\n" \
                     f"Creator       : {creator}\n" \
                     f"Producer      : {producer}\n" \
                     f"Creation Date : {creation_date}\n" \
                     f"Modified Date : {modified_date}\n" \
                     f"Number of Pages : {number_of_pages}\n"

            return result
    except Exception as e:
        return f"[-] Error: {str(e)}"


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 pdfanalysis.py <pdf_path>")
    else:
        pdf_path = sys.argv[1]
        analysis_result = pdfanalysis(pdf_path)
        print(analysis_result)
