<template>
  <main class="page">
    <slot name="top" />

    <Content class="theme-default-content" />

    <div v-if="frontmatter.type == 'plaintext'">
      <a
        class="theme-default-content"
        href="/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt"
        target="_blank"
      >/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt</a>
      <p class="theme-default-content">{{timeDirs}}</p>
    </div>
    <PageEdit />
    <PageNav v-bind="{ sidebarItems }" />

    <slot name="bottom" />
  </main>
</template>

<script>
import PageEdit from "@theme/components/PageEdit.vue";
import PageNav from "@theme/components/PageNav.vue";

export default {
  components: { PageEdit, PageNav },
  props: ["sidebarItems", "staticFileStructure"],
  data: function() {
    return {
      staticFileStructure: this.staticFileStructure
    };
  },
  computed: {
    frontmatter: function() {
      return this.$page.frontmatter;
    },
    timeDirs: function() {
      return this.staticFileStructure.children.filter(function(dir) {
        return dir.type == "directory";
      });
    }
  }
};
</script>

<style lang="stylus">
@require '../styles/wrapper.styl';

.page {
  padding-bottom: 2rem;
  display: block;
}
</style>
