<template>
  <div id="background">
    <div id="contain">
      <h1>用户注册</h1>

      <div class="form">
        <label>用户名：</label><input type="text" v-model.trim="name"><br/>
      </div>
      <div class="form">
        <label>密码：</label><input type="password" v-model.trim="password"><br/>
      </div>
      <div class="form">
        <label>邮箱：</label><input type="email" v-model.trim="mail"><br/>
      </div>
      <div class="form">
        <label>手机号：</label><input type="tel" v-model.trim="tel"><br/>
      </div>
      <button @click.prevent="handlefinish">提交</button>
      <button @click.prevent="returnToLogin">返回登录</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </div>
</template>
//css
<style scoped>
#background {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffffff, #5f93e9);
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

#contain {
  width: 400px;
  padding: 20px;
  background: #ffffff;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#contain h1 {
  color: #5f93e9;
  margin-bottom: 20px;
}

.form {
  color: #070707;
  margin-left: 10%;
  margin-top: 50px;
  font-size: 20px;
  text-align: left;
}

label {
  float: left;
  width: 5em;
  margin-right: 1em;
  text-align: left;
}

input, textarea {
  margin-left: 10px;
  padding: 4px;
  border: solid 1px #4e5ef3;
  outline: 0;
  font: normal 13px/100% Verdana, Tahoma, sans-serif;
  width: 200px;
  height: 20px;
  background: #f1f1f190;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 8px;
}

input:hover, textarea:hover, input:focus, textarea:focus {
  border-color: #0d0aa1;
}

button {
  position: relative;
  height: 33px;
  width: 150px;
  background: rgba(35, 19, 252, 0.425);
  border-radius: 10px;
  margin-top: 38px;
  box-shadow: none;
  color: white;
  margin-left: 40px;
}
</style>
<script>
import axios from "axios";

export default {
  name: 'register',
  props: {
    msg: String
  },
  data() {
    return {
      name: "",
      password: "",
      mail: "",
      tel: "",
      errorMessage: ""
    };
  }, methods: {
    returnToLogin() {
      this.$router.push('/login');
    },
    //点击完成按钮触发handlefinish
    async handlefinish() {
      try {
        const userData = {
          username: this.name,
          password: this.password,
          email: this.mail,
          phone_number: this.tel,
        }
        await axios.post('/users/register/', userData);
        await this.$router.replace('/Login');
      } catch (error) {
        if (error.response.status === 400) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = '注册失败, 请重试';
        }
      }
    }
  }
};
</script>
