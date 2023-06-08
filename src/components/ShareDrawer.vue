<template>
  <v-layout>
    <v-navigation-drawer v-model="drawer" location="bottom" temporary touchless style="height: auto">
      <v-window v-model="step">
        <v-window-item value="password" v-if="wait || step === 'password'">
          <v-card>
            <v-card-title>Share</v-card-title>
            <v-card-text>
              <v-list-subheader>Set share password</v-list-subheader>
              <v-text-field v-model="password" :rules="passwordRule" label="Password"
                            hint="Remain empty if you don't want to set a password.">
                <template #append>
                  <v-btn icon :elevation="3" @click="randomPassword">
                    <v-icon>mdi-dice-5</v-icon>
                  </v-btn>
                </template>
              </v-text-field>
            </v-card-text>
            <v-card-actions style="padding-top: 0">
              <v-spacer></v-spacer>
              <v-btn color="info" @click="next('expire')">
                Next
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-window-item>

        <v-window-item value="expire" v-if="wait || step === 'expire'">
          <v-card>
            <v-card-title>Share</v-card-title>
            <v-card-text>
              <v-list-subheader>Set share expire time</v-list-subheader>
              <v-row>
                <v-col cols="8">
                  <v-text-field v-model="expire" label="Expire After" type="number"></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-select v-model="unit" :items="['day', 'hour', 'minute']"></v-select>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-btn color="important" @click="next('password')">
                Back
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn color="info" @click="genShare" :loading="loading">
                Next
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-window-item>

        <v-window-item value="copy" v-if="wait || step === 'copy'">
          <v-card>
            <v-card-title>Get your share link!</v-card-title>
            <v-card-text>
              <v-list-subheader>Copy the link below and share it with your friends!</v-list-subheader>
              <v-text-field v-model="shareLink" label="Share Link" readonly @click:control="copyShare"></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="info" @click="confirm" :loading="loading">
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-window-item>
      </v-window>
    </v-navigation-drawer>
  </v-layout>

  <v-snackbar v-model="popup" timeout="1000">
    <v-icon left>mdi-check</v-icon>
    <span>Share link copied!</span>
  </v-snackbar>

</template>

<script>
export default {
  name: "ShareDrawer",
  data() {
    return {
      drawer: false,
      password: "",
      passwordRule: [
        v => v.length === 0 || v.length >= 4 || 'Password must be at least 4 characters',
        v => v.length === 0 || v.length <= 16 || 'Password must be at most 16 characters',
        //只能包含数字和字母
        v => v.length === 0 || /^[a-zA-Z0-9]+$/.test(v) || 'Password can only contain letters and numbers'
      ],
      files: [],
      expire: 0,
      unit: 'day',
      shareLink: "http://localhost:8080/share/123456",

      wait: false,
      step: "password",
      loading: false,
      popup: false

    }
  },
  methods: {
    show() {
      this.drawer = true
      this.wait = false
      this.password = ""
      this.expire = 0
      this.unit = 'day'

      this.next('password')

    },
    confirm() {
      this.drawer = false
    },
    randomPassword() {
      let password = ""
      let table = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
      for (let i = 0; i < 4; i++) {
        password += table[Math.floor(Math.random() * table.length)]
      }
      this.password = password
    },
    next(step) {
      if (this.wait) return

      this.wait = true
      setTimeout(() => {
        this.step = step
      }, 100)
      setTimeout(() => {
        if (this.step !== step) {
          this.step = step
        }
        this.wait = false
      }, 350)
    },
    genShare() {
      this.loading = true
      setTimeout(() => {
        this.next('copy')
        this.loading = false
      }, 1000)
    },
    copyShare() {
      this.popup = true
    }
  }
}
</script>

<style scoped>

</style>
