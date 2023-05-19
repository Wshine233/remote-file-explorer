<template>
  <div id="login-panel">
    <h1>用户登录</h1>
    <form action="" method="post">
      <div id="username-div" class="input-field">
        <InputField label="用户名" type="text" name="username" ref="username"/>
      </div>
      <div id="password-div" class="input-field">
        <InputField label="密码" type="password" name="password" ref="password"/>
      </div>
      <div>
        <div class="check-box">
          <input type="checkbox" name="remember-me" id="remember-me"/>
          <label for="remember-me">自动登录</label>
        </div>
      </div>
      <div>
        <button class="action-btn" type="submit" @click="login">登录</button>
      </div>
    </form>
  </div>
</template>

<script>
import InputField from "@/components/InputField";
export default {
  name: "LoginPage",
  components: {InputField},
  data(){
    return{
      remember: false,
      username: "",
      password: ""
    }
  },
  methods: {
    login(){
      this.getUsername();
      this.getPassword();
      window.alert("username: " + this.username + "\npassword: " + this.password)
    },
    getUsername(){
      this.username = this.$refs.username.value;
    },
    getPassword(){
      this.password = this.$refs.password.value;
    }
  }
}
</script>

<style scoped>
#login-panel {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

#login-panel h1 {
  margin-top: 10px;
  margin-bottom: 30px;
  text-align: center;
}

#login-panel form {
  margin-top: 20px;
}

#login-panel form>div {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.input-field {
  position: relative;
  /*background: #42b983;*/
  height: 2.6rem;
}

.action-btn{
  width: 100%;
  height: 2.6rem;
  border: none;
  border-radius: 5px;
  background: #42b983;
  color: white;
  font-size: 1rem;
  cursor: pointer;

  transition: all 0.2s;
}

.action-btn:hover{
  filter: brightness(1.1);
}

.check-box{
  display: flex;
  flex-direction: row;
  align-items: center;
}

input[type=checkbox]{
  margin-right: 5px;
  width: 1.2rem;
  height: 1.2rem;
}

label{
  transform: translate(0, -1px);
  user-select: none;
}
</style>