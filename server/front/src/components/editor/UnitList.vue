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
                                <div class="column is-6">
                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                        <div class=""><input class="input" type="text" name="name"
                                                             id="unit_name"
                                                             v-model="unit.name"
                                                             placeholder="Special unit name"/>
                                        </div>
                                        <div class=""><input class="input" type="text" name="def"
                                                             id="unit_def"
                                                             v-model="unit.definition"
                                                             placeholder="Special unit definition"/>
                                        </div>

                                    </div>
                                </div>

                                <div class="ml-auto">
                                    <button class="button" @click="rmUnit($event,unit.name)">-
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="endUnits"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
    export default {
        props: {
            titleUnitList: { type: String, required: true },
            units: { type: Array, required: true },
        },
        data() {
            return {
                unitsExpanded: false,
               
            }
        },
        methods: {
            
           toggleExpandUnits(){
                this.unitsExpanded = !this.unitsExpanded;

            },
            
            addUnit(){
                this.$emit('add',{name:"",units:""});
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