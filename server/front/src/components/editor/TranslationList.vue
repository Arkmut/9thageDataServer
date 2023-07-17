<template>
    <div class="block">
        <div class="block">
            <div class="is-flex">
                <div class="is-align-self-flex-start">
                    <h2 class="subtitle">{{language}}</h2>
                </div>

                <div class="ml-auto">
                    <input class="input" type="text" name="name"
                           :id="'newTranslationEntryName_'+language"
                           v-model="newTranslationEntryName"
                           placeholder="entry"/>
                </div>
                <div class="">
                    <button class="button" @click="addTranslationEntry(true)">+</button>
                </div>
                <div>
                    <button class="button" @click="toggleExpandTranslationsEntries"
                            v-show=" Object.keys(translations).length>0">
                        <div v-if="translationsEntriesExpanded">
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
                    <button class="button" @click="rmTranslation($event)"
                            v-show="language !== 'en'">-
                    </button>
                </div>
            </div>
            <div class="columns is-flex">

                <div class="column is-2">
                    <button class="button" @click="loadTranslation">Load LateX</button>
                </div>
                <div class="column is-2"/>
                <div class="column is-8"><textarea class="textarea" name="name" rows="3"
                                        id="latex_data"
                                        v-model="latex"
                                        placeholder="LateX values"></textarea>
                </div>
            </div>
        </div>
        <v-collapse-wrapper class="columns is-flex-direction-column">
            <div v-for="(keyLine, indexKeyLine) in Object.keys(translations)" :key="indexKeyLine"
                 v-show="translationsEntriesExpanded">
                <div class="block">
                    <div class="card">
                        <div class="card-content">

                            <div class="columns is-flex is-align-items-center">
                                <div class="column is-10">
                                    <div class="columns is-flex is-justify-content-space-evenly is-align-items-center">
                                        <div class="column is-2">
                                            <div class="subtitle is-6">{{keyLine}}
                                            </div>
                                        </div>
                                        <div class="column is-8"><textarea class="textarea" name="name" rows="3"
                                                                id="loc_line_value"
                                                                :value="translations[keyLine]"
                                                                @input="updateTranslation($event,keyLine)"
                                                                placeholder="Translation entry text"></textarea>
                                        </div>

                                    </div>
                                </div>

                                <div class="ml-auto">
                                    <button class="button"
                                            @click="rmTranslationEntry( $event,keyLine)">-
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div :id="'endTranslationEntry_'+language"></div>
        </v-collapse-wrapper>
    </div>

</template>
<script>
    export default {
        props: {
            translations: { type: Object, required: true },
            language:{type: String, required: true},
        },
        data() {
            return {
                translationsEntriesExpanded : false,
                newTranslationEntryName: "entry",
                latex:"",
               
            }
        },
        methods: {
            

            rmTranslation(){
                this.$emit('rmTranslation',this.language);
            },

            addTranslationEntry(manual){
                if(this.newTranslationEntryName in this.translations){
                    return;
                }
                this.$emit('addTranslationEntry',{key:this.newTranslationEntryName,value:""});
                this.newTranslationEntryName="entry";
                if(manual){
                    //this.translationsEntriesExpanded=true;
                    //let elmnt =document.getElementById('endTranslationEntry_'+this.language);
                    //elmnt.scrollIntoView(true);
                }
            },
            rmTranslationEntry(event,keyLine){
                this.$emit('rmTranslationEntry', keyLine);
               this.translationsEntriesExpanded = Object.keys(this.translations).length>0;

            },
            toggleExpandTranslationsEntries(){
                this.translationsEntriesExpanded = !this.translationsEntriesExpanded;
                if(this.translationsEntriesExpanded){
                    let elmnt =document.getElementById('endTranslationEntry_'+this.language);
                    elmnt.scrollIntoView(true);


                }
            },
            updateTranslation(event,keyLine){
                this.$emit('addTranslationEntry',{key:keyLine,value:event.target.value});
            },
            async loadTranslation(){
                try {
                    // Send a POST request to the API
                       const response =  await this.$http.post('http://localhost:8000/api/army_list/parse_translation', {
                        latex:this.latex
                        });
                    for(let i =0;i<Object.keys(response.data).length;i++){
                        let key= Object.keys(response.data)[i];
                        this.newTranslationEntryName =key;
                        if(!(key in this.translations)){
                            this.addTranslationEntry(false);
                        }
                        this.updateTranslation({target:{value:response.data[key]}},key);

                    }

                } catch (error) {
                    // Log the error
                    console.log(error);
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