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
                        <button class="button" @click="saveArmy">Save</button>
                        <button class="button" @click="downloadArmy">Download PDF</button>
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

                <RuleList :rules="army.armyRules.rules" titleRuleList="Army Specific rules"
                          @add="addToArray(army.armyRules.rules,$event)"
                          @rm="rmFromArray(army.armyRules.rules,$event)"/>
                <!-- Model specific rules-->
                <RuleList :rules="army.modelRules.rules" titleRuleList="Model Specific rules"
                          @add="addToArray(army.modelRules.rules,$event)"
                          @rm="rmFromArray(army.modelRules.rules,$event)"/>

                <!-- Hereditary spell-->

                <ObjectEditor
                        :value="army.hereditarySpell"
                        :defaultValues="defaultHereditarySpell"
                        :optionalValues="optionalHereditary"
                        :titleValue="'Hereditary Spell'"
                        :titleLevel="'title'"
                        :enums="enumHereditary"
                        @updateValue="addToObject(army.hereditarySpell,$event)"
                        @deleteField="deleteField(army.hereditarySpell,$event)"
                />
                <!-- Special items-->
                <ItemList :items="army.specialItems.items" titleItemList="Special items"
                          @add="addToArray(army.specialItems.items,$event)"
                          @rm="rmFromArray(army.specialItems.items,$event)"/>


                <!-- Army Organisation-->
                <CategoryList :categories="army.armyOrganisation.categories"
                              titleCategoryList="Army organisation"
                              @add="addToArray(army.armyOrganisation.categories,$event)"
                              @rm="rmFromArray(army.armyOrganisation.categories,$event)"/>

                <!-- units-->
                <UnitList :units="army.armyList.units" titleUnitList="Units"
                          @add="addToArray(army.armyList.units,$event)"
                          @rm="rmFromArray(army.armyList.units,$event)"/>

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

    export default {
        components: {
            RuleList,
            ItemList,
            CategoryList,
            UnitList,
            LanguageList,
            ObjectEditor,
        },
        data() {
            return {
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
            async downloadArmy() {
                try {
                    // Send a POST request to the API
                        const response = await this.$http.post('http://localhost:8000/api/army_list/download_army', {
                        name: this.$route.params.name,
                        version: this.$route.params.version
                        }, {
                          headers: {
                            'Content-Type': 'application/json', // Set the content type here
                          },
                            responseType: 'arraybuffer', // Set the response type to arraybuffer to receive binary data
                        });
                    const blob = new Blob([response.data], { type: 'application/pdf' })
                    const disposition = response.headers['content-disposition'];
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    const filename = matches !== null && matches[1] ? matches[1].replace(/['"]/g, '') : 'filename.pdf';
                    const link = document.createElement('a')
                    link.href = URL.createObjectURL(blob)
                    link.download = filename
                    link.click()
                    URL.revokeObjectURL(link.href)
                } catch (error) {
                    // Log the error
                    console.log(error);
                }
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
.custom-size {
  height: 64px;
  width: 64px;
}
























</style>