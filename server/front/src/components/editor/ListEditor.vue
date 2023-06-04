<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 :class="titleLevel">{{titleValue}}</h1>
                </div>
                <div class="ml-auto">
                    <button class="button" @click="addElement">+</button>
                </div>

                <div class="" v-show="value.length>0">
                    <button class="button" @click="toggleExpandValue">
                        <div v-if="valueExpanded">
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
            <div v-for="(element,index) in value" :key="index"
                 v-show="valueExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>

                                <div class="column is-10">
                                    <div v-if="(typeof element) === 'object'">
                                        <div v-if="element.constructor.name === 'Object'">
                                            <ObjectEditor
                                                    :value="element"
                                                    :defaultValues="defaultValues"
                                                    :titleValue="index"
                                                    :titleLevel="subtitle"
                                                    @updateValue="updateSubValue(index,$event)"
                                            />
                                            <div style="margin-bottom:30px"/>
                                        </div>
                                        <div v-else>
                                            ERROR ! nested list
                                        </div>
                                    </div>
                                    <div v-else>
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-6">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="is-align-self-flex-start">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>
                                                    <div class=""><input class="input"
                                                                         type="text"
                                                                         name="def"
                                                                         :value="element"
                                                                         @input="updateValue(index,event.target.value)"
                                                                         placeholder="Value"/>
                                                    </div>

                                                </div>
                                            </div>

                                            <div class="ml-auto">
                                                <button class="button" @click="rmElement(index)">-</button>
                                            </div>
                                        </div>
                                            
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="endValue"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
import ObjectEditor from './ObjectEditor.vue'

    export default {
    components:{
        ObjectEditor,
    },
        props: {
            value: { type: Object, required: true },
            defaultValues: { type: Object, required: true },
            titleValue:{type: String, required: true },
            titleLevel:{type: String, required: true },
        },
        data() {
            return {
                valueExpanded: false,

            }
        },
        methods: {

           toggleExpandValue(){
                this.valueExpanded = !this.valueExpanded;

            },

            updateValue(index,value){
                this.$emit("updateValue",{key:index,value:value});
            },
           updateSubValue(index,event){
                let tmp = this.value;
                tmp[event.key] = event.value;
                this.updateValue(index,tmp);
            },
            addElement(){
                let tmp = this.defaultValues;
                this.$emit("addValue",tmp);
            },
            rmElement(index){
                this.$emit("rmValue",index);

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