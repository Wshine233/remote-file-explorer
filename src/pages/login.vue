<template>
  <div id="register-panel">
    <h1>用户登录</h1>
    <form>
      <span ref="err" class="err-log" style="display: none">{{errMsg}}</span>
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
        <button class="action-btn" type="submit" @click.prevent="login">登录</button>
      </div>
      <div>
        <a href="register.html">没有账号？点击注册</a>
      </div>
    </form>
  </div>
</template>

<script>
import InputField from "@/components/InputField";
import {requestLogin, requestVerifySession} from "@/user-manager";
import {hashPassword} from "@/user-manager";
import {systemState} from "@/system";

export default {
  name: "LoginPage",
  components: {InputField},
  data(){
    return{
      remember: false,
      username: "",
      password: "",
      errMsg: "用户名或密码错误"
    }
  },
  methods: {
    login(){
      this.getUsername();
      this.getPassword();

      let m = this;
      requestLogin(this.username, hashPassword(this.password))
          .then(res => m.responseLogin(res))
      this.$refs["err"].style.display = "none";
    },
    responseLogin(response){
      let confirm = response.success;
      this.errMsg = response.message;
      if(!confirm){
        this.$refs["err"].style.display = "inline-block";
      }else{
        window.alert(response.message)
        window.location.href = "/test.html";
      }
    },
    getUsername(){
      this.username = this.$refs.username.value;
    },
    getPassword(){
      this.password = this.$refs.password.value;
    }
  },
  created() {
    if(systemState.currentSession === undefined) return

    requestVerifySession(systemState.currentSession)
        .then(res => {
          if(res.success){
            window.location.href = "/test.html";
          }
        })
  }
}
</script>

<style scoped>
#register-panel {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

#register-panel h1 {
  margin-top: 10px;
  margin-bottom: 30px;
  text-align: center;
}

#register-panel form {
  margin-top: 20px;
}

#register-panel form>div {
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

a{
  text-decoration: none;
  color: #42b983;
  width: 100%;
  text-align: center;
}

.err-log{
  display: inline-block;
  color: red;
  font-size: 0.8rem;
  margin-left: 5px;
  margin-top: -0.6rem;
  margin-bottom: 0.6rem;
}
</style>
