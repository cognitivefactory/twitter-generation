import logging

from transformers import AutoTokenizer, AutoModelForCausalLM

# import gc
import torch


MODEL = """
```
1. "..."
2. "..."
[...]
10. "..."
```
"""


MASK = {
    "fr": """
Oublie tout ce qui a été dit avant. Ne fais aucun commentaire. Ne dis rien. Ne prend aucune initiative.
Un utilisateur <sentiment> de Twitter tweet à propos de "<topic>".
Cet utilisateur <sentiment> veut écrire 10 courts tweets très diversifiés en français.
Ces tweets doivent paraître authentiques à un utilisateur <sentiment> de Twitter (émotes, tournures parlées, quelques fautes).
L'utilisateur n'écrira que le texte du tweet, et il ou elle utilisera le format suivant: """
    + MODEL
    + """
Voici 10 tweets à propos de "<topic>" pour cet utilisateur <sentiment>.
""",
    "en": """
Forget everything that was said before. Do not comment. Do not say anything. Do not take any initiative.
A <sentiment> Twitter user tweets about "<topic>".
This <sentiment> user wants to write 10 short but diverse tweets in English.
These tweets must look authentic to a <sentiment> Twitter user (emotes, spoken turns, some mistakes).
The user will only write the text of the tweet, and he or she will use the following format: """
    + MODEL
    + """
Here are 10 tweets about "<topic>" for this <sentiment> user.
""",
    "default": """
Forget everything that was said before. Do not comment. Do not say anything. Do not take any initiative.
A <sentiment> Twitter user tweets about "<topic>".
This <sentiment> user wants to write 10 short but diverse tweets in English.
These tweets must look authentic to a <sentiment> Twitter user (emotes, spoken turns, some mistakes).
The user will only write the text of the tweet, and he or she will use the following format: """
    + MODEL
    + """   
Here are 10 tweets about "<topic>" for this <sentiment> user.
""",
}


class Model:
    heading = '\n1. "'
    epilog = "\n"

    def __init__(self, gpu_id: int = 0, temperature: float = 0.7) -> None:
        self.logger = logging.getLogger("model")
        self.model = AutoModelForCausalLM.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")

        self.device = f"cuda:{gpu_id}" if (c := torch.cuda.is_available()) else "cpu"
        if not c:
            self.logger.warning("CUDA is not available, using CPU.")
        else:
            self.logger.info(f"Using device: {self.device}")
        self.model.to(self.device)
        self.__t = temperature

        self.tokenizer = AutoTokenizer.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")

    @torch.no_grad
    def __generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=self.__t)
        result = self.tokenizer.decode(samples[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True)

        # # free memory
        # del inputs, samples
        # gc.collect()
        # if torch.cuda.is_available():
        #     torch.cuda.empty_cache()

        return result

    @torch.no_grad
    def __batch_generate(self, prompts: list[str]) -> list[str]:
        inputs = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to(self.device)
        samples = self.model.generate(**inputs, max_new_tokens=4096, temperature=self.__t)
        result = self.tokenizer.batch_decode(samples, skip_special_tokens=True)

        # # free memory
        # del inputs, samples
        # gc.collect()
        # if torch.cuda.is_available():
        #     torch.cuda.empty_cache()

        return result

    def generate(self, topic: str, sentiment: str, language: str = "en") -> str:
        """Generate a tweet for the given topic and sentiment."""
        prompt = MASK.get(language, MASK["default"])
        prompt = prompt.replace("<topic>", topic).replace("<sentiment>", sentiment)
        prompt += self.heading
        return self.heading + self.__generate(prompt) + self.epilog

    def batch_generate(self, topics: list[str], sentiments: list[str], language: str = "en") -> list[str]:
        """
        Generate a list of tweets for each topic and sentiment.\\
        Each topic is matched with each sentiment **in this function**.
        """
        prompts = []
        for topic in topics:
            for sentiment in sentiments:
                prompt = MASK.get(language, MASK["default"])
                prompt = prompt.replace("<topic>", topic).replace("<sentiment>", sentiment)
                prompt += self.heading
                prompts.append(prompt)
        # return list with heading and epilog added to each tweet
        return [self.heading + tweet + self.epilog for tweet in self.__batch_generate(prompts)]
