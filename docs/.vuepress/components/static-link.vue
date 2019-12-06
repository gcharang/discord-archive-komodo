<template>
  <div class="collapsed">
    <input v-model="message" />
    <p>{{ message }}</p>
  </div>
</template>


<script>
export default {
  data() {
    return {
      message: "Hello Vue!"
    };
  }
};
</script>

<style lang="stylus"></style>