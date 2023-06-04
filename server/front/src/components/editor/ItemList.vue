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
                                <div class="column is-6">
                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                        <div class=""><input class="input" type="text" name="name"
                                                             id="specialItem_name"
                                                             v-model="item.name"
                                                             placeholder="Special item name"/>
                                        </div>

                                    </div>
                                </div>

                                <div class="ml-auto">
                                    <button class="button" @click="rmItem($event,item.name)">-
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="endItems"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
    export default {
        props: {
            titleItemList: { type: String, required: true },
            items: { type: Array, required: true },
        },
        data() {
            return {
                itemsExpanded: false,
               
            }
        },
        methods: {
            
           toggleExpandItems(){
                this.itemsExpanded = !this.itemsExpanded;

            },
            
            addItem(){
                this.$emit('add',{name:"",items:""});
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