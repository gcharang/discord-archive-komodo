<template>
  <input v-model="message" />
  <div>
    <button>Go</button>
  </div>
  <p>{{message}}</p>
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

<style lang="stylus">
button {
  display: inline-block;
  font-size: 0.9em;
  color: #fff;
  background-color: $borderColor;
  padding: 0.4em 0.8em;
  border-radius: 4px;
  transition: background-color 0.1s ease;
  box-sizing: border-box;
  border: none;

  &:hover {
    background-color: lighten($borderColor, 10%);
  }
}
</style>