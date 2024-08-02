import pandas as pd
import gutenbergpy.textget


def get_by_book_id(ids: list) -> pd.DataFrame:

    books_by_id = {'book': {}}

    for book_id in ids:
        raw_book = gutenbergpy.textget.get_text_by_id(book_id)
        clean_book = gutenbergpy.textget.strip_headers(raw_book)

        books_by_id['book'].update({book_id: clean_book})

    # convert to pandas
    df = pd.DataFrame(books_by_id)
    return df


if __name__ == "__main__":
    get_by_book_id([1342])

