import logging

from .export_adapter import ExportAdapter
from .prompt_generator import SomethingGenerator, PrompGenerator
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

        prompt_generator = PrompGenerator(topic_generator, sentiment_generator)

        for t, s in prompt_generator:
            r = self.model.generate(t, s, local_lang)
            dispatcher.export(f"{t};{s};{r}\n")
