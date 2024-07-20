<template>
  <div id="container">
    <h1 class="title">个人信息</h1>
    <el-table :data="tableData" style="width: 97%; margin-top: 50px; margin-left: 20px;">
      <el-table-column prop="label" label="内容"></el-table-column>
      <el-table-column prop="value" label="信息"></el-table-column>
    </el-table>
  </div>
</template>

<style lang="less" scoped>
#container {
  top: 20px;
  left: 20px;
  width: 97%;
  height: 95%;
  padding: 20px;
  background: #ffffff;
  text-align: left;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info {
  margin-top: 30px;
}

p {
  font-size: 18px;
  margin-left: 20px;
  margin-top: 20px;
}

.title {
  font-size: 30px;
  text-align: center;
  margin-bottom: 20px;
}
</style>

<script>
import axios from "axios";

export default {
  name: 'Home',
  data() {
    return {
      tableData: [
        { label: "用户名", value: this.username },
        { label: "邮箱", value: this.email },
        { label: "手机号", value: this.phone_number }
      ],
      isAuth: "",//是否保持登录状态
    };
  },
  created() {
    this.fetchPersonalInfo();
  },
  methods: {
    async fetchPersonalInfo() {
      try {
        const response = await axios.get('/users/user_info'); // 假设后端 API 地址为 /api/personal-info
        const data = response.data;
        this.username = data.username || '无';
        this.email = data.email || '无';
        this.phone_number = data.phone_number || '无';
      } catch (error) {
        this.$message.error('Error fetching personal info:' + error.message);
      }
    }
  }
}
</script>
