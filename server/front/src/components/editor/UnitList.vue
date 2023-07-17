<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 class="title">{{titleUnitList}}</h1>
                </div>
                <div class="ml-auto">
                    <button class="button" @click="addUnit">+</button>
                </div>
                <div>
                    <button class="button" @click="toggleExpandUnits"
                            v-show="units.length>0">
                        <div v-if="unitsExpanded">
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
            <div v-for="(unit,key) in units" :key="key"
                 v-show="unitsExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-1"/>
                                <div class="column is-10">

                                    <ObjectEditor
                                            :value="unit"
                                            :defaultValues="defaultUnit"
                                            :optionalValues="optionalUnit"
                                            :titleValue="unit.name"
                                            :titleLevel="'subtitle'"
                                            :enums="enumUnit"
                                            @updateValue="addToObject(unit,$event)"
                                            @deleteField="deleteField(unit,$event)"
                                    />
                                </div>
                                <div class="ml-auto">
                                    <button class="button" @click="duplicateUnit(unit)"><span class="icon">
                                    <i class="fas fa-copy" aria-hidden="true"></i>
                                </span>
                                    </button>
                                </div>
                                <div class="">
                                    <button class="button" @click="rmUnit($event,unit.name)">-
                                    </button>
                                </div>

                            </div>
                            <div style="margin-bottom:30px"/>

                        </div>
                    </div>
                </div>
            </div>
            <div id="endUnits"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
import ObjectEditor from './ObjectEditor.vue'
    export default {
        props: {
            titleUnitList: { type: String, required: true },
            units: { type: Array, required: true },
        },
        components: {
            ObjectEditor,
        },
        data() {
            return {
                unitsExpanded: false,
                defaultUnit:{
                    categories:"",
                    profile:{
                        global:{rules:{bsonType:"array",default:{name:"",equipment:false}}},
                        defense:{rules:{bsonType:"array",default:{name:"",equipment:false}}},
                        offenses:{
                            name:"",
                            attacks:"",
                            offensiveSkill:"",
                            strength:"",
                            ap:"",
                            agility:"",
                            rules:{bsonType:"array",default:{name:"",equipment:false}},
                        },
                    },
                    options:{
                        bsonType:"array","default":{globalName:"",globalPrice:"",values:{ bsonType:"array","default":{name:"",price:""}}}
                    },
                },
                enumUnit:{
                },
               optionalUnit:{
                    restrictions:{
                        maxPerArmy:1,
                        sharedMaxPerArmy:1,
                        maxModelsPerArmy:0,
                        specialNote:"",
                    },
                    categoryChange:{
                        "condition":"",
                    },
                    "maxunitsize":0,
                    "costpermodel":0,

                    options:{
                        isMount:true,
                        isMagic:true,
                        isCommandGroup:true,
                    },
                    modelRules:{
                        bsonType:"array","default":{name:"",rules:"",type:"universal"}
                    },
                    paths:{
                        bsonType:"array","default":""
                    },
                },
            }
        },
       created() {
            this.getEnums();
        },
        methods: {
           async getEnums(){
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_unit_types');
                    this.enumUnit['type'] = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_rule_types');
                    this.enumUnit['modelRules'] ={'type': response.data};
                } catch (error) {
                    // Log the error
                    console.log(error);
                }

                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_unit_heights');
                    this.enumUnit['height'] = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
           },
            
           toggleExpandUnits(){
                this.unitsExpanded = !this.unitsExpanded;

            },
            addToObject(obj, element){
                this.$set(obj,element.key,element.value);
           },
           deleteField(obj, element){
                this.$delete(obj,element.key);
           },
            addUnit(){
                this.$emit('add',
                    {
                        name:"",categories:[],cost:0,unitSize:1,type:"infantry",height:"standard",
                        baseSize:{width:20,depth:20},
                        profile:
                            {
                                global:
                                    {
                                        advanceRate:"",
                                        marchRate:"",
                                        discipline:"",
                                        rules:[],
                                    },
                                defense:
                                    {
                                        hp:"",
                                        defensiveSkill:"",
                                        resistance:"",
                                        armour:"",
                                        rules:[],
                                    },
                                offenses:[],
                            },
                            options:[],
                    });
                this.unitsExpanded=true;

            },
            duplicateUnit(unit){
                this.$emit('add',
                    JSON.parse(JSON.stringify(unit)));
                this.unitsExpanded=true;

            },
            rmUnit(event,name){
                for(let i =0; i<this.units.length;i++){
                    if(this.units[i].name === name){
                        this.$emit('rm',i);
                        break;
                    }
                }
                this.unitsExpanded = this.units.length>0;

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