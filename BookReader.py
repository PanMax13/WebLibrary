import pypdf


class BookReader:

    # init book
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf = pypdf.PdfReader(self.pdf_path)

    # get page text
    def page_reader(self, page=0) -> str:
        text = self.pdf.get_page(page).extract_text()
        return text

    # pagination
    def pagination(self, page=1) -> []: # return pagination pages
        middle = page

        value_of_pages = 5 # value of pages in pagination list
        pagination = []

        if middle - value_of_pages < 0:
            pagination = [page for page in range(0, middle)] + [page for page in range(middle, value_of_pages)]
            return pagination

        if middle + value_of_pages > len(self.pdf.pages):
            pagination = [page for page in range(middle - value_of_pages, len(self.pdf.pages))]
            return pagination

        return [page for page in range(middle - value_of_pages, middle)] + [page for page in range(middle, middle + value_of_pages)]



    def get_last_page(self):
        return self.pdf.get_num_pages() - 1
