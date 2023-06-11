<template>
  <div id="register-panel">
    <h1>用户注册</h1>
    <form>
      <span ref="user-err" class="err-log" style="display: none">{{ errMsgUser }}</span>
      <div id="username-div" class="input-field">
        <InputField label="用户名" type="text" name="username" ref="username"
                    :validator="validateUsername" @inputChange="(name) => this.username = name"/>
      </div>
      <span ref="pass-err" class="err-log" style="display: none">{{ errMsgPass }}</span>
      <div id="password-div" class="input-field">
        <InputField label="密码" type="password" name="password" ref="password"
                    :validator="validatePassword" @inputChange="(pass) => this.password = pass"/>
      </div>
      <span ref="confirm-err" class="err-log" style="display: none">{{ errMsgConfirm }}</span>
      <div id="password-confirm-div" class="input-field">
        <InputField label="确认密码" type="password" name="password" ref="password"
                    :validator="validatePasswordConfirm" @inputChange="(val) => this.passwordConfirm = val"/>
      </div>
      <div>
        <div class="check-box">
          <input v-model="protocol" type="checkbox" name="remember-me" id="remember-me"/>
          <label for="remember-me">我同意 <a ref="protocol" href="" @click.prevent="popupProtocol">用户使用协议</a></label>
        </div>
      </div>
      <div>
        <button class="action-btn" type="submit" @click.prevent="submit">确认注册</button>
      </div>
      <div>
        <a href="login.html">已有账号？点击登录</a>
      </div>
    </form>
  </div>

  <Transition type="transition">
    <div v-if="protocolDialog" id="protocol" class="dialog">
      <h1>用户使用协议</h1>
      <p>{{protocolContent}}</p>
      <button class="action-btn" @click="closeProtocol">我已阅读</button>
    </div>
  </Transition>
</template>

<script>
import InputField from "@/components/InputField.vue";
import {requestRegister} from "@/user-manager";
import {hashPassword} from "@/user-manager";

