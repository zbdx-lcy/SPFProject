<template>
    <div class="top">
        <el-input v-model="formulationId" placeholder="请输入配方ID"></el-input>

        <el-select v-model="selectedChart">
            <el-option value="时间-损耗因子图">时间-损耗因子图</el-option>
            <el-option value="时间-模量图">时间-模量图</el-option>
            <el-option value="固化终点-模量图">固化终点-模量图</el-option>
            <el-option value="时间-复数黏度图">时间-复数黏度图</el-option>
        </el-select>
        <el-button type="primary" @click="fetchData">查询</el-button>
        <div ref="chart" style="width: 600px; height: 400px;"></div>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios'; // 引入axios

export default {
    data() {
        return {
            formulationId: '',
            selectedChart: '图表样式',
            chartInstance: null, // 图表实例
        };
    },
    methods: {
        async fetchData() {
            try {
                const response = await axios.get('/formulation/', { params: { formulationId: this.formulationId } });
                // 假设后端返回的数据格式为{ data: [{ name: 'A', value: 100 }, ...] }
                const data = response.data.data;
                this.renderChart(data);
            } catch (error) {
                this.$message.error('获取数据失败:' + error);
            }
        },
        renderChart(data) { //根据选择的图表样式设置图表配置
            if (!this.chartInstance) {
                this.chartInstance = echarts.init(this.$refs.chart);
            }
            const options = this.getChartOptions(this.selectedChart, data); //传入选择的图表和id
            this.chartInstance.setOption(options);
        },
        getChartOptions(type, data) {
            const commonOptions = {
                title: {
                    text: `配方ID: ${this.formulationId}`,
                },
                tooltip: {},
                legend: {
                    data: ['数据'],
                },
                xAxis: {
                    data: data.map(item => item.name),
                },
                yAxis: {},
            };

            switch (type) {
                case '时间-损耗因子图':
                    return {

                        ...commonOptions,
                        series: [{ name: '数据', type: 'bar', data: data.map(item => item.value) }],
                    };
                case '时间-模量图':
                    return {
                        ...commonOptions,
                        series: [{ name: '数据', type: 'line', data: data.map(item => item.value) }],
                    };
                case '固化终点-模量图':
                    return {
                        ...commonOptions,
                        series: [{ name: '数据', type: 'pie', radius: '55%', data }],
                    };
                case '时间-复数黏度图':
                    return {
                        ...commonOptions,
                        series: [{ name: '数据', type: 'scatter', data: data.map(item => [item.name, item.value]) }],
                    };
                default:
                    return {};
            }
        },
    },
};
</script>


<style lang="less" scoped>
.top {
    text-align: end;
    .el-input{
    width:150px;
    margin-right: 20px;
  }
.el-select {
    width:160px;
    margin-right: 20px;
}
}

</style>