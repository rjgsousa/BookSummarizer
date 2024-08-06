import pandas as pd
import random
import evaluate
import logging

from booksum.utils.io_ops import BookSumDataSetIO, load_parquet
from booksum.utils.service_utils import book_summary_api


class Evaluation:
    def __init__(self, logger, data_path):
        random.seed(65535)
        self.logger = logger
        self.data_path = data_path

        # load BookSum utility
        self.book_sum = BookSumDataSetIO(
            data_path=self.data_path
        )

        self.metric_names = ["bleu", "rouge", "meteor"]
        # Load the evaluation metric
        self.metrics = dict(zip(self.metric_names, map(lambda x: evaluate.load(x), self.metric_names)))

    def _calc_metrics(self, pred, resp) -> pd.DataFrame:
        results = pd.DataFrame(columns=[key for key in self.metric_names])

        for key, val in self.metrics.items():
            results[key] = [self.metrics[key].compute(predictions=pred, references=resp)]

        return results

    def _calc_metrics_batch(self, results: pd.DataFrame | str):

        if isinstance(results, str):
            results = load_parquet(results)

        with_literacy_know_how = results['with-literacy-know-how'].unique()[0]

        metrics = pd.DataFrame(columns=[key for key in self.metric_names])
        # Compute summarization metrics
        for response_type in ['base-response', 'simple-rag']:
            met = self._calc_metrics(results[response_type], results['summary'])
            # set index for reference
            met = met.set_index(pd.Series([response_type]))

            metrics = pd.concat([metrics, met], axis=0)

        self.logger.warning('Saving a metrics ...')
        df = pd.DataFrame(metrics)
        df.to_parquet(f'metrics_with-literacy-know-how={with_literacy_know_how}.parquet')

    @staticmethod
    def summarize_given_text(text):
        results = book_summary_api({"book_text": text}, "book-passage")
        return results

    @staticmethod
    def summarize_given_title(title):
        results = book_summary_api({"book": title}, "book-title")
        return results

    def evaluate(
            self,
            book_chapter_name=None,
            book_title=None
    ):
        # one or the other, not both true or false
        if (not book_title) ^ (not book_chapter_name):
            raise ValueError('Summarization evaluation should be done either by a chapter name or by a book title.')

        if not book_chapter_name:
            bid, summary, chapter, book_parquet_ref = \
                self.book_sum.get_booksum_summary_and_chapter_by_name_and_chapter(book_chapter_name)

            response = self.summarize_given_text(chapter)
        else:
            raise NotImplemented(f"Not implemented due lack of annotated data")

        # Compute summarization metrics
        results = self._calc_metrics([response], [summary])
        return results

    def evaluate_random_batch(self):

        batch_results = pd.DataFrame(
            columns=['ref', 'summary', 'base-response', 'simple-rag', 'with-literacy-know-how']
        )

        # just to test in order to avoid rate limit errors
        books = self.book_sum.booksum[self.book_sum.booksum.chapter_length < 1000]
        bids = random.sample(books.bid.unique().tolist(), 10)

        for item, bid in enumerate(bids):
            summary, chapter, book_parquet_ref = \
                self.book_sum.get_booksum_by_index(bid)

            response = self.summarize_given_text(chapter)

            batch_results.loc[item] = (
                    [book_parquet_ref] +
                    [summary] +
                    [response['base-response']] + [response['simple-rag']] +
                    [response['with-literacy-know-how']]
            )

        self.logger.warning('Saving a snapshot of results...')
        df = pd.DataFrame(batch_results)
        df.to_parquet('metrics_snapshot.parquet')

        self._calc_metrics_batch(batch_results)

        return batch_results


if __name__ == "__main__":
    sum_logger = logging.getLogger()
    sum_logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    sum_logger.addHandler(console_handler)

    eval_book_summary = Evaluation(logger=sum_logger, data_path='../../data/processed')
    eval_book_summary.evaluate_random_batch()
    eval_book_summary._calc_metrics_batch('metrics_snapshot.parquet')

