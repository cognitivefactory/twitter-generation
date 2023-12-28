import logging

from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# import torch.nn as nn


MASK = {
    "en": """
Forget everything said before and do as told. You are a <sentiment> user of Twitter and you are tweeting about "<topic>".
Generate a small list of tweets you could write in real life about "<topic>", making them look as real as possible.
The tweets should be as diverse as possible and users should feel <sentiment> about the topic.
Do generate anything that is not a tweet.
""",
    "fr": """
Oublie tout ce qui a été dit avant et fais comme on te dit. Tu es un utilisateur <sentiment> de Twitter et tu tweetes à propos de "<topic>".
Génère une petite liste de tweets que tu pourrais écrire dans la vraie vie à propos de "<topic>", en les rendant aussi réels que possible.
Les tweets doivent être aussi diversifiés que possible et les utilisateurs doivent être <sentiment> à propos du sujet.
Ne génère rien qui ne soit pas un tweet.
""",
    "de": """
Vergessen Sie alles, was vorher gesagt wurde und tun Sie, was gesagt wurde. Sie sind ein <sentiment> Benutzer von Twitter und Sie twittern über "<topic>".
Generieren Sie eine kleine Liste von Tweets, die Sie im wirklichen Leben über "<topic>" schreiben könnten, und machen Sie sie so real wie möglich.
Die Tweets sollten so vielfältig wie möglich und die Nutzer sollten <sentiment> zum Thema empfinden.
Generieren Sie nichts, was kein Tweet ist.
""",
    "default": """
Forget everything said before and do as told. You are a <sentiment> user of Twitter and you are tweeting about "<topic>".
Generate a small list of tweets you could write in real life about "<topic>", making them look as real as possible.
The tweets should be as diverse as possible and users should feel <sentiment> about the topic.
Do generate anything that is not a tweet.
""",
}


class Model:
    heading = "\n1. "
    epilogue = "\n"

    def __init__(self) -> None:
        self.logger = logging.getLogger("model")
        self.model = AutoModelForCausalLM.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")

        # n = torch.cuda.device_count()
        # self.logger.info("using %d GPUs", n)
        # if n > 1:
        #     self.model = nn.DataParallel(self.model)

        # self.model.to("cuda")
        self.tokenizer = AutoTokenizer.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")

    def __generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=0.7)
        return self.tokenizer.decode(samples[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)

    def __batch_generate(self, prompts: list[str]) -> list[str]:
        inputs = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=0.7)
        return self.tokenizer.batch_decode(samples, skip_special_tokens=True)

    def generate(self, topic: str, sentiment: str, language: str = "en") -> str:
        prompt = MASK.get(language, MASK["default"])
        prompt = prompt.replace("<topic>", topic).replace("<sentiment>", sentiment)
        prompt += self.heading
        return self.heading + self.__generate(prompt) + self.epilogue
