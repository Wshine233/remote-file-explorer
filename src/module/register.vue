<template>
  <div id="register-panel">
    <h1>用户注册</h1>
    <form>
      <span ref="user-err" class="err-log" style="display: none">{{errMsgUser}}</span>
      <div id="username-div" class="input-field">
        <InputField label="用户名" type="text" name="username" ref="username"
                    :validator="validateUsername" @inputChange="(name) => this.username = name"/>
      </div>
      <span ref="pass-err" class="err-log" style="display: none">{{errMsgPass}}</span>
      <div id="password-div" class="input-field">
        <InputField label="密码" type="password" name="password" ref="password"
                    :validator="validatePassword" @inputChange="(pass) => this.password = pass"/>
      </div>
      <span ref="confirm-err" class="err-log" style="display: none">{{errMsgConfirm}}</span>
      <div id="password-confirm-div" class="input-field">
        <InputField label="确认密码" type="password" name="password" ref="password"
                    :validator="validatePasswordConfirm" @inputChange="(val) => this.passwordConfirm = val"/>
      </div>
      <div>
        <div class="check-box">
          <input type="checkbox" name="remember-me" id="remember-me"/>
          <label for="remember-me">我同意 <a ref="protocol" href="" @click.prevent="popupProtocol">用户使用协议</a></label>
        </div>
      </div>
      <div>
        <button class="action-btn" type="submit" @click.prevent="submit">确认注册</button>
      </div>
      <div>
        <a href="login">已有账号？点击登录</a>
      </div>
    </form>
  </div>
</template>

<script>
import InputField from "@/components/InputField.vue";

export default {
  name: "RegisterPage",
  components:{
    InputField
  },
  data(){
    return {
      username: "",
      password: "",
      passwordConfirm: "",
      errMsgUser: "用户名长度不得小于4",
      errMsgPass: "密码长度不得小于6或大于16",
      errMsgConfirm: "两次密码输入不一致"
    }
  },
  methods: {
    popupProtocol(){
      window.alert("这里以后要写一个弹出框组件代替alert");
    },
    validateUsername(){
      return this.username.length >= 4;
    },
    validatePassword(){
      return this.password.length >= 6 && this.password.length <= 16;
    },
    validatePasswordConfirm(){
      return this.password === this.passwordConfirm;
    },
    submitValidate(){
      let valid = true;
      if(!this.validateUsername()){
        this.errMsg = "用户名长度不得小于4";
        this.$refs['user-err'].style.display = "inline-block";
        valid = false;
      }else{
        this.$refs['user-err'].style.display = "none";
      }
      if(!this.validatePassword()){
        this.errMsg = "密码长度不得小于6或大于16";
        this.$refs["pass-err"].style.display = "inline-block";
        valid = false;
      }else{
        this.$refs["pass-err"].style.display = "none";
      }
      if(!this.validatePasswordConfirm()){
        this.errMsg = "两次密码输入不一致";
        this.$refs["confirm-err"].style.display = "inline-block";
        valid = false;
      }else{
        this.$refs["confirm-err"].style.display = "none";
      }
      return valid;
    },
    submit(){
      if(this.submitValidate()){
        this.$refs["user-err"].style.display = "none";
        this.$refs["pass-err"].style.display = "none";
        this.$refs["confirm-err"].style.display = "none";
        alert("注册成功")
      }
    }
  },
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

#register-panel form > div {
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

.action-btn {
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

.action-btn:hover {
  filter: brightness(1.1);
}

.check-box {
  display: flex;
  flex-direction: row;
  align-items: center;
}

input[type=checkbox] {
  margin-right: 5px;
  width: 1.2rem;
  height: 1.2rem;
}

label {
  transform: translate(0, -1px);
  user-select: none;
}

a {
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