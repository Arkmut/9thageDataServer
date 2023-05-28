<template>
    <div class="columns is-flex-direction-column">
        <div v-if="army===null">
            <!-- Show a loading indicator or message -->
            Loading...
        </div>
        <div v-else>
            <nav class="navbar is-fixed-bottom is-success">
                <div class="navbar-brand"></div>
                <div class="navbar-start">
                    <a class="navbar-item">{{ army.name }}</a>
                </div>
                <div class="navbar-end">
                    <div class="navbar-item">
                        <button class="button" @click="saveArmy">Save</button>
                    </div>

                </div>
            </nav>
            <div style="margin-bottom: 60px;">
                <section class="hero is-link is-large">
                    <div class="hero-body">
                        <p class="title">
                            {{ army.name }}
                        </p>
                        <p class="subtitle">
                            {{ army.version }}
                        </p>
                    </div>
                </section>

                <section class="section small">
                    <h1 class="title">Army specific rules</h1>
                </section>

                <section class="section small">
                    <h1 class="title">Models specific rules</h1>
                </section>

                <section class="section small">
                    <h1 class="title">Hereditary spell</h1>
                </section>

                <section class="section small">
                    <h1 class="title">Special Items</h1>
                </section>

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Army organisation</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addCategory">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandCategories" v-show="army.armyOrganisation.categories.length>0">Expand</button>
                        </div>
                    </div>

                </section>

                <v-collapse-wrapper class="columns is-flex-direction-column">
                    <div v-for="(category,key) in army.armyOrganisation.categories" :key="key"
                         v-show="categoriesExpanded">
                        <div class="block">
                            <div class="card">
                                <div class="card-content">

                                    <div class="is-flex is-align-items-stretch">
                                        <div class=""><input class="input" type="text" name="name" id="name"
                                                             v-model="category.name" placeholder="Category name"/>
                                        </div>
                                        <div class="ml-auto"><input class="input" type="text" name="value" id="value"
                                                                    v-model="category.value"
                                                                    placeholder="Category value"/>
                                        </div>
                                        <div class="ml-auto">
                                            <button class="button" @click="rmCategory" :id="'rm_' + category.name">-
                                            </button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </v-collapse-wrapper>

                <section class="section small">
                    <h1 class="title">Units</h1>
                </section>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                army: null,
                categoriesExpanded: false,
            }
        },
        methods: {
            async getArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/get_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version
                        });
                    this.army = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            async saveArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/save_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version,
                        army:this.army
                        });
                    console.log(response.data);
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            toggleExpandCategories(){
                this.categoriesExpanded = !this.categoriesExpanded;
            },
            addCategory(){
                this.army.armyOrganisation.categories.push({name:"",value:""});
                this.categoriesExpanded=true;
            },
            rmCategory(event){
                console.log(event.target.id);
                for(let i =0; i<this.army.armyOrganisation.categories.length;i++){
                    if(this.army.armyOrganisation.categories[i].name === event.target.id.substring(3)){
                        this.army.armyOrganisation.categories.splice(i,1);
                        break;
                    }
                }
                this.categoriesExpanded = this.army.armyOrganisation.categories.length==0;

            },
        },
        created() {
            // Fetch armies on page load
            this.getArmy();
        }
    }































</script>