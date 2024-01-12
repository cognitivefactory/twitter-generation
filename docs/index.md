---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "twitter-generation"
  text: "Generation of realistic tweets using LLMs"
  tagline: A Télécom Physique Strasbourg Study
  actions:
    - theme: brand
      text: Get Started
      link: /pages/get-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/cognitivefactory/twitter-generation
  image:
    src: https://onedrive.live.com/embed?resid=DAC5E8A44C554913%21160393&authkey=%21ANs5YVolVkTE-QE
    alt: favicon.png

features:
  - icon: ✏️
    title: Documentation
    details: Everything you need to know about the code.
  - icon: 📊
    title: Results
    details: Results of our experiments and analysis of performance.
  - icon: 📚
    title: Publications
    details: Publications related to our work.
---

<style>
:root {
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: -webkit-linear-gradient(120deg, #bd34fe 30%, #41d1ff);

  --vp-home-hero-image-background-image: linear-gradient(-45deg, #bd34fe 50%, #47caff 50%);
  --vp-home-hero-image-filter: blur(44px);
}

@media (min-width: 640px) {
  :root {
    --vp-home-hero-image-filter: blur(56px);
  }
}

@media (min-width: 960px) {
  :root {
    --vp-home-hero-image-filter: blur(68px);
  }
}
</style>
