<template>
  <div id="app">
    
    <!-- <el-container>
      <el-header> <common-header></common-header> </el-header>
      <el-container>
        <el-aside width="auto"><common-aside></common-aside></el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container> -->
    <router-view></router-view>


  </div>
</template>

<script>
import CommonAside from './components/CommonAside.vue';
import CommonHeader from './components/CommonHeader.vue';
export default {
  name: "App",
  components: {
    CommonAside,
    CommonHeader,

  }
};
</script>

<style lang="less">
html,
body,
h3 {
  margin: 0;
  padding: 0;
}

.el-header {
  padding: 0;
}

.el-main {
  background-color: #f2f3f8;
}
</style>