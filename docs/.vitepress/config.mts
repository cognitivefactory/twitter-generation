import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "twitter-generation",
  description: "Generation of realistic tweets using LLMs",
  base: "/twitter-generation/", // for GitHub Pages ONLY

  head: [
    [
      "link",
      {
        rel: "icon",
        href: "https://onedrive.live.com/embed?resid=DAC5E8A44C554913%21160391&authkey=%21AB4zQFP-EHHtMWQ",
      },
    ],
    [
      "link",
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" },
    ],
  ],

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: "https://onedrive.live.com/embed?resid=DAC5E8A44C554913%21160391&authkey=%21AB4zQFP-EHHtMWQ",

    nav: [
      { text: "Home", link: "/" },
      { text: "Documentation", link: "/pages/get-started" },
      { text: "Results", link: "/pages/results" },
      { text: "Publications", link: "/pages/publications" },
    ],

    sidebar: [
      {
        text: "Documentation",
        items: [
          { text: "🚀 Get Started", link: "/pages/get-started" },
          { text: "⌨️ the CLI", link: "/pages/doc/cli" },
          { text: "🤖 XWin LLM", link: "/pages/doc/xwin-llm" },
          { text: "🤖 Mistral LLM", link: "/pages/doc/mistral-llm" },
          { text: "📚 data loader", link: "/pages/doc/data-loader" },
        ],
      },
      {
        text: "Results",
        items: [{ text: "📊 Results", link: "/pages/results" }],
      },
    ],

    socialLinks: [{ icon: "github", link: "https://github.com/cognitivefactory/twitter-generation" }],

    footer: {
      message:
        "Twitter Generation is a project by " +
        "<a href='https://github.com/orgs/cognitivefactory/teams/tps-sdia-2023'>Cognitive Factory</a><br><br>",
      copyright:
        "this website : Copyright (c) 2023-present " +
        "<a href='https://github.com/ThomasByr/'>ThomasByr</a> - AGPL v3<br>" +
        "logo & icon : Copyright (c) 2024-present " +
        "<a href=''>Jean-Hervé</a> - all rights reserved",
    },
  },
});
