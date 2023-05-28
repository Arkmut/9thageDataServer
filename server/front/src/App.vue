<template>
    <div class="container">

        <ArmyList  v-if="$route.path === '/'"/>
        <router-view  v-if="$route.path !== '/'"/>
    </div>
</template>

<script>
import ArmyList from './components/ArmyList.vue'
export default {
  name: 'App',
  components: {
    ArmyList
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
</style>