export default {
  name: "RegisterPage",
  components: {
    InputField
  },
  data() {
    return {
      username: "",
      password: "",
      passwordConfirm: "",
      errMsgUser: "用户名长度不得小于4或大于12，且只能包含数字或字母以及下划线",
      errMsgPass: "密码长度不得小于6或大于16",
      errMsgConfirm: "两次密码输入不一致",
      protocol: false,

      protocolDialog: false,
      protocolContent:
        "欢迎使用远程文件管理器！在开始使用本应用程序之前，请仔细阅读以下用户使用协议。通过使用本应用程序，即表示您同意遵守以下条款和条件：\n" +
        "\n" +
        "1. 注册与账户安全：\n" +
        "   a. 为了使用远程文件管理器，您需要注册一个账户，并提供准确、最新和完整的个人信息。\n" +
        "   b. 您是唯一对您的账户负责的人，因此，您需对您的账户和密码的保密负全部责任。\n" +
        "   c. 如果您怀疑有人未经授权访问或使用您的账户，请立即通知我们。\n" +
        "\n" +
        "2. 使用权限和限制：\n" +
        "   a. 您可以使用远程文件管理器上传、下载、浏览和管理您的个人文件和文件夹。\n" +
        "   b. 您不得使用远程文件管理器传输、存储、共享或访问任何非法、侵犯他人隐私或知识产权的内容。\n" +
        "   c. 您不得通过远程文件管理器执行任何恶意活动，包括但不限于病毒传播、黑客攻击等。\n" +
        "\n" +
        "3. 数据安全和隐私：\n" +
        "   a. 我们将采取合理的技术和组织措施来保护您在远程文件管理器中存储的数据的安全。\n" +
        "   b. 您应该自行负责备份您的重要数据，以防止数据丢失或损坏。\n" +
        "   c. 我们将遵守适用的隐私法律和政策，保护您的个人信息的隐私和安全。\n" +
        "\n" +
        "4. 知识产权：\n" +
        "   a. 远程文件管理器和其中包含的所有内容（如文本、图形、图像、标志、图标、音频和视频片段等）的所有权归属于我们或我们的许可方。\n" +
        "   b. 您不得以任何方式复制、修改、分发、传播、展示、出售或使用远程文件管理器的任何部分或内容，除非事先获得我们的书面许可。\n" +
        "\n" +
        "5. 责任限制：\n" +
        "   a. 远程文件管理器仅按现有状况提供，不提供任何明示或暗示的担保或条件。\n" +
        "   b. 我们不对远程文件管理器的使用中出现的任何损失、损害或任何间接、特殊、附带或相应的损害负责。\n" +
        "   c. 我们不对由于使用或无法使用远程文件管理器而导致的数据丢失或损坏承担责任。\n" +
        "\n" +
        "6. 协议修改和终止：\n" +
        "   a. 我们保留随时修改本用户使用协议的权利。修改后\n" +
        "\n" +
        "的协议将在我们的应用程序上发布，您继续使用远程文件管理器即表示您接受修改后的协议。\n" +
        "   b. 我们保留随时终止、暂停或限制您对远程文件管理器的访问权利的权利。\n" +
        "\n" +
        "请注意，本用户使用协议构成您与我们之间关于远程文件管理器的完整协议，并取代您先前与我们之间就此事宜达成的任何口头或书面协议。如您不同意本协议的任何部分，请勿使用远程文件管理器。"
    }
  },
  methods: {
    popupProtocol() {
      this.protocolDialog = true;
    },
    closeProtocol(){
      this.protocolDialog = false;
    },
    validateUsername() {
      return this.username.length >= 4 && this.username.length <= 12 && /^[a-zA-Z0-9_]+$/.test(this.username);
    },
    validatePassword() {
      return this.password.length >= 6 && this.password.length <= 16;
    },
    validatePasswordConfirm() {
      return this.password === this.passwordConfirm;
    },
    submitValidate() {
      let valid = true;
      if (!this.validateUsername()) {
        this.errMsg = "用户名长度不得小于4或大于12，且只能包含数字或字母以及下划线";
        this.$refs['user-err'].style.display = "inline-block";
        valid = false;
      } else {
        this.$refs['user-err'].style.display = "none";
      }
      if (!this.validatePassword()) {
        this.errMsg = "密码长度不得小于6或大于16";
        this.$refs["pass-err"].style.display = "inline-block";
        valid = false;
      } else {
        this.$refs["pass-err"].style.display = "none";
      }
      if (!this.validatePasswordConfirm()) {
        this.errMsg = "两次密码输入不一致";
        this.$refs["confirm-err"].style.display = "inline-block";
        valid = false;
      } else {
        this.$refs["confirm-err"].style.display = "none";
      }

      if (!this.protocol) {
        alert("请同意用户使用协议");
        valid = false;
      }
      return valid;
    },
    submit() {
      if (this.submitValidate()) {
        this.$refs["user-err"].style.display = "none";
        this.$refs["pass-err"].style.display = "none";
        this.$refs["confirm-err"].style.display = "none";
        requestRegister(this.username, hashPassword(this.password)).then(res => {
          console.log(`Request result: ${res}`);
          if (res.success) {
            alert("注册成功")
            window.location.href = "login.html"
          } else {
            alert(`注册失败：${res.message}`)
          }
        })

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

.err-log {
  display: inline-block;
  color: red;
  font-size: 0.8rem;
  margin-left: 5px;
  margin-top: -0.6rem;
  margin-bottom: 0.6rem;
}

.dialog{
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 100;
  width: 80vw;
  height: 80vh;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 10px;

  box-sizing: border-box;
  padding: 20px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  transition: all 0.3s;
}

.dialog h1{
  color: white;
  font-size: 1.5rem;
  margin-bottom: 20px;
  margin-top: 0;
  text-align: center;

}

.dialog p{
  min-height: 40vh;
  flex-grow: 1;
  overflow: auto;
  white-space: pre-wrap;

  margin-top: 0;
  padding: 10px 16px;
  background-color: #ffffff;
  border-radius: 10px;

  line-height: 1.5;
}

.dialog button{
  flex-shrink: 0;
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

.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
