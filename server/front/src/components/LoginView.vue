<template>
    <section class="hero is-link is-fullheight">
        <div class="hero-body">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-5-tablet is-4-desktop is-3-widescreen">
                        <form action="" class="box">
                            <div class="field">
                                <label for="" class="label">User</label>
                                <div class="control has-icons-left">
                                    <input v-model="userName" type="email" placeholder="Username" class="input">
                                    <span class="icon is-small is-left">
                  <i class="fa fa-user"></i>
                </span>
                                </div>
                            </div>
                            <div class="field">
                                <label for="" class="label">Password</label>
                                <div class="control has-icons-left">
                                    <input v-model="passwordLogin" type="password" placeholder="*******" class="input">
                                    <span class="icon is-small is-left">
                  <i class="fa fa-lock"></i>
                </span>
                                </div>
                            </div>
                            <div class="field">
                                <button v-bind:class="'button '+ loginClass" @click="doLogin">
                                    Login
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>


    export default {
        components: {

        },
        data() {
            return {
                loginClass:"is-link",
                userName:"",
                passwordLogin:"",
            }
        },
        methods: {
            async doLogin() {
                 if (this.userName === "" || this.passwordLogin === "") {
                    this.loginClass = "is-failure";
                 } else {
                    try {
                        // Send a POST request to the API
                       await this.$http.post('http://localhost:8000/api/login',{username:this.userName,password:this.passwordLogin},{
                          headers: {
                            'Content-Type': 'application/json'
                          }});
                        this.loginClass = "is-link";
                        this.$router.push({ path: `/`});
                    } catch (error) {
                        // Log the error
                        console.log(error);
                    }
                 }
              },
            


        },
        created() {
            
        }
    }


























</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}























</style>