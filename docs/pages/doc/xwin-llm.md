# 🤖 XWin LLM

> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> Model by [🔗 Xwin-LM Team](https://github.com/Xwin-LM)
>
> ```tex
> @software{xwin-lm,
>   title = {Xwin-LM},
>   author = {Xwin-LM Team},
>   url = {https://github.com/Xwin-LM/Xwin-LM},
>   version = {pre-release},
>   year = {2023},
>   month = {9},
> }
> ```

This model is based on Llama2 and was released under the same license. This model is just a LLM, meaning that this model only generates the most likely piece of text following a prompt. We use the 7B version of this model. Cavecats may include:

- generating text that is actually the prompt and then maybe answering the (modified) prompt
- not fully understanding the prompt
- writing very similar tweets in one generation
- making undesired comments and/or remarks

## 📥 Download

```py
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")
model = AutoModelForCausalLM.from_pretrained("Xwin-LM/Xwin-LM-7B-V0.2")
```
