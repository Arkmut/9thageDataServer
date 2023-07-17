<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 class="title">{{titleCategoryList}}</h1>
                </div>
                <div class="ml-auto">
                    <button class="button" @click="addCategory">+</button>
                </div>
                <div>
                    <button class="button" @click="toggleExpandCategories"
                            v-show="categories.length>0">
                        <div v-if="categoriesExpanded">
                                    <span class="icon">
                                    <i class="fas fa-angle-up" aria-hidden="true"></i>
                                </span>
                        </div>
                        <div v-else>
                                    <span class="icon">
                                    <i class="fas fa-angle-down" aria-hidden="true"></i>
                                </span>
                        </div>
                    </button>
                </div>
            </div>
        </section>
        <v-collapse-wrapper class="columns is-flex-direction-column">
            <div v-for="(category,key) in categories" :key="key"
                 v-show="categoriesExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-6">
                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                        <div class=""><input class="input" type="text" name="name" id="name"
                                                             v-model="category.name"
                                                             placeholder="Category name"/>
                                        </div>
                                        <div class=""><input class="input" type="text" name="name" id="logo"
                                                             v-model="category.logo"
                                                             placeholder="Category Logo"/>
                                        </div>
                                        <div class="" v-if="category.minimum">
                                            <p>&gt;=</p>
                                        </div>
                                        <div class="" v-else>
                                            <p>&lt;=</p>
                                        </div>
                                        <div class=""><input class="input" type="number" name="value" id="value"
                                                             :value="category.value"
                                                             @input="event => updateValue(key,event.target.value)"
                                                             placeholder="Category value"/>
                                        </div>
                                        <div class="">
                                            <p>%</p>
                                        </div>

                                    </div>
                                </div>
                                <div class="column is-2"><label class="checkbox"><input type="checkbox"
                                                                                        name="minimum"
                                                                                        id="minimum"
                                                                                        v-model="category.minimum">
                                    Value is a minimum
                                </label>
                                </div>
                                <div class="ml-auto">
                                    <button class="button" @click="rmCategory($event,category.name)">-
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="endCategories"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
    export default {
        props: {
            titleCategoryList: { type: String, required: true },
            categories: { type: Array, required: true },
        },
        data() {
            return {
                categoriesExpanded: false,
               
            }
        },
        methods: {
            
           toggleExpandCategories(){
                this.categoriesExpanded = !this.categoriesExpanded;

            },
            
            addCategory(){
                this.$emit('add',{name:"",categories:"",logo:"",value:0,minimum:false});
                this.categoriesExpanded=true;

            },
            updateValue(index,value){
                let val = this.categories[index];
                if(typeof value ==="number"){
                    val.value = value;
                }else{
                    val.value = parseInt(value);
                }
                this.$set(this.categories,index,val);
            },
            rmCategory(event,name){
                for(let i =0; i<this.categories.length;i++){
                    if(this.categories[i].name === name){
                        this.$emit('rm',i);
                        break;
                    }
                }
                this.categoriesExpanded = this.categories.length>0;

            },
            

        },
        
    }






















</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}



















</style>