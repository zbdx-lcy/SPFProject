<template>
  <div class="container">
    <h1 class="mt-5 mb-4 text-center">固化终点-模量图展示</h1>
    <div class="row" style="max-height: 80vh; overflow: auto;">
      <div class="col-md-6">
        <div id="chart1" class="chart-container" style="width: 600px; height: 500px;"></div>
      </div>
      <div class="col-md-6">
        <div id="chart2" class="chart-container" style="width: 600px; height: 500px;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import html2canvas from "html2canvas";

export default {
  name: 'CureEndpointModChart',
  data() {
    return {
      formulationData: [],
      formulationIds: [],
      temperaturesEM: [],
      temperaturesLM: [],
      seriesData: [],
      seriesDataLM: [],
    };
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('/formulation/cur_Endpoint_fig/');
        this.formulationData = response.data;
        this.renderCharts();
        this.initCharts();
        this.$message.success('图表加载成功!')
        // this.saveChartDataAsImage();
      } catch (error) {
        console.error('数据获取失败:' + error);
      }
    },
    renderCharts() {
      this.formulationData.forEach((item) => {
        if (!this.formulationIds.includes(item.formulation_id)) {
          this.formulationIds.push(item.formulation_id);
        }
        if (!this.temperaturesEM.includes(item.temperature)) {
          this.temperaturesEM.push(item.temperature);
        }
        if (!this.temperaturesLM.includes(item.temperature)) {
          this.temperaturesLM.push(item.temperature);
        }
      });

      this.temperaturesEM.forEach(temperature => {
        const temperatureSeriesData = this.formulationData.filter(item => item.temperature === temperature).map(item => item.energy_storage_mod);

        this.seriesData.push({
          name: temperature + '°C',
          type: 'bar',
          data: temperatureSeriesData
        });
      });

      this.temperaturesLM.forEach(temperature => {
        const temperatureSeriesData = this.formulationData.filter(item => item.temperature === temperature).map(item => item.loss_mod);

        this.seriesDataLM.push({
          name: temperature + '°C',
          type: 'bar',
          data: temperatureSeriesData
        });
      });
    },
    initCharts() {
      if (this.formulationData.length === 0) {
        console.warn('No data available for chart initialization');
        return;
      }
      const chartId1 = document.getElementById('chart1')
      const chartId2 = document.getElementById('chart2')
      const chart1 = echarts.init(chartId1);
      const chart2 = echarts.init(chartId2);

      const option1 = {
        title: {
          text: '固化终点-储能模量图',
          left: 'center',
          top: 20,
          textStyle: {
            color: 'black',
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            return '配方号: ' + params[0].name + '<br>' +
                '温度:' + params[0].seriesName + '<br>' +
                '储能模量: ' + params[0].data + '<br>' +
                '温度:' + params[1].seriesName + '<br>' +
                '储能模量:' + params[1].data + '<br>' +
                '温度:' + params[2].seriesName + '<br>' +
                '储能模量:' + params[2].data
          }
        },
        legend: {
          data: this.temperaturesEM.map((temperature) => {
            return temperature + '°C';
          })
        },
        xAxis: {
          type: 'category',
          data: this.formulationIds,
          axisLabel: {
            color: '#999',
            fontFamily: 'Georgia, serif',
            fontSize: 12,
          },
          name: '配方号'
        },
        yAxis: {
          type: 'value',
          name: '储能模量',
        },
        series: this.seriesData

      };

      const option2 = {
        title: {
          text: '固化终点-损耗模量图',
          left: 'center',
          top: 20,
          textStyle: {
            color: 'black',
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            return '配方号: ' + params[0].name + '<br>' +
                '温度:' + params[0].seriesName + '<br>' +
                '损耗模量: ' + params[0].data + '<br>' +
                '温度:' + params[1].seriesName + '<br>' +
                '损耗模量:' + params[1].data + '<br>' +
                '温度:' + params[2].seriesName + '<br>' +

                '损耗模量:' + params[2].data
          }
        },
        legend: {
          data: this.temperaturesLM.map((temperature) => {
            return temperature + '°C';
          })
        },
        xAxis: {
          type: 'category',
          data: this.formulationIds,
          axisLabel: {
            color: '#999',
            fontFamily: 'Georgia, serif',
            fontSize: 12,
          },
          name: '配方号'
        },
        yAxis: {
          type: 'value',
          name: '损耗模量'
        },
        series: this.seriesDataLM
      };
      chart1.setOption(option1);
      chart2.setOption(option2);
      // 监听图表渲染完成事件
      chart1.on('finished', () => {
        this.saveChartDataAsImage(chart1, 'CureEndpointEMModChart.png');
      });
      chart2.on('finished', () => {
        this.saveChartDataAsImage(chart2, 'CureEndpointLMModChart.png');
      });
    },

    saveChartDataAsImage(chart, filename) {
      const chartContainer = chart.getDom();
      html2canvas(chartContainer).then(canvas => {
        canvas.toBlob(blob => {
          const formData = new FormData();
          formData.append('chartImage', blob, filename);
          axios.post('/fileupload/curPoint_img/image/', formData, {
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
.container {
  h1 {
    font-weight: bold;
    color: #333;
    font-style: normal;
    font-family: 'Arial, sans-serif';
    font-size: 25px;
    text-align: center;
  }

  .row {
    display: flex;
    justify-content: space-around;
  }
}

.chart-container {
  position: relative;
}
</style>
