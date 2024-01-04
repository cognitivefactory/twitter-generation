import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "twitter-generation",
  description: "Generation of realistic tweets using LLMs",
  base: "/twitter-generation/", // for GitHub Pages

  head: [
    ["link", { rel: "icon", href: "/webApp-data-p/favicon.ico" }], // for GitHub Pages
    // ['link', { rel: 'icon', href: '/favicon.png' }],
    [
      "link",
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" },
    ],
  ],

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/favicon.png',

    nav: [
      { text: "Home", link: "/" },
      { text: "Publications", link: "/pages/publications" },
    ],

    sidebar: [
      {
        text: "Documentation",
        items: [
          { text: "🚀 Get Started", link: "/pages/get-started" },
          { text: "⌨️ the CLI", link: "/pages/doc/cli" },
          { text: "🤖 XWin LLM", link: "/pages/doc/xwin-llm" },
          { text: "📚 data loader", link: "/pages/doc/data-loader" },
        ],
      },
      {
        text: "Results",
        items: [
        ],
      }
    ],

    socialLinks: [{ icon: "github", link: "https://github.com/cognitivefactory/twitter-generation" }],
  },
});
