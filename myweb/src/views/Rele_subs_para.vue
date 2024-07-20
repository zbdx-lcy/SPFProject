<template>
    <div>
        <h2>相关物质的热力学参数</h2>
        <!-- 粘合剂的热力学参数表 -->
        <h3>表1 粘合剂的热力学参数</h3>
        <el-table :data="dataAdhesive" border>
            <el-table-column prop="substance" label="物质"></el-table-column>
            <el-table-column prop="deltaH" label="∆H (kJ/mol)"></el-table-column>
        </el-table>

        <!-- 固化剂的热力学参数表 -->
        <h3>表2 固化剂的热力学参数</h3>
        <el-table :data="dataCuringAgent" border>
            <el-table-column prop="substance" label="物质"></el-table-column>
            <el-table-column prop="Tb" label="Tb (K)"></el-table-column>
            <el-table-column prop="Tc" label="Tc (K)"></el-table-column>
            <el-table-column prop="deltaH" label="∆H (kJ/mol)"></el-table-column>
            <el-table-column prop="S" label="S (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaVH" label="∆vH_T (kJ/mol)" width="250px"></el-table-column>
            <el-table-column prop="CP" label="C_P (J∙mol-1∙K-1)"  width="350px"></el-table-column>
        </el-table>

        <!-- 交联剂的热力学参数表 -->
        <h3>表3 交联剂的热力学参数</h3>
        <el-table :data="dataCrosslinkingAgent" border>
            <el-table-column prop="substance" label="物质"></el-table-column>
            <el-table-column prop="Tb" label="Tb (K)"></el-table-column>
            <el-table-column prop="Tc" label="Tc (K)"></el-table-column>
            <el-table-column prop="deltaH" label="∆H (kJ/mol)"></el-table-column>
            <el-table-column prop="S" label="S (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaVH" label="∆vH_T (kJ/mol)"  width="250px"></el-table-column>
            <el-table-column prop="CP" label="C_P (J∙mol-1∙K-1)"  width="350px"></el-table-column>
        </el-table>

        <!-- 键合剂的热力学参数表 -->
        <h3>表4 键合剂的热力学参数</h3>
        <el-table :data="dataBondingAgent"  border>
            <el-table-column prop="substance" label="物质"></el-table-column>
            <el-table-column prop="Tb" label="Tb (K)"></el-table-column>
            <el-table-column prop="Tc" label="Tc (K)"></el-table-column>
            <el-table-column prop="deltaH" label="∆H (kJ/mol)"></el-table-column>
            <el-table-column prop="S" label="S (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaVH" label="∆vH_T (kJ/mol)"  width="250px"></el-table-column>
            <el-table-column prop="CP" label="C_P (J∙mol-1∙K-1)"  width="350px"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    name: 'ThermodynamicProperties',
    data() {
        return {
            dataAdhesive: [
                { substance: 'PBT', deltaH: '6874.26' }
            ],
            dataCuringAgent: [
                { substance: 'TDI', Tb: '542.02', Tc: '725.25', deltaH: '-36.3', S: '471.01', deltaVH: '79.948*(1-T/725.25)^0.3850', CP: '1.6E-07T^3 - 0.0006T^2 + 0.7404T + 12.801' }
            ],
            dataCrosslinkingAgent: [
                { substance: 'TMP', Tb: '570.22', Tc: '749.29', deltaH: '-638.15', S: '489.63', deltaVH: '147.31*(1-T/749.29)^0.4471', CP: '1.7E-07T^3 - 0.0003T^2 + 0.6313T + 19.088' }
            ],
            dataBondingAgent: [
                { substance: '三乙醇胺', Tb: '587.75', Tc: '772.54', deltaH: '-558.2', S: '545.69', deltaVH: '160.07*(1-T/772.54)^0.4559', CP: '8E-08T^3 - 0.0005T^2 + 0.7916T - 0.7219' }
            ]
        };
    }
};
</script>

<style scoped>
.el-table th,
.el-table td {
    padding: 8px;
    border-color: #ebeef5;
}
h2{
    text-align: center;
}
h3{
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}
.el-table{
    margin: auto;
    width: 100%;
}
</style>