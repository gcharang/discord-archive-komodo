module.exports = {
  head: [
    [
      "link",
      {
        rel: "icon",
        href: "KMD_Mark_Black.png"
      }
    ],
    [
      "meta",
      {
        name: "twitter:card",
        content: "summary_large_image"
      }
    ],
    [
      "meta",
      {
        name: "twitter:card",
        content: "summary_large_image"
      }
    ],
    [
      "meta",
      {
        name: "twitter:site",
        content: "@komodoplatform"
      }
    ],
    [
      "meta",
      {
        name: "twitter:title",
        content: "Komodo Discord Archive"
      }
    ],
    [
      "meta",
      {
        name: "twitter:description",
        content: "Archive of the Komodo Discord server's public channels"
      }
    ]
  ],
  title: "Komodo Discord Archive",
  base: "/",
  description: "Archive of the Komodo Discord server's public channels",
  themeConfig: {
    repo: "gcharang/discord-archive-komodo",
    repoLabel: "Github",
    docsDir: "docs",
    editLinks: false,
    logo: "/KMD_Horiz_White.svg",
    nav: [{
        text: "HTML Light",
        link: "/format/htmllight.md"
      },
      {
        text: "HTML Dark",
        link: "/format/htmldark.md"
      },
      {
        text: "Plain Text",
        link: "/format/plaintext.md"
      },
      {
        text: "CSV",
        link: "/format/csv.md"
      }
    ]
  }
};