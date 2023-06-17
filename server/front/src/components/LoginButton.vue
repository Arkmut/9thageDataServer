<template>

    <span class="navbar-item">
        <template v-if="!isLoggedIn">
            <a class="button is-link is-inverted" href="/login">
                <span>Login</span>
              </a>
        </template>
        <template v-else>
             <a class="button is-link is-inverted" @click="doLogout">
                <span>Logout</span>
              </a>
        </template>
    </span>
</template>
<script>
    export default {
        components: {

        },
        data() {
            return {
                isLoggedIn:false
            }
        },
        methods: {
            async loggedIn(){
                 const response = await this.$http.get('http://localhost:8000/api/is_logged_in');
                this.isLoggedIn= response.data["loggedIn"];
                this.$forceUpdate();

            },
            async doLogout(){
                await this.$http.get('http://localhost:8000/api/logout');
                this.$router.push({ path: `/logout`}).catch(()=>{});


            },

        },
        created() {
            this.loggedIn();
        }
    }


</script>