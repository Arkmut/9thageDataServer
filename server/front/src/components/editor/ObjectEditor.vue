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

        <v-collapse-wrapper class="columns is-flex-direction-column" v-show="valueExpanded || alwaysExpanded">
            <div class="is-flex">
                <div v-for="(key) in Object.keys(optionalValues)" :key="key">
                    <template v-if="!((typeof value[key]) === 'object')">
                        <div class="">
                            <button class="button" @click="addField(key,optionalValues[key])">add
                                {{key}}
                            </button>
                        </div>
                    </template>
                </div>
            </div>
            <div v-for="(key) in Object.keys(value)" :key="key">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>
                                <div class="column is-9">
                                    <template v-if="(typeof value[key]) === 'object'">
                                        <template v-if="value[key].constructor.name === 'Object'">
                                            <ObjectEditor
                                                    :value="value[key]"
                                                    :titleValue="key"
                                                    :defaultValues="defaultValues[key]"
                                                    :optionalValues="getOptional(key)"
                                                    :titleLevel="subtitle"
                                                    :enums="enums[key]"
                                                    @updateValue="updateSubValue(key,$event)"
                                                    @deleteField="deleteFieldSubValue(key,$event)"
                                            />
                                            <div style="margin-bottom:30px"/>
                                        </template>
                                        <template v-else>
                                            <ListEditor
                                                    :value="value[key]"
                                                    :titleValue="key"
                                                    :defaultValues="defaultValues[key]"
                                                    :titleLevel="subtitle"
                                                    :enums="enums[key]"
                                                    @updateValue="updateSubValue(key,$event)"
                                                    @addValue="addValue(key,$event)"
                                                    @rmValue="rmValue(key,$event)"
                                            />
                                            <div style="margin-bottom:30px"/>
                                        </template>
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
                                    <template v-else-if="(typeof value[key]) === 'number'">
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-6">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="column is-flex">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>

                                                    <div class="column is-flex"><input class="input"
                                                                                       type="number"
                                                                                       name="def"
                                                                                       :value="value[key]"
                                                                                       @input="event => updateValue(key,Number(event.target.value))"
                                                                                       placeholder="0"/>
                                                    </div>
                                                </div>
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
                                <div class="column is-1"
                                     v-show="key in optionalValues && !((typeof value[key]) === 'object')">
                                    <button class="button" @click="deleteField(key)"
                                    >-
                                    </button>
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
import EnumEditor from './EnumEditor.vue'

    export default {
    name: "ObjectEditor",
    components:{
        ListEditor,
        EnumEditor,
    },
        props: {
            value: { type: Object, required: true },
            defaultValues: { type: Object, required: true },
            optionalValues: { type: Object, default:() => ({}) },
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
            addField(key,value){
                this.updateValue(key,value);
                this.$forceUpdate();
            },
           updateSubValue(key,event){
                let tmp = this.value[key];
                tmp[event.key] = event.value;
                this.updateValue(key,tmp);
            },
            deleteFieldSubValue(key,event){
                let tmp = this.value[key];
                delete tmp[event.key];
                this.updateValue(key,tmp);

            },
             addValue(key,event){
                let tmp = this.value[key];
                tmp.push(event);
                this.updateValue(key,tmp);
            },
            rmValue(key,index){
                let tmp = this.value[key];
                tmp.splice(index,1);
                this.updateValue(key,tmp);
            },
            deleteField(key){
                this.$emit("deleteField",{key:key});
                this.$forceUpdate();
            },
            getOptional(key){
                if(key in this.optionalValues){
                    return this.optionalValues[key];
                }else{
                    return {}
                }
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