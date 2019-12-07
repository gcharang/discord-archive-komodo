<template>
  <main class="page">
    <slot name="top" />

    <Content class="theme-default-content" />

    <div v-if="formatPage" class="theme-default-content">
      <select
        name="Period"
        @change="periodDirOnchange()"
        v-model="selectedPeriodDirName"
      >
        <option disabled value>Please select the period</option>
        <option v-for="dir in periodDirNames">{{ dir }}</option>
      </select>

      <div v-if="displayDate">
        <select
          name="Date"
          @change="dateDirOnchange()"
          v-model="selectedDateDirName"
        >
          <option disabled value>Please select the date</option>
          <option v-for="dir in dateDirNames">{{ dir }}</option>
        </select>
      </div>
      <div v-if="categoryDirs && categoryDirs.length !== 0">
        <select
          name="Category"
          @change="categoryDirOnchange()"
          v-model="selectedCategoryDirName"
        >
          <option disabled value>Please select the category</option>
          <option v-for="dir in categoryDirNames">{{ dir }}</option>
        </select>
      </div>
      <div v-if="channelDirs && channelDirs.length !== 0">
        <select
          name="Channel"
          @change="channelOnchange()"
          v-model="selectedChannelDirName"
        >
          <option disabled value>Please select the channel</option>
          <option v-for="dir in channelDirNames">{{ dir }}</option>
        </select>
      </div>

      <div v-for="displayPath in displayPaths">
        <ul>
          <li>
            <a
              class="theme-default-content"
              v-bind:href="displayPath"
              target="_blank"
              >{{ displayPath }}</a
            >
          </li>
        </ul>
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
    fileType: function() {
      switch (this.format) {
        case "darkhtml":
          return "html";
          break;
        case "lighthtml":
          return "html";
          break;
        case "plaintext":
          return "txt";
          break;
        case "csv":
          return "csv";
          break;
        default:
          return "html";
      }
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
      return formats.indexOf(vm.format) > -1;
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
        let dirPathArr = vm.selectedChannelDir.path.split("/").slice(4);
        let toReplace = dirPathArr.indexOf("htmldark");
        dirPathArr[toReplace] = vm.format;
        let dirPath = dirPathArr.join("/");
        let fileName = file.name.split(".")[0] + "." + vm.fileType;
        return "/" + dirPath + "/" + fileName;
      });
      this.displayPaths.sort(function(a, b) {
        return (
          a
            .split("/")
            .pop()
            .split(".")[0] -
          b
            .split("/")
            .pop()
            .split(".")[0]
        );
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
