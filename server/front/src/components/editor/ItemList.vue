<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 class="title">{{titleItemList}}</h1>
                </div>
                <div class="ml-auto">
                    <button class="button" @click="addItem">+</button>
                </div>
                <div>
                    <button class="button" @click="toggleExpandItems"
                            v-show="items.length>0">
                        <div v-if="itemsExpanded">
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
            <div v-for="(item,key) in items" :key="key"
                 v-show="itemsExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>
                                <div class="column is-10">

                                    <ObjectEditor
                                            :value="item"
                                            :defaultValues="defaultItem"
                                            :titleValue="item.name"
                                            :titleLevel="'subtitle'"
                                            :enums="enumItem"
                                            @updateValue="addToObject(item,$event)"
                                    />
                                </div>

                                <div class="ml-auto">
                                    <button class="button" @click="rmItem($event,item.name)">-
                                    </button>
                                </div>

                            </div>
                            <div style="margin-bottom:30px"/>

                        </div>
                    </div>
                </div>
            </div>
            <div id="endItems"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
import ObjectEditor from './ObjectEditor.vue'

    export default {
        props: {
            titleItemList: { type: String, required: true },
            items: { type: Array, required: true },
        },
        components: {
            ObjectEditor,
        },
        data() {
            return {
                itemsExpanded: false,
                defaultItem:{
                    support:"",
                },
                enumItem:{
                },
               
            }
        },
        created() {
            this.getItemTypes();
        },
        methods: {
           async getItemTypes(){
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_item_types');
                    this.enumItem['type'] = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
           },
           toggleExpandItems(){
                this.itemsExpanded = !this.itemsExpanded;

            },
            addToObject(obj, element){
                this.$set(obj,element.key,element.value);
           },
            addItem(){
                this.$emit('add',{name:"",type:"weapon",cost:0,support:[],maxNb:1,dominant:false,restriction:"",rules:""});
                this.itemsExpanded=true;

            },
            rmItem(event,name){
                for(let i =0; i<this.items.length;i++){
                    if(this.items[i].name === name){
                        this.$emit('rm',i);
                        break;
                    }
                }
                this.itemsExpanded = this.items.length>0;

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