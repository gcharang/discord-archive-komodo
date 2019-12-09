<template>
  <main class="page">
    <slot name="top" />
    <v-container fluid v-if="formatPage" class="theme-default-content">
      <blockquote
        class="blockquote"
      >Please make a selection using the menus below to see the available {{format.toUpperCase()}} archives.</blockquote>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="periodDirNames"
            label="Please select the period"
            @change="periodDirOnchange()"
            v-model="selectedPeriodDirName"
          ></v-select>
        </v-col>

        <v-col v-if="displayDate" class="d-flex" cols="12" sm="6">
          <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-right="40"
            transition="scale-transition"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on }">
              <v-text-field v-model="selectedDate" label="Please select a Date" readonly v-on="on"></v-text-field>
            </template>
            <v-date-picker
              no-title
              :allowed-dates="allowedDates"
              @change="dateDirOnchange()"
              v-model="selectedDate"
              :min="minDateInPicker"
              :max="maxDateInPicker"
              full-width
              @input="menu = false"
            ></v-date-picker>
          </v-menu>
        </v-col>

        <v-col v-if="categoryDirs && categoryDirs.length !== 0" class="d-flex" cols="12" sm="6">
          <v-select
            :items="categoryDirNames"
            label="Please select the category"
            @change="categoryDirOnchange()"
            v-model="selectedCategoryDirName"
          ></v-select>
        </v-col>
        <v-col v-if="channelDirs && channelDirs.length !== 0" class="d-flex" cols="12" sm="6">
          <v-select
            :items="channelDirNames"
            label="Please select the channel"
            @change="channelOnchange()"
            v-model="selectedChannelDirName"
          ></v-select>
        </v-col>
      </v-row>

      <blockquote
        v-if="displayPaths.length != 0"
        class="blockquote"
      >Below is a list of files that satisfy the above selection.</blockquote>

      <v-row no-gutters class="mb-2" align="center">
        <v-col v-for="displayPath in displayPaths" cols="12">
          <v-btn
            block
            color="secondary"
            dark
            :href="displayPath"
            target="_blank"
            class="mb-2"
          >{{ displayPath }}</v-btn>
        </v-col>
      </v-row>
    </v-container>

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
      menu: false,
      selectedPeriodDirName: "",
      selectedPeriodDir: {},
      dateDirs: [],
      dateDirNames: [],
      selectedDate: "",
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
    },
    minDateInPicker: function() {
      let dateObj = new Date(this.dateDirNames[0]);
      let dateString = new Date(
        dateObj.getTime() - dateObj.getTimezoneOffset() * 60000
      )
        .toISOString()
        .split("T")[0];
      return dateString;
    },
    maxDateInPicker: function() {
      let dateObj = new Date(this.dateDirNames[this.dateDirNames.length - 1]);
      let dateString = new Date(
        dateObj.getTime() - dateObj.getTimezoneOffset() * 60000
      )
        .toISOString()
        .split("T")[0];
      return dateString;
    }
  },
  methods: {
    periodDirOnchange: function() {
      let vm = this;
      this.dateDirs = [];
      this.selectedDate = "";
      this.categoryDirs = [];
      this.selectedCategoryDirName = "";
      this.channelDirs = [];
      this.selectedChannelDirName = "";
      this.displayPaths = [];
      this.selectedPeriodDir = this.periodDirs.filter(function(dir) {
        return dir.name == vm.selectedPeriodDirName;
      })[0];
      if (vm.selectedPeriodDirName.startsWith("after")) {
        this.dateDirs = this.selectedPeriodDir.children;
        this.dateDirNames = this.dateDirs
          .map(function(dir) {
            return dir.name;
          })
          .sort(function(a, b) {
            return new Date(a) - new Date(b);
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
      this.categoryDirs = [];
      this.selectedCategoryDirName = "";
      this.channelDirs = [];
      this.selectedChannelDirName = "";
      this.displayPaths = [];
      let formatDate = function(date) {
        let dateArr = date.split("-");
        switch (dateArr[1]) {
          case "1":
            dateArr[1] = "Jan";
            break;
          case "2":
            dateArr[1] = "Feb";
            break;
          case "3":
            dateArr[1] = "Mar";
            break;
          case "4":
            dateArr[1] = "Apr";
            break;
          case "5":
            dateArr[1] = "May";
            break;
          case "6":
            dateArr[1] = "Jun";
            break;
          case "7":
            dateArr[1] = "Jul";
            break;
          case "8":
            dateArr[1] = "Aug";
            break;
          case "9":
            dateArr[1] = "Sep";
            break;
          case "10":
            dateArr[1] = "Oct";
            break;
          case "11":
            dateArr[1] = "Nov";
            break;
          case "12":
            dateArr[1] = "Dec";
            break;
          default:
            dateArr[1] = "Dec";
        }
        return dateArr.join("-");
      };

      this.selectedDateDirName = formatDate(this.selectedDate);
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
      this.channelDirs = [];
      this.selectedChannelDirName = "";
      this.displayPaths = [];
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
    },
    allowedDates: function(date) {
      let vm = this;
      let dateObj = new Date(date + " UTC");
      let dateObjGetTime = dateObj.getTime();
      let dateDirdateObjGetTimeArr = vm.dateDirNames.map(function(item) {
        return new Date(item + " UTC").getTime();
      });
      let truthiness = false;
      for (let index = 0; index < dateDirdateObjGetTimeArr.length; index++) {
        if (dateDirdateObjGetTimeArr[index] == dateObjGetTime) {
          truthiness = true;
          break;
        } else {
          truthiness = false;
        }
      }
      return truthiness;
    }
  },
  watch: {}
};
</script>

<style lang="stylus">
@require '../styles/wrapper.styl';

.v-btn {
  text-transform: none !important;
}

.page {
  padding-bottom: 2rem;
  display: block;
}
</style>
