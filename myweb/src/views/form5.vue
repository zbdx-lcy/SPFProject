<template>
  <div class="container-lg">

    <div class="top">
      <el-input v-model="fid" placeholder="请输入配方ID"></el-input>
      <el-button type="primary" @click="fetchData">加载数据</el-button>
      <el-button type="primary" @click="getChart">查询</el-button>
    </div>

    <h3 class="text-center mt-4 mb-4">时间-固化度图展示</h3>
    <h3 class="text-center">配方 {{ formulation.formulation_id }}</h3>
    <br>
    <div class="row" style="max-height: 100vh; overflow: auto;">
      <div class="col-8 col-md-8 col-lg-4 mb-4" style="overflow-x: auto;">
        <div class="d-flex justify-content-center align-items-center chart-container" style="height: 50vh;">
          <div class="chart-container" :id="'chart_' + formulation.formulation_id"
               style="width: 100%; height: 100%;"></div>
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
  name: 'TimeSolidificationChart',
  data() {
    return {
      solidification_65: [],
      solidification_60: [],
      formulation: {},
      solidification_55: [],
      time_s: [],
      merged_data: [],
      fid: null,
    }
  },
  async mounted() {
    // await this.fetchData();

  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`/formulation/time_solidification_fig/${this.fid}`);
        this.formulation = response.data.formulation;
        this.time_s = response.data.solidification_65.map(item => item.time_s);
        this.solidification_55 = response.data.solidification_55.map(item => [item.time_s, item.solidification]);
        this.solidification_60 = response.data.solidification_60.map(item => [item.time_s, item.solidification]);
        this.solidification_65 = response.data.solidification_65.map(item => [item.time_s, item.solidification]);
        if (this.solidification_55.length > 0 && this.solidification_65.length > 0 && this.solidification_60.length > 0) {
          this.$message.success('数据加载成功!')
        }
      } catch (error) {
        console.error('获取数据失败:' + error);
      }
    },
    getChart() {
      try {
        this.initChart()
        this.$message.success('图表加载成功!')
      } catch (error) {
        this.$message.error('图表加载失败!')
      }
    },
    initChart() {
      const chartID = document.getElementById('chart_' + this.formulation.formulation_id);
      const chart = echarts.init(chartID);

      const option = {
        title: {
          text: '时间-固化度图',
          top: '5%',
          left: 'center'
        },
        legend: {
          data: ['55°C', '60°C', '65°C'],
          top:'bottom',
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            console.log(params)
            if (params.length > 2) {
              var time55 = params[0].value[0];
              var temp55 = params[0].seriesName;
              var solidification55 = params[0].value[1];
              var time65 = params[2].value[0];
              var temp65 = params[2].seriesName;
              var solidification65 = params[2].value[1];
              var time60 = params[1].value[0];
              var temp60 = params[1].seriesName;
              var solidification60 = params[1].value[1];
              return temp55 + ' Time: ' + time55 + 's' + ' 固化度:' + solidification55 + '<br>' +
                  temp60 + ' Time:' + time60 + 's' + ' 固化度:' + solidification60 + '<br>' +
                  temp65 + ' Time:' + time65 + 's' + ' 固化度:' + solidification65;
            } else {
              var time = params[0].value[0];
              var temp = params[0].seriesName;
              var solidification = params[0].value[1];
              return temp + ' Time: ' + time + 's' + ' 固化度:' + solidification;
            }
          }
        },
        xAxis: {
          type: 'value',
          name: '时间(s)',
          data: this.time_s,
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
          name: '固化度',
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
          data: this.solidification_55,
          type: 'line',
          name: '55°C',
          smooth: true,
          tooltip: {
            show: true // 数据点显示tooltip
          }
        },
          {
            data: this.solidification_60,
            type: 'line',
            name: '60°C',
            smooth: true,
            tooltip: {
              show: true // 数据点显示tooltip
            }
          },
          {
            data: this.solidification_65,
            type: 'line',
            name: '65°C',
            smooth: true,
            tooltip: {
              show: true // 数据点显示tooltip
            }
          }]
      };
      chart.setOption(option);
      const fileName = `TimeSolidificationChart_${this.formulation.formulation_id}.png`;
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
          axios.post('/fileupload/time_solid_img/image/', formData, {
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
    height: 500px;
  }
}
</style>