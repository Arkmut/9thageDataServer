<template>
    <section class="hero is-link is-fullheight">
        <div class="hero-body">
            <div class="container">
                <div class="columns is-centered">
                    <div class="column is-5-tablet is-4-desktop is-3-widescreen">
                        <form action="" class="box">
                            Logged out
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

            }
        },
        methods: {

            timeout(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },


        },
        created() {
                this.timeout(3000);
                this.$router.push({ path: `/`}).catch(()=>{});

        }
    }


























</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}























</style>