import pypdf


def page_reader(pdf_path, page=0):
    pdf = pypdf.PdfReader(pdf_path)
    return pdf.pages[page].extract_text() if not None else "Sorry, some goes wrong. May be file dont contains the text(contain scan of text)"


