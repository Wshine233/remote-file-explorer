<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>Select Date Time</v-card-title>
      <v-card-text>
        <v-text-field v-model="date" variant="outlined" label="Date" density="compact" type="date"></v-text-field>
        <div style="display: flex; align-items: stretch">
          <v-text-field v-model="hour" variant="outlined" type="number" label="Hour" density="compact" readonly style="margin-right: 5px" @focusin="focus = 'hour'"></v-text-field>
          <div class="time-symbol">:</div>
          <v-text-field v-model="minute" variant="outlined" type="number" label="Minute" density="compact" readonly style="margin: 0 5px" @focusin="focus = 'minute'"></v-text-field>
          <div class="time-symbol">:</div>
          <v-text-field v-model="second" variant="outlined" type="number" label="Second" density="compact" readonly style="margin-left: 5px" @focusin="focus = 'second'"></v-text-field>
        </div>
        <v-slider v-model="value" :max="max" :min="min" step="1" color="primary" hide-details thumb-label></v-slider>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Cancel</v-btn>
        <v-btn text @click="submit" :disabled="!valid">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DateTimePicker",
  emits: ['input'],
  data(){
    return {
      dialog: false,
      date: '',
      hour: 0,
      minute: 0,
      second: 0,
      focus: 'hour',
      value: 0
    }
  },
  computed:{
    max(){
      switch (this.focus){
        case 'hour':
          return 23;
        case 'minute':
          return 59;
        case 'second':
          return 59;
      }
    },
    min(){
      switch (this.focus){
        case 'hour':
          return 0;
        case 'minute':
          return 0;
        case 'second':
          return 0;
      }
    },
    dateTime(){
      let d = new Date(this.date);
      return new Date(d.getFullYear(), d.getMonth(), d.getDate(), this.hour, this.minute, this.second);
    },
    valid(){
      return !isNaN(this.dateTime.getTime());
    }
  },
  methods:{
    submit(){
      this.$emit('input', this.dateTime);
      console.log(this.dateTime)
      this.dialog = false;
    },
    setDateTime(d){
      this.date = d.toISOString().substr(0, 10);
      this.hour = d.getHours();
      this.minute = d.getMinutes();
      this.second = d.getSeconds();
    }
  },
  watch:{
    value(val){
      switch (this.focus){
        case 'hour':
          this.hour = val;
          break;
        case 'minute':
          this.minute = val;
          break;
        case 'second':
          this.second = val;
          break;
      }
    },
    focus(val){
      switch (val){
        case 'hour':
          this.value = this.hour;
          break;
        case 'minute':
          this.value = this.minute;
          break;
        case 'second':
          this.value = this.second;
          break;
      }
    },
    dialog(val){
      if (val){
        this.focus = 'hour';
        this.value = this.hour
      }
    }
  }
}
</script>

<style scoped>
.flex-row-align-center{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.time-symbol{
  padding-top: 6px;
  font-weight: bold;
}
</style>
