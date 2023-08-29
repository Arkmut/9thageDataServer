<template>
    <div class="columns is-flex-direction-column">
        <div v-if="army===null" class="column is-align-self-stretch is-12">
            <div class="loader-wrapper is-active">
                <div class="loader is-loading ml-auto mr-auto custom-size"></div>
            </div>
        </div>
        <div v-else>
            <nav class="navbar is-fixed-bottom is-link">
                <div class="navbar-brand"></div>
                <div class="navbar-start">
                    <a class="navbar-item">{{ army.name }}</a>
                </div>
                <div class="navbar-end">
                    <div class="navbar-item">
                        <button :class="{ 'button is-success': saveSuccess==='success','button is-danger': saveSuccess==='failure', button: true }"
                                @click="saveArmy">
                            <template v-if="startDownloading">
                                <div class="loader-wrapper is-active">
                                    <div class="loader is-loading ml-auto mr-auto custom-size-spinner"></div>
                                </div>
                            </template>
                            <template v-else>
                                Save
                            </template>
                        </button>
                        <button class="button" @click="downloadArmy(false)" v-show="army.name!==translationName">
                            <template v-if="startDownloading">
                                <div class="loader-wrapper is-active">
                                    <div class="loader is-loading ml-auto mr-auto custom-size-spinner"></div>
                                </div>
                            </template>
                            <template v-else>
                                Download PDF
                            </template>
                        </button>
                        <button class="button" @click="downloadArmy(true)" v-show="army.name!==translationName">
                            <template v-if="startDownloading">
                                <div class="loader-wrapper is-active">
                                    <div class="loader is-loading ml-auto mr-auto custom-size-spinner"></div>
                                </div>
                            </template>
                            <template v-else>
                                Download Latex
                            </template>
                        </button>
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
                <div class="columns is-flex is-vcentered" v-show="army.name!==translationName">
                    <div class="column is-11">
                        <h1 class="title">Release Date</h1>
                        <datepicker placeholder="Select Date" v-model="date"></datepicker>
                    </div>
                </div>
                <!-- Army specific rules -->
                <RuleList :rules="army.armyRules.rules" titleRuleList="Army Specific rules"
                          @add="addToArray(army.armyRules.rules,$event)"
                          @rm="rmFromArray(army.armyRules.rules,$event)" v-show="army.name!==translationName"/>
                <!-- Model specific rules-->
                <RuleList :rules="army.modelRules.rules" titleRuleList="Model Specific rules"
                          @add="addToArray(army.modelRules.rules,$event)"
                          @rm="rmFromArray(army.modelRules.rules,$event)" v-show="army.name!==translationName"/>

                <!-- Hereditary spell-->
                <div class="columns is-flex is-vcentered">
                    <div class="column is-11">
                        <ObjectEditor
                                :value="army.hereditarySpell"
                                :defaultValues="defaultHereditarySpell"
                                :optionalValues="optionalHereditary"
                                :titleValue="'Hereditary Spell'"
                                :titleLevel="'title'"
                                :enums="enumHereditary"
                                @updateValue="addToObject(army.hereditarySpell,$event)"
                                @deleteField="deleteField(army.hereditarySpell,$event)"
                                v-show="army.name!==translationName &&  army.hasOwnProperty('hereditarySpell')"
                        />
                        <h1 class="title"
                            v-show="army.name!==translationName && !(army.hasOwnProperty('hereditarySpell'))">No
                            Hereditary</h1>
                    </div>
                    <div class="ml-auto" v-show="army.name!==translationName">
                        <template v-if="army.hasOwnProperty('hereditarySpell')">
                            <button class="button" @click="rmFromObject(army,'hereditarySpell')">-
                            </button>
                        </template>
                        <template v-else>
                            <button class="button"
                                    @click="addToObject(army,{key:'hereditarySpell',value:{name: '', castingValue: {base: 0},range: 0,types: [],duration: 'oneTurn',effect: ''}})">
                                +
                            </button>
                        </template>

                    </div>
                </div>

                <!-- Special items-->
                <ItemList :items="army.specialItems.items" titleItemList="Special items"
                          @add="addToArray(army.specialItems.items,$event)"
                          @rm="rmFromArray(army.specialItems.items,$event)" v-show="army.name!==translationName"/>


                <!-- Army Organisation-->
                <CategoryList :categories="army.armyOrganisation.categories"
                              titleCategoryList="Army organisation"
                              @add="addToArray(army.armyOrganisation.categories,$event)"
                              @rm="rmFromArray(army.armyOrganisation.categories,$event)"
                              v-show="army.name!==translationName"/>

                <!-- units-->
                <UnitList :units="army.armyList.units" titleUnitList="Units"
                          @add="addToArray(army.armyList.units,$event)"
                          @rm="rmFromArray(army.armyList.units,$event)" v-show="army.name!==translationName"/>

                <!-- translations-->
                <LanguageList :translations="army.loc"
                              @addTranslation="addToObject(army.loc,$event)"
                              @rmTranslation="rmFromObject(army.loc,$event)"
                              @addTranslationEntry="addToObject(army.loc[$event.keyTrans],$event)"
                              @rmTranslationEntry="rmFromObject(army.loc[$event.keyTrans],$event.key)"
                />

            </div>
        </div>
    </div>
