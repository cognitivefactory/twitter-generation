import logging

from alive_progress import alive_bar

from .export_adapter import ExportAdapter
from .prompt_generator import SomethingGenerator, PromptGenerator
from .model import Model

__all__ = ["App"]


class App:
    def __init__(self) -> None:
        self.model = Model()
        self.logger = logging.getLogger("app")

    def run(
        self,
        topics_file_path: str,
        sentiments_file_path: str,
        output_file_path: str,
        local_lang: str = "en",
    ) -> None:
        dispatcher = ExportAdapter(output_file_path)
        topic_generator = SomethingGenerator(topics_file_path)
        sentiment_generator = SomethingGenerator(sentiments_file_path)

        self.logger.info("got %d topics and %d sentiments", topic_generator.count, sentiment_generator.count)

        prompt_generator = PromptGenerator(topic_generator, sentiment_generator)
        topic_number = 0
        senti_number = 0

        with alive_bar(prompt_generator.count) as bar:
            for t, s in prompt_generator:
                # (str, str) because 2 generators
                if senti_number == sentiment_generator.count:
                    senti_number = 0
                    topic_number += 1

                bar.title(f"generating #{topic_number + 1}({senti_number + 1})")
                r = self.model.generate(t, s, local_lang)
                bar.title(f" exporting #{topic_number + 1}({senti_number + 1})")
                dispatcher.export(t, s, r)
                bar()

                senti_number += 1
