import Vue from "vue";
import VueRouter from "vue-router";
import Report from "../views/Report.vue";
import Main from "../views/Main.vue";
import Data from "@/views/Data.vue";
import Formulation from "@/views/Formulation.vue";
import Form from "../views/Form.vue";
import Home from "../views/Home.vue";
import form1 from "@/views/form1.vue";
import form2 from "@/views/form2.vue";
import form3 from "@/views/form3.vue";
import form4 from "@/views/form4.vue";
import Forecast from "@/views/Forecast.vue";
import Login from "@/views/Login.vue";
import out from "@/views/out.vue";
import Register from "@/views/Register.vue";
import person from "@/views/person.vue";
import form5 from "@/views/form5.vue";
import form6 from "@/views/form6.vue";
import form7 from "@/views/form7.vue";
import Rele_react_para from "@/views/Rele_react_para.vue";
import Rele_subs_para from "@/views/Rele_subs_para.vue";

//获取原型对象上的push函数
const originalPush = VueRouter.prototype.push;
//修改原型对象中的push方法
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch((err) => err);
};
Vue.use(VueRouter);

const routes = [
    // {
    //     path: "/",
    //     component: out,
    //     redirect: "/login",
    //     children: [
    //         {path: "login", component: Login},
    //         {path: "register", component: Register},
    //     ]
    // },
    {
        path: "/person",
        component: person,
    },
    {
        path: "/main",
        component: Main,
        // redirect: "/main",
        children: [
            {path: "formulation", component: Formulation},
            {path: "rhdata", component: Data},
            {path: "form", component: Form},
            {path: "report", component: Report},
            {path: "form1", component: form1},
            {path: "form2", component: form2},
            {path: "form3", component: form3},
            {path: "person", component: person},
            {path: "form4", component: form4},
            // {path: "forecast", component: Forecast},
            {path: "", component: Formulation},
            {path: "form5", component: form5},
            {path: "form6", component: form6},
            {path: "form7", component: form7},
            {path: "Rele_react_para", component: Rele_react_para},
            {path: "Rele_subs_para", component: Rele_subs_para},
        ],
    },
];

const router = new VueRouter({
    routes,
});

export default router;
