<template>
  <div class="container-lg">

    <div class="top">
      <el-input v-model="fid" placeholder="请输入配方ID"></el-input>
      <el-button type="primary" @click="fetchData">加载数据</el-button>
      <el-button type="primary" @click="getChart">查询</el-button>
    </div>

    <h3 class="text-center mt-4 mb-4">时间-模量图展示</h3>
    <h3 class="text-center">配方 {{ formulation.formulation_id }}</h3>
    <br>
    <el-row class="row" style="max-height: 100vh; overflow: auto;">
      <el-col v-for="temperature in temperatures" :key="temperature.temp_id" :class="getColClass">
        <div class="d-flex justify-content-center align-items-center chart-container" style="height: 50vh;">
          <div class="chart-container" :id="'chart_' + formulation.formulation_id + '_' + temperature.temp_id"
            style="width: 90%; height: 90%;">
          </div>
        </div>
        <el-card class="box-card">
          <h4 class="text-center">{{ temperature.temp_value }} °C</h4>
          <el-divider></el-divider>
          <el-table :data="[temperature]" style="width: 100%; height: 90%">
            <el-table-column prop="gelPointTime" label="凝胶点时间"></el-table-column>
            <el-table-column prop="gelPointESmod" label="储能模量"></el-table-column>
            <el-table-column prop="gelPointLSmod" label="损耗模量"></el-table-column>
            <el-table-column prop="gelPointComplexViscosity" label="复合粘度"></el-table-column>
            <el-table-column prop="gelPointLossFactor" label="损耗因子"></el-table-column>
            <el-table-column prop="gelPointSolidification" label="固化度"></el-table-column>
            <el-table-column prop="gelPointDerivative_value" label="固化速率"></el-table-column>
            <el-table-column prop="gelPointEnergy" label="表观活化能"></el-table-column>
          </el-table>
          <el-divider></el-divider>
          <el-table :data="[temperature]" style="width: 100%">
            <el-table-column prop="curPointTime" label="固化终点时间"></el-table-column>
            <el-table-column prop="curPointESmod" label="储能模量"></el-table-column>
            <el-table-column prop="curPointLSmod" label="损耗模量"></el-table-column>
            <el-table-column prop="curPointComplexViscosity" label="复合粘度"></el-table-column>
            <el-table-column prop="curPointLossFactor" label="损耗因子"></el-table-column>
            <el-table-column prop="curPointSolidification" label="固化度"></el-table-column>
            <el-table-column prop="curPointDerivative_value" label="固化速率"></el-table-column>
            <el-table-column prop="curPointEnergy" label="表观活化能"></el-table-column>
          </el-table>

        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import html2canvas from "html2canvas";

