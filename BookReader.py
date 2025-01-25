import pypdf


class BookReader():

    # init book
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf = pypdf.PdfReader(self.pdf_path)

    # get page text
    def page_reader(self, page=0) -> str:
        text = self.pdf.get_page(page).extract_text()
        return text

    # pagination
    def pagination(self, page=0) -> []: # return pagination pages
        pages = 5 # value of pages in pagination block

        middle = page

        if middle < pages:
            return [x for x in range(1, middle)] + [x for x in range(middle, middle + pages)]
        return [x for x in range(middle - pages, middle)] + [x for x in range(middle, middle + pages + 1)]


    def get_last_page(self):
        return self.pdf.get_num_pages() - 1



book = BookReader('books/Anna_Karenina.pdf')

print(book.get_last_page())