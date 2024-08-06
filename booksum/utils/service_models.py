from booksum.summarizer.booksummarizer import BookSummarizer


# class to load models
class BookSumIndex:
    def __init__(self, root_path, logger):
        self.model = None
        self.root_path = root_path
        self.logger = logger

    def load_all_models(self) -> None:
        self.model = BookSummarizer(
            logger=self.logger,
            root_path=self.root_path,
            books_cfg_kb_filepath='config/books_to_process.yaml',
            frac=1,
            with_literacy=True
        )
