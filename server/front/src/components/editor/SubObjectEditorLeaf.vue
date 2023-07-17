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
                <div v-for="(key) in Object.keys(optionalValuesModified)" :key="key">
                    <template v-if="isOptionForHere(key,false)">
                        <div class="">
                            <button class="button" @click="addField(key,optionalValuesModified[key])">add
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
                                        <div>Can't nest anymore!!</div>
                                    </template>
                                    <template v-else-if="(typeof value[key]) === 'boolean'">
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-11">
                                                <CheckboxEditor
                                                        :value="value[key]"
                                                        :label="key"
                                                        @input="valueEvt => updateValue(key,valueEvt)"
                                                />

                                            </div>
                                        </div>
                                    </template>
                                    <template v-else-if="(typeof value[key]) === 'number'">
                                        <div class="columns is-flex is-align-items-center">
                                            <div class="column is-flex is-11">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="column is-flex is-4">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>

                                                    <div class="column is-flex is-8"><input class="input"
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
                                            <div class="column is-flex is-11">
                                                <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                    <div class="column is-flex is-4">
                                                        <label>
                                                            {{key}}
                                                        </label>
                                                    </div>
                                                    <div class="column is-flex is-8" v-if="(key in enums)">
                                                        <EnumEditor
                                                                :value="value[key]"
                                                                :enumList="enums[key]"
                                                                @updateValue="updateValue(key,$event)"
                                                        />
                                                    </div>
                                                    <div class="column is-flex is-8" v-else><input class="input"
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
                                     v-show="key in optionalValuesModified && isOptionForHere(key,true)">
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
import CheckboxEditor from './CheckboxEditor.vue'
import EnumEditor from './EnumEditor.vue'

    export default {
    name: "SubObjectEditorLeaf",
    components:{
        EnumEditor,
        CheckboxEditor,

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
                defaultValuesModified:{},
                optionalValuesModified:{},
            }
        },
        methods: {
            isOptionForHere(key,removal){
                if(key in this.value){
                    return removal;
                }
                console.log("optional key end: ",key ,this.optionalValuesModified[key]);

                if((typeof this.optionalValuesModified[key]) === 'object'){
                    if( !(key in this.defaultValuesModified) || !(this.optionalValuesModified[key].constructor.name === 'Object')){
                        return true;
                    }else{
                        return false;
                    }
                }else{
                    return true;
                }
            },

           toggleExpandValue(){
                this.valueExpanded = !this.valueExpanded;

            },

            updateValue(key,value){
                let v = value;
                if((typeof this.value[key]) === 'boolean'){
                    v = !!v;
                }
                if((typeof this.value[key]) === 'number'){
                    v = Number(v);
                }
                this.$emit("updateValue",{key:key,value:v});
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
                if(key in this.optionalValuesModified){
                    return this.optionalValuesModified[key];
                }else{
                    return {}
                }
            },

        },
        created(){
        console.log("end: ",this.enums,this.optionalValues);
            if(this.defaultValues != null){
                this.defaultValuesModified=JSON.parse(JSON.stringify(this.defaultValues));
            }
            for(const item of Object.entries(this.defaultValuesModified)){
                const key = item[0];
                //const value = item[1];

                if (typeof this.defaultValuesModified[key] === 'object') {
                    if('bsonType' in this.defaultValuesModified[key]){
                        if(this.defaultValuesModified[key]['bsonType'] ==='array'){
                            this.defaultValuesModified[key] = this.defaultValuesModified[key]['default'];
                            this.updateSubValue(key,{value:[]});
                        }
                    }
                }
            }
            if(this.optionalValues != null){
                this.optionalValuesModified=JSON.parse(JSON.stringify(this.optionalValues));
            }
            for(const item of Object.entries(this.optionalValuesModified)){
                const key = item[0];
                //const value = item[1];

                if (typeof this.optionalValuesModified[key] === 'object') {
                    if('bsonType' in this.optionalValuesModified[key]){
                        if(this.optionalValuesModified[key]['bsonType'] ==='array'){
                            this.defaultValuesModified[key] = this.optionalValuesModified[key]['default'];
                            this.optionalValuesModified[key]=[];
                            console.log("opt modified: ",key);
                        }
                    }
                }
            }
        }

    }






































</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}






































</style>