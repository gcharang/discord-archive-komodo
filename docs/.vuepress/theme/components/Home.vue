<template>
  <main class="home" aria-labelledby="main-title">
    <div class="wrapper">
    <header class="hero">
      <img
        v-if="data.heroImage"
        :src="$withBase(data.heroImage)"
        :alt="data.heroAlt || 'hero'"
      >

     
      <h6 class="description">
        {{ data.tagline || $description || 'Welcome to your VuePress site' }}
      </h6>

      <p
        class="action"
        v-if="data.actionText && data.actionLink"
      >
        <NavLink
          class="action-button"
          :item="actionLink"
        />
      </p>

      <p class="description">Select a Format</p>

      <div
        class="features1"
        v-if="data.shortcuts && data.shortcuts.length"
      >        
        <div
          class="feature"
          v-for="(shortcut, index) in data.shortcuts"
          :key="index"
        >                      
          <p
              
              v-if="shortcut.title && shortcut.link"
          >
              <div>
              <button @click="$router.push(shortcut.link)">{{ shortcut.title }} →</button>
              </div>            
          </p>            
        </div>
      </div>
    </header>
    </div>

    <Content class="custom"/>    

    <div
      class="footer"
      v-if="data.footer"
    >
      {{ data.footer }}
    </div>
  </main>
</template>

<script>
import NavLink from '@theme/components/NavLink.vue'

export default {
  components: { NavLink },

  computed: {
    data () {
      return this.$page.frontmatter
    },

    actionLink () {
      return {
        link: this.data.actionLink,
        text: this.data.actionText
      }
    }           
  }
}
</script>

<style lang="stylus">
.home
  padding $navbarHeight 2rem 0
  max-width 960px
  margin 0px auto
  display flex
  flex-direction column
  min-height 100vh
  background-color #222832
  .wrapper
    display flex
    flex-wrap wrap
    align-items flex-start
    align-content stretch
    justify-content center
  .hero
    text-align center
    flex-grow 1
    flex-basis 50%
    max-width 50%
    img
      max-width: 50%
      max-height 180px
      display block
      margin 3rem auto 1.5rem
    h1
      font-size 3rem
    h1, .description, .action
      margin 1.8rem auto
    .description
      max-width 35rem
      font-size 1.6rem
      line-height 1.3
      color lighten($textColor, 40%)
    .action-button
      display inline-block
      font-size 1.2rem
      color #fff
      background-color $borderColor
      padding 0.8rem 1.6rem
      border-radius 4px
      transition background-color .1s ease
      box-sizing border-box
      border-bottom 1px solid darken($borderColor, 10%)
      &:hover
        background-color lighten($borderColor, 10%)
  .textContent
    flex-grow 1
    flex-basis 50%
    max-width 50%   
  .features,.features1
    border-top 1px solid $borderColor
    padding 1.2rem 0    
    margin-top 2.5rem
    display flex
    flex-wrap wrap
    align-items flex-start
    align-content stretch
    justify-content space-around
  .features1
    border-top 0px none $borderColor      
  .feature
    flex-grow 1
    flex-basis 25%
    max-width 25%
    h2
      font-size 1.4rem
      font-weight 500
      border-bottom none
      padding-bottom 0
      color lighten($textColor, 10%)
    p
      color lighten($textColor, 25%)      
    button 
        display inline-block
        font-size 0.9em
        color #fff
        background-color $borderColor
        padding 0.4em 0.8em
        border-radius 4px
        transition background-color .1s ease
        box-sizing border-box
        border none
        &:hover
            background-color lighten($borderColor, 10%)             
  .footer
    padding 2.5rem
    border-top 1px solid $borderColor
    text-align center
    color lighten($textColor, 25%)

@media (max-width: $MQMobile)
  .home
    .wrapper
      flex-direction column
    .features
      flex-direction column
    .feature
      max-width 100%
      padding 0 2.5rem
    .hero
      max-width 100%
      padding 0 2.5rem
    .textContent
      max-width 100%
      padding 0 2.5rem    

@media (max-width: $MQMobileNarrow)
  .home
    padding-left 1.5rem
    padding-right 1.5rem
    .hero
      max-width 100%
      padding 0 2.5rem
      img
        max-height 210px
        margin 2rem auto 1.2rem
      h1
        font-size 2rem
      h1, .description, .action
        margin 1.2rem auto
      .description
        font-size 1.2rem
      .action-button
        font-size 1rem
        padding 0.6rem 1.2rem
    .feature
      max-width 100%
      padding 0 2.5rem      
      h2
        font-size 1.25rem
    .wrapper
      flex-direction column
    .features
      flex-direction column
    .textContent
      max-width 90%
      padding 0 2.5rem      
</style>