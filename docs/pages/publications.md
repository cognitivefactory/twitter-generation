# Publications related to our work

## 2023

### [Mistral 7B](https://arxiv.org/pdf/2310.06825.pdf)

arXiv:2310.06825v1

::: tip Authors

Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford,
Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel,
Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux,
Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix,
William El Sayed

:::

::: details Abstract
We introduce Mistral 7B, a 7–billion-parameter language model engineered for
superior performance and efficiency. Mistral 7B outperforms the best open 13B
model (Llama 2) across all evaluated benchmarks, and the best released 34B
model (Llama 1) in reasoning, mathematics, and code generation. Our model
leverages grouped-query attention (GQA) for faster inference, coupled with sliding
window attention (SWA) to effectively handle sequences of arbitrary length with a
reduced inference cost. We also provide a model fine-tuned to follow instructions,
Mistral 7B – Instruct, that surpasses Llama 2 13B – chat model both on human and
automated benchmarks. Our models are released under the Apache 2.0 license.

Code: <https://github.com/mistralai/mistral-src>

Webpage: <https://mistral.ai/news/announcing-mistral-7b>
:::

### [Fine Tuning LLM: Parameter Efficient Fine Tuning (PEFT) — LoRA & QLoRA — Part 1](https://abvijaykumar.medium.com/fine-tuning-llm-parameter-efficient-fine-tuning-peft-lora-qlora-part-1-571a472612c4)

online blog post on Medium

::: tip Authors

A B Vijay Kumar

:::

::: details Summary
In this blog, we will understand the idea behind Parameter Efficient Fine Tuning (PEFT), and explore LoRA and QLoRA, Two of the most important PEFT methods. We will understnad how PEFT can be used to fine tune the model for domain specific tasks, at the lowest cost and minimal infrastrcuture.
:::

## 2017

### [NILC-USP at SemEval-2017 Task 4: A Multi-view Ensemble for Twitter Sentiment Analysis](https://arxiv.org/pdf/1704.02263.pdf)

arXiv:1704.02263v1

::: tip Authors

- **Edilson A. Corrêa Jr.**, Institute of Mathematics and Computer Science University of São Paulo (USP), São Carlos, São Paulo, Brazil
- **Vanessa Queiroz Marinho**, Institute of Mathematics and Computer Science University of São Paulo (USP), São Carlos, São Paulo, Brazil
- **Leandro Borges dos Santos**, Institute of Mathematics and Computer Science University of São Paulo (USP), São Carlos, São Paulo, Brazil

:::

::: details Abstract
This paper describes our multi-view ensemble approach to SemEval-2017 Task 4
on Sentiment Analysis in Twitter, specifically, the Message Polarity Classification
subtask for English (subtask A). Our system is a voting ensemble, where each base
classifier is trained in a different feature
space. The first space is a bag-of-words
model and has a Linear SVM as base classifier. The second and third spaces are two
different strategies of combining word embeddings to represent sentences and use a
Linear SVM and a Logistic Regressor as
base classifiers. The proposed system was
ranked 18th out of 38 systems considering
F1 score and 20th considering recall.
:::
