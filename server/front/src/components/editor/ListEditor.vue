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
                                    <template v-if="(typeof element) === 'object'">
                                        <template v-if="element.constructor.name === 'Object'">

                                            <SubObjectEditor
                                                    :value="element"
                                                    :defaultValues="defaultValues"
                                                    :titleValue="index"
                                                    :titleLevel="subtitle"
                                                    :enums="enums"
                                                    @updateValue="updateSubValue(index,$event)"
                                                    @deleteField="deleteSubField(index,$event)"
                                            />


                                            <div style="margin-bottom:30px"/>
                                        </template>
                                        <template v-else>
                                            ERROR ! nested list
                                        </template>
                                    </template>
                                    <template v-else-if="(typeof value[key]) === 'boolean'">
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-6">
                                                <label class="checkbox"><input type="checkbox"
                                                                               name="minimum"
                                                                               id="minimum"
                                                                               :value="element"
                                                                               @input="event => updateValue(index,event.target.value)">
                                                </label>
                                            </div>

                                        </div>
                                    </template>
                                    <template v-else>
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-6">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="column is-flex">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>
                                                    <div class="column is-flex" v-if="(enums.length>0)">
                                                        <EnumEditor
                                                                :value="value[index]"
                                                                :enumList="enums"
                                                                @updateValue="updateValue(index,$event)"
                                                        />
                                                    </div>
                                                    <div class="column is-flex" v-else><input class="input"
                                                                                              type="text"
                                                                                              name="def"
                                                                                              :value="element"
                                                                                              @input="event => updateValue(index,event.target.value)"
                                                                                              placeholder="Value"/>
                                                    </div>

                                                </div>
                                            </div>


                                        </div>

                                    </template>
                                </div>
                                <div class="ml-auto">
                                    <button class="button" @click="rmElement(index)">-</button>
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
import SubObjectEditor from './SubObjectEditor.vue'
import EnumEditor from './EnumEditor.vue'


    export default {
    components:{
        SubObjectEditor,
        EnumEditor,
    },
        props: {
            value: { type: Object, required: true },
            defaultValues: { type: Object, required: true },
            titleValue:{type: String, required: true },
            titleLevel:{type: String, required: true },
            enums:{type:Array,default:() => ([])},

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
                this.$set(this.value,index,value);
                this.$emit("updateValue",{key:index,value:value});
            },
           updateSubValue(index,event){
                let tmp = this.value[index];
                tmp[event.key] = event.value;
                this.updateValue(index,tmp);
            },
            deleteSubField(index,event){
                let tmp = this.value[index];
                delete tmp[event.key];
                this.updateValue(index,tmp);
            },
            addElement(){
                let tmp = this.defaultValues;
                this.valueExpanded = true;
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