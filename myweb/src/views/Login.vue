<template>
  <div id="background">
    <h1>复合含能材料热力学数据库</h1>
    <div class="container">
      <form action="">
        <div class="form">
          <div class="item">
            <label>用户名：</label><input type="text" name="username" v-model.trim="name" placeholder="请输入用户名">
          </div>
          <div class="item">
            <label>密码：</label><input type="password" name="password" v-model.trim="password" placeholder="请输入密码">
          </div>
        </div>
<!--          <div class="keep">-->
<!--            <input @click="handlesave" id="yes" type="radio" value="0">-->
<!--            <label for="yes">保持登录状态</label>-->
<!--          </div>-->
      </form>
      <button type="submit" @click.prevent="handlelogin">登录</button>

      <button @click.prevent="handleregister">注册</button>
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
#background {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #ffffff, #01a2ff);
  /* background: rgb(209, 226, 255); */
  position: fixed;
  top: 0;
  left: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}

.container {
  width: 400px;
  padding: 20px;
  margin-top: 120px;
  background: rgba(255, 255, 255, 0.42);
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.container h1 {
  color: #5f93e9;
  margin-bottom: 20px;
}

.item {
  margin-bottom: 20px;
}

.item label {
  display: block;
  text-align: left;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 8px;
  border: 1px solid #5f93e9;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

button {
  margin-top: 30px;
  margin-bottom: 15px;
  margin-left: 30px;
  margin-right: 30px;
  padding: 10px 20px;
  background: #5f93e9;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.keep input {
  margin-right: 5px;
}
</style>


<script>
import Main from './Main.vue';
import axios from "axios";
export default {
  name: 'APP',
  comments: {
    Main
  },
  data() {
    return {
      name: "",//姓名，用v-model绑定监听，将输入的字符串赋值给name变量
      password: "",//密码
      st: "false",//false为不保存登录
    };
  },
  mounted() {
    // const isLoggedIn = this.getCookie('loggedIn');
    // if (isLoggedIn === 'true') {
    //   this.handleAutoLogin();
    // }
  },
  methods: {
    async handlelogin() {
      try {
        const url = 'users/login/';
        const data = {
          username: this.name,
          password: this.password,
        }
        const response = await axios.post(url, data);
        // if (this.st) {
        //   this.setCookie('loggedIn', 'true', 15);
        // }
        if (response.data.code === 200) {
          this.$router.replace('/main'); // 登录成功，跳转至主页面
        } else {
          this.$message.error("登录失败:" + response.data.msg)
          // alert("登录失败:" + response.data.msg)
        }
      } catch (error) {
        if (error.code === 400) {
          this.$message.error("登录失败:" + error.response.msg)
        }
      }
    },
    handleregister: function () {
      this.$router.replace('/register')//点击注册按钮，跳转至注册页面
    },
    //点击保持登录状态触发handlesave
    handlesave: function () {
      this.st = !this.st;//修改登录状态为true
    },
    handleAutoLogin() {
      this.handlelogin();
    },
    setCookie() {
      const date = new Date();
      date.setTime(data.getTime() + (days * 24 * 60 *60 * 1000));
      document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
    },
    getCookie() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  }
};
</script>
