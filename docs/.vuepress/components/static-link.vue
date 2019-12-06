<template>
  <form>
    <h1 class="title is-1">{{form.formName}}</h1>

    <div class="field">
      <label class="label">Name</label>
      <div class="control">
        <input class="input" type="text" v-model="form.userName" />
      </div>
    </div>
  </form>
  <div>
    <button>Go</button>
  </div>
  <a
    href="/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt"
    target="_blank"
  >/before-2019-Dec-05/plaintext/ama-archive/antara-ama-july2019/1.txt</a>
</template>

<script>
export default {};
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