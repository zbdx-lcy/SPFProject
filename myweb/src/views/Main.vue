<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div>
        <el-container>
            <el-header> <common-header></common-header> </el-header>
            <el-container>
                <el-aside width="auto"><common-aside></common-aside></el-aside>
                <el-main>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>
<script>
import CommonAside from '@/components/CommonAside.vue';
import CommonHeader from '@/components/CommonHeader.vue';
import Formulation from './Formulation.vue';
import person from './person.vue';
export default {
    components: {
        CommonAside,
        CommonHeader,
        Formulation,
        person,
    }
}
// let x = "a";
// console.log(x)
</script>