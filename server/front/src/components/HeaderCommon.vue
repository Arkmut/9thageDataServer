<template>
    <section class="hero is-link is-medium">
        <!-- Hero head: will stick at the top -->
        <div class="hero-head" id="head">
            <nav class="navbar">
                <div class="container">
                    <div class="navbar-brand">
                        <a class="navbar-item">
                            <img src="https://www.the-ninth-age.com/squelettes/IMG/header_text_logo_gold_en.png"
                                 alt="Logo">
                        </a>
                    </div>
                    <div id="navbarMenuHeroA" class="navbar-menu">
                        <div class="navbar-end">
                            <LoginButton v-if="$route.path !== '/login'"/>


                        </div>
                    </div>
                </div>
            </nav>
        </div>

        <!-- Hero content: will be in the middle -->
        <div class="hero-body">
            <div class="container has-text-centered">
                <p class="title">
                    9th Age Army Editor
                </p>
                <p class="subtitle">
                    Build armies and rules for The 9th Age Fantasy Battles
                </p>
            </div>
        </div>

        <!-- Hero footer: will stick at the bottom -->
        <div class="hero-foot">
        </div>
    </section>

</template>
<script>
import LoginButton from './LoginButton.vue'

    export default {
        components: {
            LoginButton,
        },
        data() {
            return {

            }
        },
        methods: {


        },
        created() {

        }
    }

</script>