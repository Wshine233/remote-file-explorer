<template>
    <label :for="name" :class="{'label-focus': !idle}">{{ label }}</label>
    <input v-model="value" :type="type" :name="name" ref="input" @focusin="isFocus = true" @focusout="isFocus = false">
    <fieldset :class="{'fieldset-focus': isFocus}">
      <legend :class="{'legend-hidden': idle}">{{ label }}</legend>
    </fieldset>
</template>

<script>
export default {
  name: "InputField",
  props: {
    label: String,
    type: String,
    name: String,
  },
  data() {
    return{
      isFocus: false,
      value: ""
    }
  },
  computed: {
    idle() {
      return !this.isFocus && this.value.length === 0;
    }
  }
}
</script>

<style scoped>
*{
  --border-normal: 1px;
  --border-focus: 3px;
  --small-font: 0.75rem;
}

input{
  position: relative;
  width: calc(100% - 20px);
  height: 100%;
  border: none;
  border-radius: 10px;
  padding: 0 10px;
  margin: 0;

  font-size: 1rem;

  background: none;
  z-index: 1;
}

input:focus{
  outline: none;
}

label{
  position: absolute;
  top: 50%;
  left: 0;
  margin-left: 10px;
  color: gray;

  transform: translate(0, calc(-50% - 1px));
  transition: all 0.2s;
  z-index: 0;
}

.label-focus{
  top: 0;
  margin-left: 12px;
  font-size: var(--small-font);
  z-index: 2;
}

legend{
  height: var(--small-font);
  font-size: var(--small-font);
  margin: 0 10px;
  opacity: 0;

  transition: all 0.1s;
}

.legend-hidden{
  opacity: 0;
  max-width: 0;
  /*margin: 0;*/
  padding: 0;
}


fieldset {
  position: absolute;
  left: 0;
  top: 0;
  width: calc(100%);
  height: calc(100% + var(--small-font) / 2 - var(--border-normal));
  padding: 0;
  margin: 0;
  margin-inline: 0;
  padding-block: 0;
  padding-inline: 0;

  border-width: var(--border-normal);
  border-radius: 10px;
  border-style: solid;

  transform: translate(calc(0px - var(--border-normal)), calc(0px - var(--small-font) / 2));
  /*transition: all 0.1s;*/
}

.fieldset-focus {
  height: calc(100% + var(--small-font) / 2 - var(--border-focus));
  /*border-color: #aaaaaa;*/
  border-width: var(--border-focus);

  transform: translate(calc(0px - var(--border-focus)), calc(0px - var(--small-font) / 2));
}

</style>