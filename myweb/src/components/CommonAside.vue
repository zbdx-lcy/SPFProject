<template>
    <div>
        <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
            :collapse="isCollapse" >
            
            <el-menu-item @click="clickMenu(item)" :index="item.name" v-for="item in menuData" :key="item.name">
                <template slot="title">
                    <i :class="item.icon"></i>
                    <span>{{ item.lable }}</span>
                </template>
            </el-menu-item>

            <el-submenu index="2">
                <template slot="title">
                    <i :class="elicon2"></i>
                    <span>热力学参数</span>
                </template>
                <el-menu-item-group  v-for="item in haschildren2" :key="item.lable">
                    <el-menu-item :index="item.path" @click="clickMenu(item)">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span>{{ item.lable }}</span>
                        </template>
                    </el-menu-item>
                </el-menu-item-group>
            </el-submenu>

            <el-submenu index="1">
                <template slot="title">
                    <i :class="elicon"></i>
                    <span>热力学数据图表</span>
                </template>
                <el-menu-item-group  v-for="item in haschildren" :key="item.lable">
                    <el-menu-item :index="item.path" @click="clickMenu(item)">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span>{{ item.lable }}</span>
                        </template>
                    </el-menu-item>
                </el-menu-item-group>
            </el-submenu>
        </el-menu>
    </div>
</template>


<style lang="less" scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
    position: sticky;
    top: 0;
    left: 0;
    float: left;
    overflow-y: auto;
    display: block;
    box-sizing: border-box;
    
    //margin-top: 5px;
}

.el-menu {
    height: 91vh;
    background-color:"#FFFFFF" ;
    color:"#6E7078";
    
   
    h3 {
        color: black;
        text-align: center;
        line-height: 65px;
        font-size: 19px;
        font-family: Open Sans, sans-serif;
    }
    i {
        color: #5A6FC0;
    }
}

.el-menu-item.is-active {
    //没作用
    background-color: #5A6FC0;
    color: #ffffff;

    i {
        color: #ffffff;
    }
}
</style>

<script>
export default {
    data() {
        return {
            elicon: "el-icon-pie-chart",
            elicon2: "el-icon-edit-outline",
            menuData: [
                {
                    path: "/main/formulation",
                    name: "formulation",
                    lable: "体系组份",
                    url: "",
                    icon: "el-icon-document"
                },
                {
                    path: "/main/rhdata",
                    name: "rhdata",
                    lable: "热力学数据",
                    url: "",
                    icon: "el-icon-data-analysis"
                },
                {
                    path: "/main/report",
                    name: "report",
                    lable: "报告展示",
                    url: "",
                    icon: "el-icon-reading"
                },
                {
                    path: "/main/forecast",
                    name: "forecast",
                    lable: "数据预测",
                    url: "",
                    icon: "el-icon-data-line"
                },
                {
                    path: "/main/person",
                    name: "person",
                    lable: "个人信息",
                    icon: "el-icon-user"
                }
            ],
            haschildren: [
                {
                    path: "/main/form1",
                    name: "form1",
                    lable: "时间-损耗因子图",
                    url: ""
                },
                {
                    path: "/main/form2",
                    name: "form2",
                    lable: "时间-模量图",
                    url: ""
                },
                {
                    path: "/main/form3",
                    name: "form3",
                    lable: "固化终点-模量图",
                    url: ""
                },
                {
                    path: "/main/form4",
                    name: "form4",
                    lable: "时间-复数黏度图",
                    url: ""
                },
                {
                    path: "/main/form5",
                    name: "form5",
                    lable: "时间-固化度图",
                    url: ""
                },
                {
                    path: "/main/form6",
                    name: "form6",
                    lable: "固化度-固化速率图",
                    url: ""
                },
                {
                    path: "/main/form7",
                    name: "form7",
                    lable: "固化度-表观活化能图",
                    url: ""
                }
            ],
            haschildren2: [
                {
                    path: "/main/Rele_subs_para",
                    name: "Rele_subs_para",
                    lable: "相关物质参数",
                    url: ""
                },
                {
                    path: "/main/Rele_react_para",
                    name: "Rele_subs_para",
                    lable: "相关化学反应参数",
                    url: ""
                },
            ]
        };
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        clickMenu(item) {
            //路径不同能跳
            if (this.$router.path !== item.path || (this.$router.path === '/formulation' && (item.path === '/'))) {
                this.$router.push(item.path);
            }
        }
    },
    computed: {
        // isCollapse() {
        //     return this.$store.state.tab.isCollapse
        // }
    }
}
</script>