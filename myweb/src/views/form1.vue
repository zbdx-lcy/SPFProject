<template>
  <div class="container-lg">
    <div class="top">
      <el-input v-model="fid" placeholder="请输入配方ID"></el-input>
      <el-button type="primary" @click="fetchData">加载数据</el-button>
      <el-button type="primary" @click="getChart">查询</el-button>
    </div>
    <h3 class="text-center mt-4 mb-4">时间-损耗因子图展示</h3>
    <h3 class="text-center">配方 {{ formulation.formulation_id }}</h3>
    <br>

    <div class="row" style="max-height: 80vh; overflow: auto;">
      <div class="" v-for="temperature in temperatures" :key="temperature.temp_id">
        <h4 class="text-center">{{ temperature.temp_value }} °C</h4>
        <div class="d-flex justify-content-center align-items-center chart-container" style="height: 50vh;">
          <div :id="'chart_' + formulation.formulation_id + '_' + temperature.temp_id" ref="chartD"
               style="width: 1000px; height: 400px;"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios'; // 引入axios
import html2canvas from 'html2canvas'; // 引入html2canvas库
export default {
  name: 'TimeLossFactorChart',
  data() {
    return {
      formulation: {},
      temperatures: [], // 初始为空数组
      relatedData: [], // 初始为空数组
      fid: null,
      data: [],
      timeMin: [],
      lossFactor: [],
    }
  },
  async mounted() {
    // await this.fetchData();
  },
  methods: {

    async fetchData() {
      try {
        const response = await axios.get(`/formulation/time_loss_factor_fig/${this.fid}`);
        this.formulation = response.data.formulation;
        this.temperatures = response.data.temperatures;
        this.relatedData = response.data.relatedData;

        this.temperatures.forEach(temperature => {
          temperature.relatedData = this.relatedData.filter((item, index) => {
            return item.temperature_id_id === temperature.temp_id;
          });
          temperature.timeMin = temperature.relatedData.map(item => item.time_min);
          temperature.lossFactor = temperature.relatedData.map(item => [item.time_min, item.loss_factor]);
          if (temperature.relatedData.length > 0) {
            this.$message.success('数据加载成功!')
          }

        });
      } catch (error) {
        console.error('获取信息失败:' + error);
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
    saveChartDataAsImage(chart, fileName) {
      const chartContainer = chart.getDom();
      html2canvas(chartContainer).then(canvas => {
        canvas.toBlob(blob => {
          const formData = new FormData();
          formData.append('chartImage', blob, fileName);
          // console.log(formData)
          axios.post('/fileupload/time_loss_img/image/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
              .then(response => {
                console.log('上传成功:' + response.data);
              })
              .catch(error => {
                console.error('上传失败:', error);
              });
        }, 'image/png');
      });
    },

    initChart(temperature) {
      const chartID = document.getElementById('chart_' + this.formulation.formulation_id + '_' + temperature.temp_id);
      const chart = echarts.init(chartID);
      const option = {
        title: {
          text: '时间-损耗系数图',
          left: 'center',
          top: 20,
          textStyle: {
            color: 'black'
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const time = params[0].value[0];
            const lossFactor = params[0].value[1].toFixed(2);
            return 'Time: ' + time + '<br>' + temperature.temp_value + '°C' + ' 损耗系数: ' + lossFactor;
          }
        },
        xAxis: {
          type: 'value',
          data: temperature.timeMin,
          name: '时间(min)',
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
          name: '损耗因子',
          nameTextStyle: { // 坐标轴名称样式
            fontFamily: 'Times New Roman, serif',
            fontSize: 14,
            fontWeight: 'bold',
          },
          axisLabel: {
            formatter: (value, index) => {
              return value.toFixed(2); // 将值保留两位小数
            }
          },
        },
        series: [{
          name: temperature.temp_value + '°C' + ' 损耗因子',
          type: 'line',
          data: temperature.lossFactor,
          lineStyle: {
            color: 'blue'
          },
          emphasis: {
            focus: 'series'
          },
          symbol: 'circle',
          symbolSize: 8,
          smooth: true,
          tooltip: {
            show: true // 数据点显示tooltip
          }
        }]
      };
      chart.setOption(option);
      const fileName = `TimeLossFactorChart_${this.formulation.formulation_id}_${temperature.temp_id}.png`;
      chart.on('finished', () => {
        this.saveChartDataAsImage(chart, fileName);
      });
    }
    ,
  }
}
</script>


<style lang="less" scoped>
.container-lg {
  .top {
    text-align: end;

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