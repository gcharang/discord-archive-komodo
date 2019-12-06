<template>
  <main class="page">
    <slot name="top" />

    <Content class="theme-default-content" />
    <PageEdit />
    <a
      class="theme-default-content"
      href="/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt"
      target="_blank"
    >/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt</a>
    <p class="theme-default-content">{{staticFileStructure}}</p>
    <PageNav v-bind="{ sidebarItems }" />

    <slot name="bottom" />
  </main>
</template>

<script>
import PageEdit from "@theme/components/PageEdit.vue";
import PageNav from "@theme/components/PageNav.vue";

export default {
  components: { PageEdit, PageNav },
  props: ["sidebarItems", "data"],
  data() {
    return {
      staticFileStructure: this.data || "no response"
    };
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
