from transformers import AutoTokenizer, AutoModelForCausalLM


MASK = {
    "en": """
Generate tweets in English about "<topic>" from the user perspective, making them look as real as possible.
The tweets should be in English, as diverse as possible and users should feel <sentiment> about the topic.
""",
    "fr": """
Génère des tweets en français sur "<topic>" du point de vue de l'utilisateur, en les rendant aussi réels que possible.
Les tweets doivent être en français, aussi diversifiés que possible et les utilisateurs doivent ressentir <sentiment> à propos du sujet.
""",
    "de": """
Generieren Sie Tweets auf Deutsch über "<topic>" aus der Nutzerperspektive, so real wie möglich.
Die Tweets sollten auf Deutsch sein, so vielfältig wie möglich und die Nutzer sollten <sentiment> zum Thema empfinden.
""",
    "default": """
Generate tweets in English about "<topic>" from the user perspective, making them look as real as possible.
The tweets should be in English, as diverse as possible and users should feel <sentiment> about the topic.
""",
}


class Model:
    def __init__(self) -> None:
        self.model = AutoModelForCausalLM.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")
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
        prompt += "\n1. "
        return self.__generate(prompt)
