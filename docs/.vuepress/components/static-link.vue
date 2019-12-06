<template>
  <div>
    <input v-model="message" />
    <p>{{ message }}</p>
    <datepicker :value="state.date"></datepicker>
    <a
      href="/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt"
      target="_blank"
    >/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt</a>
    <p>{{staticFileStructure}}</p>
  </div>
</template>

<script>
import Datepicker from "../../../node_modules/vuejs-datepicker";
export default {
  data() {
    return {
      message: "Hello Vue!",
      state: {
        date: new Date(2019, 9, 16)
      }
    };
  },
  computed: {
    staticFileStructure() {
      return this.$page.staticFileStructure || "no value";
    }
  },
  components: {
    Datepicker
  }
};
</script>

<style lang="stylus"></style>
