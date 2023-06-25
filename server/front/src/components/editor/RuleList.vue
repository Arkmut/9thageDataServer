<template>
    <div class="columns is-flex-direction-column">


        <section class="section small">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h1 class="title">{{titleRuleList}}</h1>
                </div>
                <div class="ml-auto">
                    <button class="button" @click="addRule">+</button>
                </div>
                <div>
                    <button class="button" @click="toggleExpandRules"
                            v-show="rules.length>0">
                        <div v-if="rulesExpanded">
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
            <div v-for="(rule,key) in rules" :key="key"
                 v-show="rulesExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-6">
                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                        <div class=""><input class="input" type="text" name="name"
                                                             id="rule_name"
                                                             v-model="rule.name"
                                                             placeholder="Special rule name"/>
                                        </div>
                                        <div class="">
                                            <EnumEditor
                                                    :value="rule.type"
                                                    :enumList="types"
                                                    @updateValue="updateType(rule,$event)"
                                            />
                                        </div>
                                        <div class=""><input class="input" type="text" name="def"
                                                             id="rule_def"
                                                             v-model="rule.definition"
                                                             placeholder="Special rule definition"/>
                                        </div>

                                    </div>
                                </div>

                                <div class="ml-auto">
                                    <button class="button" @click="rmRule($event,rule.name)">-
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="endRules"></div>

        </v-collapse-wrapper>


    </div>
</template>
<script>
import EnumEditor from './EnumEditor.vue'

    export default {
        components:{
            EnumEditor,
        },
        props: {
            titleRuleList: { type: String, required: true },
            rules: { type: Array, required: true },
        },
        data() {
            return {
                rulesExpanded: false,
               types:[],
            }
        },
        methods: {
            
           toggleExpandRules(){
                this.rulesExpanded = !this.rulesExpanded;

            },
            
            addRule(){
                this.$emit('add',{name:"",rules:"",type:"universal"});
                this.rulesExpanded=true;

            },
            rmRule(event,name){
                for(let i =0; i<this.rules.length;i++){
                    if(this.rules[i].name === name){
                        this.$emit('rm',i);
                        break;
                    }
                }
                this.rulesExpanded = this.rules.length>0;

            },
            async getEnums() {
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_rule_types');
                    this.types = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }

            },
            updateType(rule,event){
                this.$set(rule,'type',event);
            },
        },
        created(){
            this.getEnums();
        }
    }























</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}




















</style>