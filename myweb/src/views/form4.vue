<template>
  <div class="container-lg">
    <div class="top">
      <el-input v-model="fid" placeholder="请输入配方ID"></el-input>
      <el-button type="primary" @click="fetchData">加载数据</el-button>
      <el-button type="primary" @click="getChart">查询</el-button>
    </div>

    <h2 class="text-center mt-4 mb-4">时间-复数黏度图展示</h2>
    <h3 class="text-center">配方 {{ formulation.formulation_id }}</h3>
    <br>
    <div class="row" style="max-height: 80vh; overflow: auto;">
      <div v-for="temperature in temperatures" :key="temperature.temp_id" class="col-16 col-md-16 col-lg-12 mb-12">
        <h4 class="text-center">{{ temperature.temp_value }} °C</h4>
        <div class="d-flex justify-content-center align-items-center chart-container" style="height: 50vh;">
          <div :id="'chart_' + formulation.formulation_id + '_' + temperature.temp_id" class="chart-container"
               style="width: 1000px; height: 400px;"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import html2canvas from "html2canvas";

export default {
  name: 'TimeComplexViscosityChart',
  data() {
    return {
      formulation: {},
      temperatures: [],
      relatedData: [],
      fid: null,
      data: [],
      timeMin: [],
      complexViscosity: []
    };
  },
  async mounted() {
    // await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // 假设这是你的API端点
        const Response = await axios.get(`/formulation/time_viscosity_fig/${this.fid}`);
        this.formulation = Response.data.formulation;
        this.temperatures = Response.data.temperatures;
        this.relatedData = Response.data.relatedData;
        this.temperatures.forEach((temperature) => {
          temperature.relatedData = this.relatedData.filter((item, index) => {
            return item.temperature_id_id === temperature.temp_id;
          });
          temperature.timeMin = temperature.relatedData.map(item => item.time_min);
          temperature.complexViscosity = temperature.relatedData.map(item => [item.time_min, item.complex_viscosity]);
        });
        if (temperature.relatedData.length > 0 ) {
          this.$message.success('数据加载成功!')
        }
      } catch (error) {
        console.error('数据获取失败:' + error);
      }
    },
    getChart() {
      try {
        this.temperatures.forEach(temperature => {
          this.initChart(temperature)
          this.$message.success('图表加载成功!')
        });
      } catch (error) {
        this.$message.error('图表加载失败!' +  error)
      }
    },
    initChart(temperature) {
      const chartID = document.getElementById('chart_' + this.formulation.formulation_id + '_' + temperature.temp_id);
      const chart = echarts.init(chartID);
      const option = {
        title: {
          text: '时间-复数黏度图',
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
            const complex_viscosity = params[0].value[1].toFixed(2);
            return 'Time: ' + time + '<br>' +
                temperature.temp_value + '°C' + '复数黏度: ' + complex_viscosity
          }
        },
        xAxis: {
          type: 'value',
          data: temperature.timeMin
        },
        yAxis: {
          type: 'value',
          name: '复数黏度',
          axisLabel: {
            formatter: (value, index) => {
              return value.toFixed(0); // 将值保留两位小数
            }
          },
        },
        series: [
          {
            name: temperature.temp_value + '°C' + '复数黏度',
            type: 'line',
            data: temperature.complexViscosity,
            lineStyle: {
              color: 'blue'
            },
            emphasis: {
              focus: 'series'
            },
            symbol: 'circle', // 设置数据点的形状为圆形
            symbolSize: 8, // 设置数据点的大小
            tooltip: {
              show: true // 数据点显示tooltip
            }
          },
        ]
      };

      chart.setOption(option);
      const filename = `TimeCVChart_${this.formulation.formulation_id}_${temperature.temp_id}.png`
      // 监听图表渲染完成事件
      chart.on('finished', () => {
        this.saveChartDataAsImage(chart, filename);
      });

    },
    saveChartDataAsImage(chart, filename) {
      const chartContainer = chart.getDom();
      html2canvas(chartContainer).then(canvas => {
        canvas.toBlob(blob => {
          const formData = new FormData();
          formData.append('chartImage', blob, filename);
          axios.post('/fileupload/time_cv_img/image/', formData, {
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
