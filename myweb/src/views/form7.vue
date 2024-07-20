<template>
  <div class="container-lg">

    <div class="top">
      <el-input v-model="fid" placeholder="请输入配方ID"></el-input>
      <el-button type="primary" @click="fetchData">加载数据</el-button>
      <el-button type="primary" @click="getChart">查询</el-button>
    </div>

    <h3 class="text-center mt-4 mb-4">表观活化能-固化度图展示</h3>
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
  name: 'SolidificationDerivativeChart',
  data() {
    return {
      ea_solid: [],
      formulation: {},

      time_s: [],
      derivative_data: [],
      fid: null,
    }
  },
  async mounted() {
    // await this.fetchData();

  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(`/formulation/ea_solidification_fig/${this.fid}`);
        this.formulation = response.data.formulation;
        this.ea_solid = response.data.ea_solid.map(item => [item.solidification, item.energy]);

        console.log(this.ea_solid)
        if (this.ea_solid.length > 0) {
          this.$message.success('数据加载成功!')
        }
      } catch (error) {
        this.$message.error('获取数据失败!');
      }
    },
    getChart() {
      try {
        this.initChart()
        this.$message.success('图表加载成功!')
      } catch (error) {
        this.$message.error('图表加载失败!' + error)
      }
    },
    initChart() {
      const chartID = document.getElementById('chart_' + this.formulation.formulation_id);
      const chart = echarts.init(chartID);

      const option = {
        title: {
          text: '表观活化能-固化度图',
          top: '5%',
          left: 'center'
        },
        legend: {
          top:'bottom',
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            console.log(params)
            if (params.length > 2) {
              var solid55 = params[0].value[0];
              var ea55 = params[0].value[1];
              return '固化度: ' + solid55 +  ' 表观活化能:' + ea55
            } else {
              var solid = params[0].value[0];
              var temp = params[0].seriesName;
              var ea = params[0].value[1];
              return '固化度: ' + solid +  ' 表观活化能:' + ea;
            }
          }
        },
        xAxis: {
          type: 'value',
          name: '固化度',
          data: [0, 0.2, 0.4, 0.6, 0.8, 1],
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
          name: '表观活化能Ea',
          nameTextStyle: { // 坐标轴名称样式
            fontFamily: 'Times New Roman, serif',
            fontSize: 14,
            fontWeight: 'bold',
          },
          axisLabel: {
            // rotate: 90
          },
          min: 0
        },
        series: [{
          data: this.ea_solid,
          type: 'line',
          name: '表观活化能',
          smooth: false,
          tooltip: {
            show: true // 数据点显示tooltip
          }
        }]
      };
      chart.setOption(option);
      const fileName = `SolidEAChart_${this.formulation.formulation_id}.png`;
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
    height: 5000px;
  }
}
</style>