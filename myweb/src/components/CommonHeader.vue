<template>
    <div class="header">
        <div class="l-c">
            <h3 color="#010101">{{ isCollapse ? '后台' : '复合含能材料热力学数据库' }}</h3>
        </div>
        <div class="r-c">
            <el-dropdown trigger="click" @command="handleCommand">
                <el-button class="el-dropdown-link">
                    账号<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                    <!-- <el-dropdown-item command="a">个人中心</el-dropdown-item> -->
                    <el-dropdown-item command="b">退出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>

        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isAuth: "",//是否保持登录状态
        }
    },
    methods: {
        handleCommand(command) {
            if (command == 'a') {
                this.$router.push('/person');
            }
            if (command == 'b') {
                //当点击退出按钮，将不保存登录状态
                this.isAuth = "false";//修改登录状态
                localStorage.setItem('s', this.isAuth);
                this.$router.replace('/login');//页面跳转至登录页面
            }
        }
    }
}
</script>

<style lang="less" scoped>
.header {
    background-color: white;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 20px;
    border-bottom: 1px solid #EDEDED;
    /* 添加下边框线 */
    box-shadow: 0 8px 12px -6px rgba(0, 0, 0, 0.1), 0 0 8px 0 rgba(0, 0, 0, 0.05), 0 12px 24px 0 rgba(0, 0, 0, 0.05);
    position: relative;
    z-index: 10;
    /* 设置一个较大的 z-index 值 */


    .text {
        color: #ffffff;
        font-size: 14px;
        margin-left: 10px;
    }

    .r-c {
        .el-dropdown-link {
            color: #ffffff;
            background-color: #138a07;
            border-radius: 9999px;
            margin-right: 20px;
            padding: 8px 16px 9px;
        }

        .el-button {
            border: 0;
        }
    }
}
</style>
