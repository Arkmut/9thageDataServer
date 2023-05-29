<template>
    <div class="columns is-flex-direction-column">
        <div class="column">
            <form v-on:submit.prevent="createArmy" class="is-flex">

                <div><input class="input" type="text" name="name" id="name" v-model="name" placeholder="Army Name">
                </div>
                <div><input class="input" type="text" name="version" id="version" v-model="version"
                            placeholder="Version"></div>
                <div>
                    <button class="button" type="submit">Add</button>
                </div>
            </form>
        </div>
        <div class="column">
            <div v-if="armies === null" class="column is-align-self-stretch is-12">
                <div class="loader-wrapper is-active">
                    <div class="loader is-loading ml-auto mr-auto custom-size"></div>
                </div>
            </div>
            <div v-else-if="armies.length === 0">
            </div>
            <div v-else>
                <div v-for="army in armies" :key="army.name">
                    <div class="block">
                        <div class="card">
                            <a @click="editArmy(army)">
                                <div class="card-content">
                                    <div class="media">
                                        <div class="media-left">
                                            <figure class="image is-48x48">
                                                <img src="https://bulma.io/images/placeholders/96x96.png"
                                                     alt="Placeholder image">
                                            </figure>
                                        </div>
                                        <div class="media-content">
                                            <p class="title is-4">
                                                {{ army.name }}
                                            </p>
                                            <p class="subtitle is-6">
                                                {{ army.version }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                // armies
                armies: null,
                name: '',
                version: '',
            }
        },
        methods: {
            async getData() {
                try {
                    // fetch armies
                    const response = await this.$http.get('http://localhost:8000/api/army_list');
                    // set the data returned as armies
                    this.armies = response.data;
                } catch (error) {
                    // log the error
                    console.error(error);
                }
            },
            async createArmy() {
                try {
                    // Send a POST request to the API
                    await this.$http.post('http://localhost:8000/api/army_list/create_army', {
                        name: this.name,
                        version: this.version
                        });
                    // update data
                    this.getData();
                    // Reset the title and description field values.
                    this.name = '';
                    this.version = '';
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            editArmy(army) {
            console.log(army);
                this.$router.push({ path: `/army/${army.name}/${army.version}`});
            },
        },
        created() {
            // Fetch armies on page load
            this.getData();
        }
    }







</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}


</style>