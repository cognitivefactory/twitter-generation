import logging

from alive_progress import alive_it

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

        prompt_generator = PromptGenerator(topic_generator, sentiment_generator)

        for t, s in alive_it(prompt_generator):  # (str, str) because 2 generators
            r = self.model.generate(t, s, local_lang)
            dispatcher.export(t, s, r)
