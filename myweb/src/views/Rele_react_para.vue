<template>
    <div>
        <h2>相关化学反应的热力学参数</h2>
        <!-- 固化剂与交联剂反应的热力学参数表 -->
        <h3>表5 固化剂与交联剂反应的热力学参数</h3>
        <el-table :data="dataCuringCrosslinking"  border>
            <el-table-column prop="temperature" label="Temperature"></el-table-column>
            <el-table-column prop="deltaH" label="∆rH^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="deltaS" label="∆rS^0 (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaG" label="∆rG^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="K" label="K^0"></el-table-column>
        </el-table>

        <!-- 固化剂与键合剂反应的热力学参数表 -->
        <h3>表6 固化剂与键合剂反应的热力学参数</h3>
        <el-table :data="dataCuringBonding" border>
            <el-table-column prop="temperature" label="Temperature"></el-table-column>
            <el-table-column prop="deltaH" label="∆rH^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="deltaS" label="∆rS^0 (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaG" label="∆rG^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="K" label="K^0"></el-table-column>
        </el-table>

        <!-- 固化剂与水反应的热力学参数表 -->
        <h3>表7 固化剂与水反应的热力学参数</h3>
        <el-table :data="dataCuringWater"  border>
            <el-table-column prop="temperature" label="Temperature"></el-table-column>
            <el-table-column prop="deltaH" label="∆rH^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="deltaS" label="∆rS^0 (J∙mol-1∙K-1)"></el-table-column>
            <el-table-column prop="deltaG" label="∆rG^0 (kJ/mol)"></el-table-column>
            <el-table-column prop="K" label="K^0"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    name: 'ThermodynamicReactions',
    data() {
        return {
            dataCuringCrosslinking: [
                { temperature: '298.15(g)', deltaH: '-78.67', deltaS: '-202.58', deltaG: '-18.27', K: '1589.2' },
                { temperature: '298.15', deltaH: '-42.23', deltaS: '-80.38', deltaG: '-18.26', K: '1583.2' },
                { temperature: '313.15', deltaH: '-43.72', deltaS: '-92.40', deltaG: '-14.79', K: '292.86' },
                // Add more data entries as needed
            ],
            dataCuringBonding: [
                { temperature: '298.15(g)', deltaH: '-78.67', deltaS: '-202.58', deltaG: '-18.27', K: '1588.8' },
                { temperature: '298.15', deltaH: '-40.70', deltaS: '-75.25', deltaG: '-18.26', K: '1583.10' },
                { temperature: '313.15', deltaH: '-42.12', deltaS: '-85.91', deltaG: '-15.22', K: '345.62' },
                // Add more data entries as needed
            ],
            dataCuringWater: [
                { temperature: '298.15', deltaH: '-55.00', deltaS: '206.68', deltaG: '-116.62', K: '2.70E+20' },
                { temperature: '313.15', deltaH: '-56.00', deltaS: '202.55', deltaG: '-119.43', K: '8.36E+19' },
                { temperature: '323.15', deltaH: '-56.67', deltaS: '199.95', deltaG: '-121.29', K: '4.03E+19' },
                // Add more data entries as needed
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