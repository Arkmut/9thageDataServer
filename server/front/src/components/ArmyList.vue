<template>
    <div class="columns is-flex-direction-column">
        <div class="column" v-if="isLoggedIn">
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
        <div class="column" v-else>

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

                            <div class="columns">
                                <div class="column">
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
                                <div class="ml-auto" v-show="isLoggedIn">
                                    <div class="columns is-flex is-flex-direction-row is-align-items-center">
                                        <div class="column">
                                            <template v-if="!isPublic(army)">
                                                <button class="card-header-icon" aria-label="public"
                                                        data-tooltip="Make this version public"
                                                        @click="makePublic(army)">
                                      <span class="icon">
                                        <i class="far fa-star" aria-hidden="true"></i>

                                      </span>
                                                </button>
                                            </template>
                                            <template v-else>
                                        <span class="icon">
                                        <i class="fas fa-star" aria-hidden="true"></i>

                                      </span>
                                            </template>
                                        </div>
                                        <div class="column">

                                            <button class="card-header-icon" aria-label="delete"
                                                    data-tooltip="Delete"
                                                    @click="deleteArmy(army)">
                                      <span class="icon">
                                        <i class="fas fa-trash" aria-hidden="true"></i>

                                      </span>
                                            </button>

                                        </div>
                                    </div>
                                </div>
                            </div>
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
                public_armies: {},
                name: '',
                version: '',
                isLoggedIn:false,
            }
        },
        methods: {
            async getData() {
                try {
                    // fetch armies
                    const response = await this.$http.get('http://localhost:8000/api/army_list');
                    // set the data returned as armies
                    this.armies = response.data['armies'];
                    this.public_armies = response.data['publicArmies'];
                    if(this.armies == null){
                        this.armies = [];
                    }
                    if(this.public_armies == null){
                        this.public_armies = {};
                    }
                    console.log("armies",this.armies,this.public_armies,response.data);

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
            async deleteArmy(army) {
                try {
                    // Send a POST request to the API
                    await this.$http.post('http://localhost:8000/api/army_list/delete_army', {
                        name: army.name,
                        version: army.version
                        });
                    // update data
                    this.getData();

                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            editArmy(army) {
            console.log(army);
                this.$router.push({ path: `/army/${army.name}/${army.version}`});
            },
            async loggedIn(){
                 const response = await this.$http.get('http://localhost:8000/api/is_logged_in');
                this.isLoggedIn= response.data["loggedIn"];
                this.$forceUpdate();
            },
            isPublic(army){
                return this.public_armies != null && (army.name in this.public_armies) && army.version===this.public_armies[army.name];
            },
            async makePublic(army){
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/army_list/set_current_version', {
                        name: army.name,
                        version: army.version
                        });
                    if(response.status == 200){
                        this.public_armies[army.name]=army.version;
                    }
                    this.$forceUpdate();

                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
        },
        created() {
            // Fetch armies on page load
            this.loggedIn();
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