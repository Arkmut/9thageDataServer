<template>
    <div class="columns is-flex-direction-column">


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
                            v-show="Object.keys(translations).length>0">
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
            <div v-for="(key) in Object.keys(translations)" :key="key"
                 v-show="translationsExpanded">
                <TranslationList :translations="translations[key]"
                                 :language="key"
                                 @rmTranslation="rmTranslation($event)"
                                 @addTranslationEntry="$emit('addTranslationEntry',{keyTrans:key, key:$event.key,value:$event.value})"
                                 @rmTranslationEntry="$emit('rmTranslationEntry',{keyTrans:key, key:$event})"
                />
                <div style="margin-bottom:60px"/>
            </div>
            <div id="endTranslations"></div>
        </v-collapse-wrapper>


    </div>
</template>
<script>
import TranslationList from './TranslationList.vue'

    export default {
    components: {
            TranslationList,

        },
        props: {
            translations: { type: Object, required: true },
        },
        data() {
            return {
               translationsExpanded: false,
                newTranslationName: "Language",

            }
        },
        methods: {
            
           addTranslation(){
                if(this.newTranslationName in this.translations){
                    return;
                }
                this.$emit('addTranslation',{key:this.newTranslationName,value:{}});
                this.newTranslationName = "Language"

                this.translationsExpanded=true;
                let elmnt =document.getElementById('endTranslations');
                elmnt.scrollIntoView(true);
            },
            rmTranslation(key){
                this.$emit('rmTranslation',key);
                this.translationsExpanded = Object.keys(this.translations).length>0;

            },
            toggleExpandTranslations(){
                this.translationsExpanded = !this.translationsExpanded;
                if(this.translationsExpanded){
                    let elmnt =document.getElementById('endTranslations');
                    elmnt.scrollIntoView(true);


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