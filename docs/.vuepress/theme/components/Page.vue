<template>
  <main class="page">
    <slot name="top" />

    <Content class="theme-default-content" />

    <div v-if="formatPage">
      <select name="Period" @change="periodDirOnchange()" v-model="selectedPeriodDirName">
        <option disabled value>Please select the period</option>
        <option v-for="dir in periodDirNames">{{dir}}</option>
      </select>
      <span>Selected: {{ selectedPeriodDirName }}</span>
      <div v-if="displayDate">
        <select name="Date" @change="dateDirOnchange()" v-model="selectedDateDirName">
          <option disabled value>Please select the date</option>
          <option v-for="dir in dateDirNames">{{dir}}</option>
        </select>
        <span>Selected: {{ selectedDateDirName }}</span>
      </div>
      <div v-if="categoryDirs && categoryDirs.length !== 0">
        <select name="Category" @change="categoryDirOnchange()" v-model="selectedCategoryDirName">
          <option disabled value>Please select the category</option>
          <option v-for="dir in categoryDirNames">{{dir}}</option>
        </select>
        <span>Selected: {{ selectedCategoryDirName }}</span>
      </div>
      <div v-if="channelDirs && channelDirs.length !== 0">
        <select name="Channel" @change="channelOnchange()" v-model="selectedChannelDirName">
          <option disabled value>Please select the channel</option>
          <option v-for="dir in channelDirNames">{{dir}}</option>
        </select>
        <span>Selected: {{ selectedChannelDirName }}</span>
      </div>
      <p class="theme-default-content">{{selectedCategoryDirName}}</p>
      <p class="theme-default-content">{{displayFiles}}</p>
      <div>
        <a
          class="theme-default-content"
          v-bind:href="displayPath"
          target="_blank"
          v-for="displayPath in displayPaths"
        >{{displayPath}}</a>
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
      // staticFileStructure: this.staticFileStructure,
      selectedPeriodDirName: "",
      selectedPeriodDir: {},
      dateDirs: [],
      dateDirNames: [],
      selectedDateDirName: "",
      selectedDateDir: {},
      categoryDirs: [],
      categoryDirNames: [],
      selectedCategoryDirName: "",
      selectedCategoryDir: {},
      channelDirs: [],
      channelDirNames: [],
      selectedChannelDirName: "",
      selectedChannelDir: {},
      displayFiles: [],
      displayPaths: []
    };
  },
  computed: {
    frontmatter: function() {
      return this.$page.frontmatter;
    },
    format: function() {
      return this.$page.frontmatter.type;
    },
    periodDirs: function() {
      return this.staticFileStructure.children.filter(function(dir) {
        return (
          dir.type == "directory" &&
          (dir.name.startsWith("before") || dir.name.startsWith("after"))
        );
      });
    },
    periodDirNames: function() {
      return this.periodDirs.map(function(dir) {
        return dir.name;
      });
    },
    formatPage: function() {
      let vm = this;
      let formats = ["htmldark", "htmllight", "plaintext", "csv"];
      return formats.indexOf(vm.frontmatter.type) > -1;
    },
    displayDate: function() {
      return (
        this.dateDirs &&
        this.dateDirs.length !== 0 &&
        this.selectedPeriodDirName.startsWith("after")
      );
    }
  },
  methods: {
    periodDirOnchange: function() {
      let vm = this;
      let formatType = this.frontmatter.type;
      this.selectedPeriodDir = this.periodDirs.filter(function(dir) {
        return dir.name == vm.selectedPeriodDirName;
      })[0];
      if (vm.selectedPeriodDirName.startsWith("after")) {
        this.dateDirs = this.selectedPeriodDir.children;
        this.dateDirNames = this.dateDirs.map(function(dir) {
          return dir.name;
        });
      } else {
        this.categoryDirs = this.selectedPeriodDir.children.filter(function(
          dir
        ) {
          return (dir.name = vm.format);
        })[0].children;
        this.categoryDirNames = this.categoryDirs.map(function(dir) {
          return dir.name;
        });
      }
    },
    dateDirOnchange: function() {
      let vm = this;
      this.selectedDateDir = this.selectedPeriodDir.children.filter(function(
        dir
      ) {
        return dir.name == vm.selectedDateDirName;
      })[0];
      this.categoryDirs = this.selectedDateDir.children.filter(function(dir) {
        return (dir.name = vm.format);
      })[0].children;
      this.categoryDirNames = this.categoryDirs.map(function(dir) {
        return dir.name;
      });
    },
    categoryDirOnchange: function() {
      let vm = this;
      if (vm.selectedPeriodDirName.startsWith("after")) {
        this.selectedCategoryDir = this.selectedDateDir.children
          .filter(function(dir) {
            return (dir.name = vm.format);
          })[0]
          .children.filter(function(dir) {
            return dir.name == vm.selectedCategoryDirName;
          })[0];
      } else {
        this.selectedCategoryDir = this.selectedPeriodDir.children
          .filter(function(dir) {
            return (dir.name = vm.format);
          })[0]
          .children.filter(function(dir) {
            return dir.name == vm.selectedCategoryDirName;
          })[0];
      }

      this.channelDirs = this.selectedCategoryDir.children;
      this.channelDirNames = this.channelDirs.map(function(dir) {
        return dir.name;
      });
    },
    channelOnchange: function() {
      let vm = this;

      this.selectedChannelDir = this.selectedCategoryDir.children.filter(
        function(dir) {
          return dir.name == vm.selectedChannelDirName;
        }
      )[0];
      this.displayFiles = this.selectedChannelDir.children;
      this.displayPaths = this.displayFiles.map(function(file) {
        let dirPath = vm.selectedChannelDir.path
          .split("/")
          .slice(4)
          .join("/");
        return "/" + dirPath + "/" + file.name;
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