</template>
<script>
import RuleList from './editor/RuleList.vue'
import ItemList from './editor/ItemList.vue'
import CategoryList from './editor/CategoryList.vue'
import UnitList from './editor/UnitList.vue'
import LanguageList from './editor/LanguageList.vue'
import ObjectEditor from './editor/ObjectEditor.vue'
import moment from 'moment';
import Datepicker from 'vuejs-datepicker';

    export default {
        components: {
            Datepicker,
            RuleList,
            ItemList,
            CategoryList,
            UnitList,
            LanguageList,
            ObjectEditor,
        },
        data() {
            return {
            translationName:'global_translation',
                date:null,
                army: null,
                defaultHereditarySpell:{
                    castingValue:{
                        "base":0,
                    },
                    types:"",
                },
                enumHereditary:{
                },
                optionalHereditary:{
                    castingValue:{
                        "boosted":0,
                    },
                },
                saveSuccess:'',
                startDownloading:false,

            }
        },
        methods: {
            async getEnums() {
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_spell_types');
                    this.enumHereditary['types'] = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
                try {
                    // Send a POST request to the API
                    const response = await this.$http.post('http://localhost:8000/api/get_spell_durations');
                    this.enumHereditary['duration'] = response.data;
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            async getArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/get_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version
                        });
                    this.army = response.data;
                    this.date = moment(this.army['date'], 'DD/MM/yyyy').toDate();
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
            },
            async saveArmy() {
                try {
                    let army = JSON.parse(JSON.stringify(this.army));
                    delete army["_id"];
                    army['date'] = moment(this.date).format('DD/MM/yyyy');
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/save_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version,
                        army:army
                        });
                    console.log(response.data);
                    this.saveSuccess="success";
                    setTimeout((function() {
                        this.saveSuccess = '';
                      }).bind(this), 1500);
                } catch (error) {
                    // Log the error
                    console.log(error);
                    this.saveSuccess="failure";
                    setTimeout((function() {
                        this.saveSuccess = '';
                      }).bind(this), 1500);
                }
            },
            async downloadArmy(isLatex) {
                try {
                    // Send a POST request to the API
                    this.startDownloading = true;
                        const response = await this.$http.post('http://localhost:8000/api/army_list/download_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version,
                        latex:isLatex
                        }, {
                          headers: {
                            'Content-Type': 'application/json', // Set the content type here
                          },
                            responseType: 'arraybuffer', // Set the response type to arraybuffer to receive binary data
                        });
                    const blob = new Blob([response.data], { type: 'application/force-download' })
                    const disposition = response.headers['content-disposition'];
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    const filename = matches !== null && matches[1] ? matches[1].replace(/['"]/g, '') : 'filename.zip';
                    const link = document.createElement('a')
                    link.href = URL.createObjectURL(blob)
                    link.download = filename
                    link.click()
                    URL.revokeObjectURL(link.href)
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
                this.startDownloading = false;
            },
           addToArray(array, element){
            array.push(element);
           },
           rmFromArray(array, index){
            array.splice(index,1);
           },
           addToObject(obj, element){
                this.$set(obj,element.key,element.value);
           },
           rmFromObject(obj, key){
               this.$delete(obj,key);
           },
            


        },
        created() {
            this.getEnums();
            // Fetch armies on page load
            this.getArmy();
        }
    }











</script>
<style>
.custom-size-spinner {
  height: 16px;
  width: 16px;
}
































</style>