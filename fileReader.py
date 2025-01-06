import pypdf


pdf = pypdf.PdfReader('./books/zverev.pdf')
def page_reader(pdf, page=0):

    return pdf.pages[page].extract_text() if not None else "Soory, some goes wrong. May be file dont contains the text(contain scan of text)"


print(page_reader(pdf, 5))