export default {
  name: 'TimeModChart',
  data() {
    return {
      // formulationId: null,
      // formulationName: '',
      formulation: {},
      temperatures: [],
      relatedData: [],
      gelPoint_data: [],
      curPoint_data: [],
      fid: null,
      data: [],
      time_min: [],
      loss_mod: [],
      energy_storage_mod: [],
      chartData: [],
    }
  },
  async mounted() {
    // await this.fetchData();

  },
  methods: {
    getColClass() {
      if (window.innerWidth > 1200) {
        return 'col-lg-4';
      } else if (window.innerWidth > 992) {
        return 'col-md-6';
      } else {
        return 'col-12';
      }
    },
    async fetchData() {
      try {
        const response = await axios.get(`/formulation/time_mod_fig/${this.fid}`);
        this.formulation = response.data.formulation;
        this.temperatures = response.data.temperatures;
        this.relatedData = response.data.relatedData;
        this.gelPoint_data = response.data.gelPoint_data;
        this.curPoint_data = response.data.curPoint_data;
        this.temperatures.forEach((temperature) => {
          temperature.relatedData = this.relatedData.filter((item, index) => {
            return item.temperature_id_id === temperature.temp_id;
          });
          temperature.timeMin = temperature.relatedData.map(item => item.time_min);
          temperature.loss_mod = temperature.relatedData.map(item => [item.time_min, Math.log10(item.loss_mod), item.loss_mod]);
          temperature.energy_storage_mod = temperature.relatedData.map(item => [item.time_min, Math.log10(item.energy_storage_mod), item.energy_storage_mod]);
          // 添加gelPoint和curPoint相关的数据
          temperature.gelPointTime = this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.time_min;
          temperature.gelPointESmod = Math.round(this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.energy_storage_mod * 100) / 100;
          temperature.gelPointLSmod = Math.round(this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.loss_mod * 100) / 100;
          temperature.gelPointLossFactor = this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.loss_factor;
          temperature.gelPointComplexViscosity = this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.complex_viscosity;
          temperature.gelPointSolidification = Math.round(this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.solidification * 10000) / 10000;
          temperature.gelPointDerivative_value = this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.derivative_value;
          temperature.gelPointEnergy = this.gelPoint_data.find(data => data.temp_id === temperature.temp_id && data.type === 'mid')?.energy;

          temperature.curPointTime = this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.time_min;
          temperature.curPointESmod = Math.round(this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.energy_storage_mod * 100) / 100;
          temperature.curPointLSmod = Math.round(this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.loss_mod * 100) / 100;
          temperature.curPointLossFactor = this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.loss_factor;
          temperature.curPointComplexViscosity = this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.complex_viscosity;
          temperature.curPointSolidification = Math.round(this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.solidification * 10000) / 10000;
          temperature.curPointDerivative_value = this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.derivative_value;
          temperature.curPointEnergy = this.curPoint_data.find(data => data.temp_id === temperature.temp_id)?.energy;
          if (temperature.relatedData.length > 0) {
            this.$message.success('数据加载成功!')
          }

        });
      } catch (error) {
        console.error('获取数据失败:' + error);
      }
    },
    getChart() {
      try {
        this.temperatures.forEach(temperature => {
          this.initChart(temperature)
          this.$message.success('图表加载成功!')
        });
      } catch (error) {
        this.$message.error('图表加载失败!')
      }
    },
    initChart(temperature) {
      const chartID = document.getElementById('chart_' + this.formulation.formulation_id + '_' + temperature.temp_id);
      const chart = echarts.init(chartID);

      const option = {
        // title: {
        //   text: '时间-模量图',
        //   left: 'center'
        // },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            var time = params[0].value[0];
            var lossModValue
            if (params.length === 4) {
              lossModValue = params[2].value[2].toFixed(2);
            } else {
              lossModValue = params[1].value[2].toFixed(2);
            }
            var energyStorageModValue;
            try {
              params.forEach((item) => {
                if (item.seriesName.indexOf('储能模量') !== -1) {
                  energyStorageModValue = item.value[2].toFixed(2);
                  throw Error();
                }
              });
            } catch (e) {
            }
            return 'Time: ' + time + '<br>' +
              temperature.temp_value + '°C' + '损耗模量: ' + lossModValue + '<br>' +
              temperature.temp_value + '°C' + '储能模量: ' + energyStorageModValue;
          }
        },
        xAxis: {
          type: 'value',
          name: '时间(min)',
          data: temperature.time_min,
          nameTextStyle: { // 坐标轴名称样式
            fontFamily: 'Times New Roman, serif',
            fontSize: 14,
            fontWeight: 'bold',
          },
          axisLabel: { // 坐标轴刻度标签的样式
            color: '#999',
            fontFamily: 'Georgia, serif',
            fontSize: 12,
          }
        },
        yAxis: {
          type: 'value',
          name: '模量(log10)',
          nameTextStyle: { // 坐标轴名称样式
            fontFamily: 'Times New Roman, serif',
            fontSize: 14,
            fontWeight: 'bold',
          },
          axisLabel: {
            formatter: function (value, index) {
              return value.toFixed(0);
            }
          },
        },
        series: [{
          data: temperature.energy_storage_mod,
          type: 'line',
          name: temperature.temp_value + '°C' + '储能模量',
          smooth: true,
          tooltip: {
            show: true // 数据点显示tooltip
          }
        },
        {
          data: temperature.loss_mod,
          type: 'line',
          name: temperature.temp_value + '°C' + '损耗模量',
          smooth: true,
          tooltip: {
            show: true // 数据点显示tooltip
          }
        }]
      };
      chart.setOption(option);
      const fileName = `TimeModChart_${this.formulation.formulation_id}_${temperature.temp_id}.png`;
      chart.on('finished', () => {
        this.saveChartDataAsImage(chart, fileName);
      });
    },
    saveChartDataAsImage(chart, fileName) {
      const chartContainer = chart.getDom()
      html2canvas(chartContainer).then(canvas => {
        canvas.toBlob(blob => {
          const formData = new FormData();
          formData.append('chartImage', blob, fileName);
          axios.post('/fileupload/time_mod_img/image/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(response => {
              console.log('上传成功:' + response.data);
            })
            .catch(error => {
              console.error('上传失败:' + error);
            });
        }, 'image/png');
      });
    },
  }
}
</script>

<style lang="less" scoped>
.container-lg {
  .top {
    text-align: end;

    .box-card {
      margin-bottom: 20px;
    }

    .el-input {
      width: 150px;
      margin-right: 20px;
    }
  }

  h2 {
    font-weight: bold;
    color: #333;
    font-style: normal;
    font-family: 'Arial, sans-serif';
    font-size: 25px;
    text-align: center;
  }

  h3 {
    text-align: center;
    color: #333;
    font-family: 'Arial, sans-serif';
  }

  h4 {
    text-align: center;
    color: #333;
    font-family: 'Arial, sans-serif';
  }

  .chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 200px;
  }
}
</style>