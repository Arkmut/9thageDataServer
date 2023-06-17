<template>
    <div>
        <HeaderCommon/>
        <div class="container">

            <ArmyList v-if="$route.path === '/'"/>
            <router-view v-if="$route.path !== '/'"/>
        </div>
    </div>

</template>

<script>
import ArmyList from './components/ArmyList.vue'
import HeaderCommon from './components/HeaderCommon.vue'
export default {
  name: 'App',
  components: {
    ArmyList,
    HeaderCommon,
  },
  async mounted() {
    try {
        // Fetch crsf cookie
        const response = await this.$http.get('http://localhost:8000/api/get_token');
        this.$cookies.set('crsftoken',response.data.token);
    } catch (error) {
        // Log the error
        console.error(error);
    }

    }

}









</script>

<style>
$fade-grey: #ededed;
$grey: #ccc;
$muted-grey: #999;
$heart: #ff4f8f;
$white: #fff;
.loader-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: #fff;
  opacity: 0;
  z-index: -1;
  transition: opacity .3s;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 6px;

  .loader {
    height: 80px;
    align-self: center;
    width: 80px;
  }

  &.is-active {
    opacity: 1;
    z-index: 1;
  }
}

.is-loading {
  position: relative;
}

</style>
