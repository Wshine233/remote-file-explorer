<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title style="padding-bottom: 2px">Reset Password</v-card-title>

      <v-card-text>
        <v-text-field v-model="passwordOld" label="Old Password" type="password" :rules="passwordOldRules" required></v-text-field>
        <v-text-field v-model="password" label="Password" type="password" :rules="passwordRules" required></v-text-field>
        <v-text-field v-model="passwordConfirm" label="Confirm Password" type="password" :rules="passwordConfirmRules" required></v-text-field>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="reset" :disabled="loading" :loading="loading">Reset</v-btn>
      </v-card-actions>

    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "PasswordResetDialog",
  data(){
    return {
      dialog: false,
      loading: false,
      passwordOld: "",
      password: "",
      passwordConfirm: "",
      passwordOldRules: [
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password must be at least 8 characters',
        v => v.length <= 16 || 'Password must be at most 16 characters',
      ],
      passwordRules: [
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password must be at least 8 characters',
        v => v.length <= 16 || 'Password must be at most 16 characters',
      ],
      passwordConfirmRules: [
        v => !!v || 'Password is required',
        v => v === this.password || 'Password does not match',
      ],
    }
  },
  methods: {
    reset() {
      this.loading = true
    }
  }
}
</script>

<style scoped>

</style>
