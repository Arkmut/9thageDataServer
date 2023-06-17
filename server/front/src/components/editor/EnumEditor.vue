<template>
    <div class="dropdown is-active">
        <div class="dropdown-trigger">
            <button class="button" aria-haspopup="true" @click="toggleExpandValue"
                    aria-controls="dropdown-menu">
                <span>{{value}}</span>
                <span class="icon is-small">
                                                                        <i class="fas fa-angle-down"
                                                                           aria-hidden="true"></i>
                                                                    </span>
            </button>
        </div>
        <div class="dropdown-menu" role="menu">
            <div class="dropdown-content" v-for="(val,key) in enumList" :key="key"
                 v-show="valueExpanded">
                <a v-if="value === val" class="dropdown-item is-active" @click="event => updateValue(val)">
                    {{val}}
                </a>
                <a v-else class="dropdown-item" @click="event => updateValue(val)">
                    {{val}}
                </a>
            </div>
        </div>
    </div>
</template>
<script>

    export default {
    name: "EnumEditor",
    components:{
    },
        props: {
            value: { required: true },
            enumList: { type: Array, required: true },

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

            updateValue(value){
                this.$emit("updateValue",value);
                this.valueExpanded=false;
            },
            timeout(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
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