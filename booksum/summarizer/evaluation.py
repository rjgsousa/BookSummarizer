import pandas as pd
import random
import evaluate
import logging

from booksum.summarizer.booksummarizer import BookSummarizer
from booksum.utils.io_ops import BookSumDataSetIO


class Evaluation(BookSummarizer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        random.seed(65535)

        # load BookSum utility
        self.book_sum = BookSumDataSetIO(
            data_path=self.data_path
        )

        self.metric_names = ["bleu", "rouge", "meteor"]
        # Load the evaluation metric
        self.metrics = dict(zip(self.metric_names, map(lambda x: evaluate.load(x), self.metric_names)))

    def _calc_metrics(self, pred, resp):
        results = {}

        for key, val in self.metrics.items():
            results[key] = self.metrics[key].compute(predictions=pred, references=resp)

        return results

    def evaluate(self, book_chapter_name):
        bid, summary, chapter, book_parquet_ref = \
            self.book_sum.get_booksum_summary_and_chapter_by_name_and_chapter(book_chapter_name)

        response = self.summarize_given_text(chapter)['base-response']

        # Compute summarization metrics
        results = self._calc_metrics([response], [summary])
        return results

    def evaluate_random_batch(self):
        column_names = self.metric_names + ['id']

        batch_results = {key: [] for key in column_names}

        # just to test in order to avoid rate limit errors
        books = self.book_sum.booksum[self.book_sum.booksum.chapter_length < 1000]
        bids = random.sample(books.bid.unique().tolist(), 5)

        for bid in bids:
            summary, chapter, book_parquet_ref = \
                self.book_sum.get_booksum_by_index(bid)

            response = self.summarize_given_text(chapter)['base-response']

            # Compute summarization metrics
            results = self._calc_metrics([response], [summary])
            results['id'] = book_parquet_ref

            for key, val in results.items():
                batch_results[key].append(val)

            self.logger.warning('Saving a snapshot of results...')
            df = pd.DataFrame(batch_results)
            df.to_parquet('metrics.parquet')

        return batch_results


if __name__ == "__main__":
    sum_logger = logging.getLogger()
    sum_logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    sum_logger.addHandler(console_handler)

    eval_book_summary = Evaluation(
        logger=sum_logger,
        frac=0.1,
        root_path='../..',
        books_cfg_kb_filepath='config/books_to_process.yaml'
    )
    eval_book_summary.evaluate(book_chapter_name='Julius Caesar.act 5.scene 2')

