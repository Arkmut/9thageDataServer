<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 :class="titleLevel">{{titleValue}}</h1>
                </div>
                <div class="ml-auto">
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
            <div v-for="(key) in Object.keys(value)" :key="key"
                 v-show="valueExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>
                                <div class="column is-10">
                                    <div v-if="(typeof value[key]) === 'object'">
                                        <div v-if="value[key].constructor.name === 'Object'">
                                            <ObjectEditor
                                                    :value="value[key]"
                                                    :titleValue="key"
                                                    :defaultValues="defaultValues[key]"
                                                    :titleLevel="subtitle"
                                                    @updateValue="updateSubValue(key,$event)"
                                            />
                                            <div style="margin-bottom:30px"/>
                                        </div>
                                        <div v-else>
                                            <ListEditor
                                                    :value="value[key]"
                                                    :titleValue="key"
                                                    :defaultValues="defaultValues[key]"
                                                    :titleLevel="subtitle"
                                                    @updateValue="updateSubValue(key,$event)"
                                                    @addValue="addValue(key,$event)"
                                                    @rmValue="rmValue(key,$event)"
                                            />
                                            <div style="margin-bottom:30px"/>
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
                                                                         :value="value[key]"
                                                                         @input="updateValue(key,event.target.value)"
                                                                         placeholder="Value"/>
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
            </div>
            <div id="endValue"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
import ListEditor from './ListEditor.vue'

    export default {
    name: "ObjectEditor",
    components:{
        ListEditor,
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

            updateValue(key,value){
                this.$emit("updateValue",{key:key,value:value});
            },
           updateSubValue(key,event){
                let tmp = this.value;
                tmp[event.key] = event.value;
                this.updateValue(key,tmp);
            },
             addValue(key,event){
                let tmp = this.value[key];
                tmp.push(event.value);
                this.updateValue(key,tmp);
            },
            rmValue(key,index){
                let tmp = this.value[key];
                tmp.splice(index,1);
                this.updateValue(key,tmp);
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