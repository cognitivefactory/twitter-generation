# 🤖 Mistral LLM

> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> Model by [🔗 Mistral AI Team](https://github.com/mistralai)
>
> ```txt
> The Mistral AI Team
> Albert Jiang, Alexandre Sablayrolles, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Louis Ternon, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, William El Sayed.
> ```

This model is a whole new LLM, released under the Apache 2.0 license.

The finetuned version we use here is an improved instruct fine-tuned version trained to answer instructions. The base version of Mistral-7B can be used the same way we use and prompt XWin-7B. This instruct model addresses the following cavecats of Xwin-LM:

- generating text that is actually the prompt and then maybe answering the (modified) prompt
- making undesired comments and/or remarks

## 📥 Download

```py
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
```
