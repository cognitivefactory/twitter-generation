from transformers import AutoTokenizer, AutoModelForCausalLM


MASK = {
    "en": """
Generate tweets about <topic> from the user perspective, making them look as real as possible.
The tweets should be as diverse as possible and users should feel <sentiment> about the topic.
""",
    "fr": """
Génère des tweets sur <topic> du point de vue de l'utilisateur, en les rendant aussi réels que possible.
Les tweets doivent être aussi diversifiés que possible et les utilisateurs doivent être <sentiment> à propos du sujet.
""",
    "de": """
Generieren Sie Tweets über <topic> aus der Sicht des Benutzers, so real wie möglich.
Die Tweets sollten so vielfältig wie möglich sein und die Benutzer sollten <sentiment> zum Thema fühlen.
""",
    "es": """
Genere tweets sobre <topic> desde la perspectiva del usuario, haciéndolos lo más reales posible.
Los tweets deben ser lo más diversos posible y los usuarios deben sentir <sentiment> sobre el tema.
""",
    "it": """
Genera tweet su <topic> dal punto di vista dell'utente, rendendoli il più realistici possibile.
I tweet dovrebbero essere il più diversi possibile e gli utenti dovrebbero sentire <sentiment> sul tema.
""",
    "pt": """
Gere tweets sobre <topic> do ponto de vista do usuário, tornando-os o mais reais possível.
Os tweets devem ser o mais diversificados possível e os usuários devem sentir <sentiment> sobre o tópico.
""",
    "default": """
Generate tweets about <topic> from the user perspective, making them look as real as possible.
The tweets should be as diverse as possible and users should feel <sentiment> about the topic.
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
