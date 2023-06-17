<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 :class="titleLevel">{{titleValue}}</h1>
                </div>
                <div class="ml-auto" v-show="!alwaysExpanded">
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
                 v-show="valueExpanded || alwaysExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>
                                <div class="column is-10">
                                    <template v-if="(typeof value[key]) === 'object'">
                                        Error!! no nested component here
                                    </template>
                                    <template v-else-if="(typeof value[key]) === 'boolean'">
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-6">
                                                <label class="checkbox"><input type="checkbox"
                                                                               name="minimum"
                                                                               id="minimum"
                                                                               :value="value[key]"
                                                                               @input="event => updateValue(key,event.target.value)">
                                                    {{key}}
                                                </label>
                                            </div>
                                        </div>
                                    </template>

                                    <template v-else>
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-6">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="column is-flex">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>
                                                    <div class="column is-flex" v-if="(key in enums)">
                                                        <EnumEditor
                                                                :value="value[key]"
                                                                :enumList="enums[key]"
                                                                @updateValue="updateValue(key,$event)"
                                                        />
                                                    </div>
                                                    <div class="column is-flex" v-else><input class="input"
                                                                                              type="text"
                                                                                              name="def"
                                                                                              :value="value[key]"
                                                                                              @input="event => updateValue(key,event.target.value)"
                                                                                              placeholder="Value"/>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </template>

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
import EnumEditor from './EnumEditor.vue'

    export default {
    name: "SubObjectEditor",
    components:{
        EnumEditor,
    },
        props: {
            value: { type: Object, required: true },
            defaultValues: { type: Object, required: true },
            titleValue:{type: String, required: true },
            titleLevel:{type: String, required: true },
            alwaysExpanded:{type:Boolean,default:false},
            enums:{type:Object,default:() => ({})},
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


        },

    }





































</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}


































</style>