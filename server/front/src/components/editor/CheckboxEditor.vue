<template>
    <label>

        <label class="checkbox"><input type="checkbox" v-model="model"/>
            {{label}}
        </label>
    </label>
</template>

<script>
export default {
  name: "CheckboxEditor",
  props: {
    label: String,
    value: Boolean,
  },
  computed: {
    model: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      },
    },
  },

    created(){
        console.log("checkbox: ",this.value);
    },
};

</script>
