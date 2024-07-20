<template>
  <div>
    <div class="top">
      <div class="file-upload-container">

      </div>
      <div class="search-container">
        <el-input v-model="formulation_id" placeholder="请输入配方ID"></el-input>
        <el-input v-model="temperature_id" placeholder="请输入温度"></el-input>
        <el-button type="primary" @click="generateReport">生成报告</el-button>
        <el-button type="primary" @click="fetchPdfData">加载报告</el-button>
        <el-button type="primary" @click="downloadPdf">下载报告</el-button>
      </div>
    </div>
    <!--    <div>-->
    <!--&lt;!&ndash;      <canvas ref="pdfCanvas"></canvas>&ndash;&gt;-->
    <!--    </div>-->
  </div>
</template>

<script>
import axios from 'axios';
import FileSaver from 'file-saver';


export default {
  data() {
    return {
      formulation_id: '',
      temperature_id: '',
      temperature_value: '',
      pdfData: null,
      pdfDocument: null,
      pdfUrl: '',
    };
  },
  methods: {
    generateReport() {
      axios.get(`fileupload/report_create/${this.formulation_id}/${this.temperature_id}/`)
          .then(response => {
            if (response.status === 200) {
              this.$message.success("报告生成成功！")
            } else {
              this.$message.error("报告生成失败!", response.data.error, response.data.details)
            }
          })
          .catch(error => {
            this.$message.error('请求出错:', error);
          });
    },
    async fetchPdfData() {
      try {
        // 从后端获取 PDF 数据，这里假设使用 axios 进行请求
        const response = await axios.get('fileupload/report_out/', {
          responseType: 'arraybuffer',
          params: {
            formulationId: this.formulation_id,
            temperatureId: this.temperature_id
          },
        });
        this.pdfData = new Blob([response.data], {type: 'application/pdf'});
        this.pdfUrl = URL.createObjectURL(this.pdfData);
        window.open(this.pdfUrl, '_blank');
        // this.pdfUrl = response.data.pdfUrl;
        // console.log(this.pdfUrl)
      } catch (error) {
        this.$message.error('Failed to fetch PDF data' + error);
      }
    }
    ,
    downloadPdf() {
      // 下载 PDF 文件
      FileSaver.saveAs(this.pdfData, 'REPORT_' + 'Formulation_' + this.formulation_id + '_' + 'temperature_' + this.temperature_id + '.pdf')
    }
    ,
  },
};
</script>

<style lang="less" scoped>
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .file-upload-container {
    margin-right: 20px;
  }

  .search-container {
    display: flex;
    align-items: center;
  }

  .el-input {
    width: 150px;
    margin-right: 20px;
  }
}
</style>
