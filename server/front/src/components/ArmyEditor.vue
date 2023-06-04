<template>
    <div class="columns is-flex-direction-column">
        <div v-if="army===null" class="column is-align-self-stretch is-12">
            <div class="loader-wrapper is-active">
                <div class="loader is-loading ml-auto mr-auto custom-size"></div>
            </div>
        </div>
        <div v-else>
            <nav class="navbar is-fixed-bottom is-success">
                <div class="navbar-brand"></div>
                <div class="navbar-start">
                    <a class="navbar-item">{{ army.name }}</a>
                </div>
                <div class="navbar-end">
                    <div class="navbar-item">
                        <button class="button" @click="saveArmy">Save</button>
                    </div>

                </div>
            </nav>
            <div style="margin-bottom: 120px;">
                <section class="hero is-link is-large">
                    <div class="hero-body">
                        <p class="title">
                            {{ army.name }}
                        </p>
                        <p class="subtitle">
                            {{ army.version }}
                        </p>
                    </div>
                </section>
                <!-- Army specific rules -->

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Army specific rules</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addArmyRule">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandArmyRules"
                                    v-show="army.armyRules.rules.length>0">
                                <div v-if="armyRulesExpanded">
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
                    <div v-for="(rule,key) in army.armyRules.rules" :key="key"
                         v-show="armyRulesExpanded">
                        <div class="block">
                            <div class="card">
                                <div class="card-content">

                                    <div class="columns is-flex is-align-items-center">
                                        <div class="column is-6">
                                            <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                <div class=""><input class="input" type="text" name="name"
                                                                     id="army_rule_name"
                                                                     v-model="rule.name"
                                                                     placeholder="Special rule name"/>
                                                </div>
                                                <div class=""><input class="input" type="text" name="def"
                                                                     id="army_rule_def"
                                                                     v-model="rule.definition"
                                                                     placeholder="Special rule definition"/>
                                                </div>

                                            </div>
                                        </div>

                                        <div class="ml-auto">
                                            <button class="button" @click="rmArmyRule($event,rule.name)">-
                                            </button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="endArmyRules"></div>

                </v-collapse-wrapper>

                <!-- Model specific rules-->

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Model specific rules</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addModelRule">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandModelRules"
                                    v-show="army.modelRules.rules.length>0">
                                <div v-if="modelRulesExpanded">
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
                    <div v-for="(rule,key) in army.modelRules.rules" :key="key"
                         v-show="modelRulesExpanded">
                        <div class="block">
                            <div class="card">
                                <div class="card-content">

                                    <div class="columns is-flex is-align-items-center">
                                        <div class="column is-6">
                                            <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                <div class=""><input class="input" type="text" name="name"
                                                                     id="modelRule_name"
                                                                     v-model="rule.name"
                                                                     placeholder="Special rule name"/>
                                                </div>
                                                <div class=""><input class="input" type="text" name="def"
                                                                     id="modelRule_def"
                                                                     v-model="rule.definition"
                                                                     placeholder="Special rule definition"/>
                                                </div>

                                            </div>
                                        </div>

                                        <div class="ml-auto">
                                            <button class="button" @click="rmModelRule($event,rule.name)">-
                                            </button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="endModelRules"></div>

                </v-collapse-wrapper>
                <!-- Hereditary spell-->

                <section class="section small">
                    <h1 class="title">Hereditary spell</h1>
                </section>
                <!-- Special items-->

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Special items</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addSpecialItem">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandSpecialItems"
                                    v-show="army.specialItems.items.length>0">
                                <div v-if="specialItemsExpanded">
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
                    <div v-for="(item,key) in army.specialItems.items" :key="key"
                         v-show="specialItemsExpanded">
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
                                            <button class="button" @click="rmSpecialItem($event,item.name)">-
                                            </button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="endItems"></div>

                </v-collapse-wrapper>

                <!-- Army Organisation-->
                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Army organisation</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addCategory">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandCategories"
                                    v-show="army.armyOrganisation.categories.length>0">
                                <div v-if="categoriesExpanded">
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
                    <div v-for="(category,key) in army.armyOrganisation.categories" :key="key"
                         v-show="categoriesExpanded">
                        <div class="block">
                            <div class="card">
                                <div class="card-content">

                                    <div class="columns is-flex is-align-items-center">
                                        <div class="column is-6">
                                            <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                <div class=""><input class="input" type="text" name="name" id="name"
                                                                     v-model="category.name"
                                                                     placeholder="Category name"/>
                                                </div>
                                                <div class="" v-if="category.minimum">
                                                    <p>&lt;=</p>
                                                </div>
                                                <div class="" v-else>
                                                    <p>&gt;=</p>
                                                </div>
                                                <div class=""><input class="input" type="number" name="value" id="value"
                                                                     v-model="category.value"
                                                                     placeholder="Category value"/>
                                                </div>
                                                <div class="">
                                                    <p>%</p>
                                                </div>

                                            </div>
                                        </div>
                                        <div class="column is-2"><label class="checkbox"><input type="checkbox"
                                                                                                name="minimum"
                                                                                                id="minimum"
                                                                                                v-model="category.minimum">
                                            Value is a minimum
                                        </label>
                                        </div>
                                        <div class="ml-auto">
                                            <button class="button" @click="rmCategory($event,category.name)">-
                                            </button>
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div id="endCategories"></div>
                </v-collapse-wrapper>

                <!-- units-->

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Units</h1>
                        </div>
                        <div class="ml-auto">
                            <button class="button" @click="addUnit">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandUnits"
                                    v-show="army.armyList.units.length>0">
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
                    <div v-for="(unit,key) in army.armyList.units" :key="key"
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
                                                                     placeholder="Unit name"/>
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

                <!-- translations-->

                <section class="section small">
                    <div class="is-flex">
                        <div class="is-align-self-flex-start">
                            <h1 class="title">Translations</h1>
                        </div>
                        <div class="ml-auto">
                            <input class="input" type="text" name="name"
                                   id="newTranslationName"
                                   v-model="newTranslationName"
                                   placeholder="Language"/>
                        </div>
                        <div class="">
                            <button class="button" @click="addTranslation">+</button>
                        </div>
                        <div>
                            <button class="button" @click="toggleExpandTranslations"
                                    v-show="Object.keys(army.loc).length>0">
                                <div v-if="translationsExpanded">
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
                    <div v-for="(key) in Object.keys(army.loc)" :key="key"
                         v-show="translationsExpanded">
                        <div class="block">
                            <div class="is-flex">
                                <div class="is-align-self-flex-start">
                                    <h2 class="subtitle">{{key}}</h2>
                                </div>
                                <div class="ml-auto">
                                    <input class="input" type="text" name="name"
                                           :id="'newTranslationEntryName_'+key"
                                           v-model="newTranslationEntryName[key]"
                                           placeholder="Language"/>
                                </div>
                                <div class="">
                                    <button class="button" @click="addTranslationEntry(key)">+</button>
                                </div>
                                <div>
                                    <button class="button" @click="toggleExpandTranslationsEntries(key)"
                                            v-show=" Object.keys(army.loc[key]).length>0">
                                        <div v-if="translationsEntriesExpanded[key]">
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
                                <div class="">
                                    <button class="button" @click="rmTranslation($event,key)"
                                            v-show="key !== 'en'">-
                                    </button>
                                </div>
                            </div>
                        </div>
                        <v-collapse-wrapper class="columns is-flex-direction-column">
                            <div v-for="(keyLine, indexKeyLine) in Object.keys(army.loc[key])" :key="indexKeyLine"
                                 v-show="translationsEntriesExpanded[key]">
                                <div class="block">
                                    <div class="card">
                                        <div class="card-content">

                                            <div class="columns is-flex is-align-items-center">
                                                <div class="column is-6">
                                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                                        <div class="">
                                                            <div class="subtitle is-6">{{keyLine}}
                                                            </div>
                                                        </div>
                                                        <div class=""><input class="input" type="text" name="name"
                                                                             id="loc_line_value"
                                                                             v-model="army.loc[key][keyLine]"
                                                                             placeholder="Translation entry text"/>
                                                        </div>

                                                    </div>
                                                </div>

                                                <div class="ml-auto">
                                                    <button class="button"
                                                            @click="rmTranslationEntry( $event,key,keyLine)">-
                                                    </button>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div :id="'endTranslationEntry_'+key"></div>
                        </v-collapse-wrapper>
                    </div>
                    <div id="endTranslations"></div>
                </v-collapse-wrapper>


            </div>
        </div>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                army: null,
                categoriesExpanded: false,
                armyRulesExpanded: false,
                modelRulesExpanded: false,
                specialItemsExpanded: false,
                unitsExpanded: false,
                translationsExpanded: false,
                translationsEntriesExpanded : {},
                newTranslationName: "Language",
                newTranslationEntryName: {"en":"entry"},
            }
        },
        methods: {
            async getArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/get_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version
                        });
                    this.army = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            async saveArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/save_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version,
                        army:this.army
                        });
                    console.log(response.data);
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            toggleExpandCategories(){
                this.categoriesExpanded = !this.categoriesExpanded;
                if(this.categoriesExpanded){
                    let elmnt =document.getElementById('endCategories');
                    elmnt.scrollIntoView(true);


                }
            },
            
            addCategory(){
                this.army.armyOrganisation.categories.push({name:"",value:""});
                this.categoriesExpanded=true;
                let elmnt =document.getElementById('endCategories');
                elmnt.scrollIntoView(true);
            },
            rmCategory(event,name){
                for(let i =0; i<this.army.armyOrganisation.categories.length;i++){
                    if(this.army.armyOrganisation.categories[i].name === name){
                        this.army.armyOrganisation.categories.splice(i,1);
                        break;
                    }
                }
                this.categoriesExpanded = this.army.armyOrganisation.categories.length>0;

            },
           toggleExpandArmyRules(){
                this.armyRulesExpanded = !this.armyRulesExpanded;

            },
            
            addArmyRule(){
                this.army.armyRules.rules.push({name:"",value:""});
                this.armyRulesExpanded=true;

            },
            rmArmyRule(event,name){
                for(let i =0; i<this.army.armyRules.rules.length;i++){
                    if(this.army.armyRules.rules[i].name === name){
                        this.army.armyRules.rules.splice(i,1);
                        break;
                    }
                }
                this.armyRulesExpanded = this.army.armyRules.rules.length>0;

            },
            toggleExpandModelRules(){
                this.modelRulesExpanded = !this.modelRulesExpanded;

            },
            
            addModelRule(){
                this.army.modelRules.rules.push({name:"",value:""});
                this.modelRulesExpanded=true;
                
            },
            rmModelRule(event,name){
                for(let i =0; i<this.army.modelRules.rules.length;i++){
                    if(this.army.modelRules.rules[i].name === name){
                        this.army.modelRules.rules.splice(i,1);
                        break;
                    }
                }
                this.modelRulesExpanded = this.army.modelRules.rules.length>0;

            },
            toggleExpandSpecialItems(){
                this.specialItemsExpanded = !this.specialItemsExpanded;
                if(this.specialItemsExpanded){
                    let elmnt =document.getElementById('endItems');
                    elmnt.scrollIntoView(true);


                }
            },
            
            addSpecialItem(){
                this.army.specialItems.items.push({name:"",value:""});
                this.specialItemsExpanded=true;
                let elmnt =document.getElementById('endItems');
                elmnt.scrollIntoView(true);
            },
            rmSpecialItem(event,name){
                for(let i =0; i<this.army.specialItems.items.length;i++){
                    if(this.army.specialItems.items[i].name === name){
                        this.army.specialItems.items.splice(i,1);
                        break;
                    }
                }
                this.specialItemsExpanded = this.army.specialItems.items.length>0;

            },
            toggleExpandUnits(){
                this.unitsExpanded = !this.unitsExpanded;
                if(this.unitsExpanded){
                    let elmnt =document.getElementById('endUnits');
                    elmnt.scrollIntoView(true);


                }
            },
            
            addUnit(){
                this.army.armyList.units.push({name:""});
                this.unitsExpanded=true;
                let elmnt =document.getElementById('endUnits');
                elmnt.scrollIntoView(true);
            },
            rmUnit(event,name){
                for(let i =0; i<this.army.armyList.units.length;i++){
                    if(this.army.armyList.units[i].name === name){
                        this.army.armyList.units.splice(i,1);
                        break;
                    }
                }
                this.unitsExpanded = this.army.armyList.units.length>0;

            },

            
            addTranslation(){
                if(this.newTranslationName in this.army.loc){
                    return;
                }
                this.$set(this.army.loc,this.newTranslationName,{});
                this.newTranslationEntryName[this.newTranslationName]="entry";
                this.newTranslationName = "Language"

                this.translationsExpanded=true;
                let elmnt =document.getElementById('endTranslations');
                elmnt.scrollIntoView(true);
            },
            rmTranslation(event,key){
                this.$delete(this.army.loc, key);
                this.translationsExpanded = Object.keys(this.army.loc).length>0;

            },
            toggleExpandTranslations(){
                this.translationsExpanded = !this.translationsExpanded;
                if(this.translationsExpanded){
                    let elmnt =document.getElementById('endTranslations');
                    elmnt.scrollIntoView(true);


                }
            },
            
            addTranslationEntry(key){
                if(key in this.army.loc[key]){
                    return;
                }
                this.$set(this.army.loc[key],this.newTranslationEntryName[key],"");
                this.newTranslationEntryName[key]="entry";
                this.translationsEntriesExpanded[key]=true;
                let elmnt =document.getElementById('endTranslationEntry_'+key);
                elmnt.scrollIntoView(true);
            },
            rmTranslationEntry(event,key,keyLine){

               this.$delete(this.army.loc[key],keyLine);
               this.translationsEntriesExpanded[key] = this.army.loc[key].length>0;

            },
            toggleExpandTranslationsEntries(key){
            console.log("toggle: "+key);
                this.translationsEntriesExpanded[key] = !(key in this.translationsEntriesExpanded) || !this.translationsEntriesExpanded[key];
                if(this.translationsEntriesExpanded[key]){
                    let elmnt =document.getElementById('endTranslationEntry_'+key);
                    elmnt.scrollIntoView(true);


                }
            },

        },
        created() {
            // Fetch armies on page load
            this.getArmy();
        }
    }




















</script>
<style>
.custom-size {
  height: 64px;
  width: 64px;
}

















</style>