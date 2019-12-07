<template>
  <main class="page">
    <slot name="top" />

    <Content class="theme-default-content" />

    <div v-if="formatPage">
      <a
        class="theme-default-content"
        href="/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt"
        target="_blank"
      >/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt</a>
      <p class="theme-default-content">{{timeDirChildren}}</p>
      <select name="LeaveType" @change="timeDirOnchange()" v-model="selectedTimeDir">
        <option disabled value>Please select one</option>
        <option v-for="dir in timeDirNames">{{dir}}</option>
      </select>
      <span>Selected: {{ selectedTimeDir }}</span>
      <div v-if="timeDirChildren.length !== 0">
        <select name="LeaveType" @change="timeDirChildOnchange()" v-model="selectedTimeDirChild">
          <option disabled value>Please select one</option>
          <option v-for="dir in timeDirChildren">{{dir}}</option>
        </select>
        <span>Selected: {{ selectedTimeDirChild }}</span>
      </div>
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
      staticFileStructure: this.staticFileStructure,
      selectedTimeDir: "",
      selectedTimeDirChild: "",
      timeDirChildren: []
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
    },
    timeDirNames: function() {
      return this.timeDirs.map(function(dir) {
        return dir.name;
      });
    },
    timeDirNames: function() {
      return this.timeDirs.map(function(dir) {
        return dir.name;
      });
    },
    formatPage: function() {
      let formats = ["htmldark", "htmllight", "plaintext", "csv"];
      return formats.indexOf(this.frontmatter.type) > -1;
    }
  },
  methods: {
    timeDirOnchange: function() {
      let vm = this;
      this.timeDirChildren = this.timeDirs
        .filter(function(dir) {
          return dir.name == vm.selectedTimeDir;
        })[0]
        .children.map(function(dir) {
          return dir.name;
        });
    },
    timeDirChildOnchange: function() {}
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
