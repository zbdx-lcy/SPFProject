<template>

  <div class="data-form">
    <div class="top">
      <div class="file-upload-container">
        <el-upload class="file-upload" action="/rhdata/rhdata_add/" :on-success="handleUploadSuccess" :on-error="handleUploadError"
                   :before-upload="beforeUpload">
          <el-button type="primary">点击上传配方对应的热力学数据</el-button>
        </el-upload>
        <div v-if="showMask" class="overlay"></div>
        <div class="progress_show">
          <el-progress v-show="showProgress" :percentage="uploadProgress" status="success"
                       :format="formatOverallProgress"></el-progress>
          <el-progress v-show="showProgress" :percentage="itemUploadProgress" status="success"
                       :format="formatItemProgress"></el-progress>
        </div>
        <span v-show="showProgress">总进度: {{ uploadProgress }}%, 当前进度: {{ itemUploadProgress }}%</span>
      </div>
      <div class="search-container">
        <el-input v-model="formulationId" placeholder="请输入配方ID"></el-input>
        <el-input v-model="temperatureId" placeholder="请输入温度"></el-input>
        <el-button type="primary" @click="fetchData">查询</el-button>
      </div>
    </div>

    <el-table :data="pagedData" style="width: 100%; margin-top: 20px;" stripe>
      <el-table-column prop="rh_id" label="数据编号" align="center"></el-table-column>
      <!-- <el-table-column prop="formulation_id_id" label="Formulation ID"></el-table-column>
      <el-table-column prop="temperature_id_id" label="Temperature ID"></el-table-column>
      <el-table-column prop="temp_mark" label="温度 °C"></el-table-column> -->
      <el-table-column prop="time_min" label="时间 (min)" align="center"></el-table-column>
      <!-- <el-table-column prop="time_s" label="Time (s)"></el-table-column> -->
      <el-table-column prop="temp" label="温度 °C" align="center"></el-table-column>
      <el-table-column prop="energy_storage_mod" label="储能模量" align="center"></el-table-column>
      <el-table-column prop="loss_mod" label="损耗模量" align="center"></el-table-column>
      <el-table-column prop="loss_factor" label="损耗因子" align="center"></el-table-column>
      <el-table-column prop="complex_viscosity" label="复数黏度" align="center"></el-table-column>
      <el-table-column prop="clearances" label="间隙" align="center"></el-table-column>
      <el-table-column prop="normal_force" label="法向力" align="center"></el-table-column>
      <el-table-column prop="torsion" label="扭矩" align="center"></el-table-column>
      <el-table-column prop="state_mark" label="状态" align="center"></el-table-column>
    </el-table>

    <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
                   layout="total ,prev, pager, next, jumper" :total="totalItems">
    </el-pagination>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showProgress: false,
      showMask: false,
      uploadProgress: 0,
      itemUploadProgress: 0,
      formulationId: '',
      temperatureId: '',
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      allData: [], //后端传入的所有数据
      pagedData: [], //某一页的数据
      markSuccess: true,
    };
  },
  mounted() {
  },
  methods: {
    formatOverallProgress() {
      return `总配方进度: ${this.uploadProgress}%`;
    },
    formatItemProgress() {
      return `当前配方进度: ${this.itemUploadProgress}%`;
    },
    startPollingProgress() {
      this.pollingTimer = setInterval(this.fetchProgress, 100); // 每隔一秒轮询一次
    },
    fetchProgress() {
      if (this.markSuccess === true) {
        // 向后端发送请求，获取数据处理进度信息
        axios.get('/rhdata/rhdata_Upload_Progress/')
            .then(response => {
              const progress = response.data.progress; // 假设后端返回的进度信息在 data.progress 中
              this.uploadProgress = progress; // 更新上传进度
              this.itemUploadProgress = response.data.item_progress;
              if (this.progress === 100 && this.itemUploadProgress === 100) {
                clearInterval(this.pollingTimer); // 数据处理完成后停止轮询
              }
            })
            .catch(error => {
              this.markSuccess = false;
              console.error('Failed to fetch progress:', error);
              clearInterval(this.pollingTimer); // 出错时停止轮询
            });
      } else {
        this.showMask = false;
        this.$message.error('文件上传失败!')
        clearInterval(this.pollingTimer);
      }
    },
    handleUploadError(error, file, fileList) {
      this.markSuccess = false;
      this.$message.error('文件格式有误，处理失败!')
    },
    handleUploadSuccess(response, file, fileList) {
      if (response.output) {
        this.$message.error(response.output)
        this.markSuccess = false;
      } else {
        this.markSuccess = true;
        axios.get('/rhdata/rhdata_Upload_Progress/').then(
            response => {
              this.uploadProgress = response.data.final_progress;
            }
        )
        clearInterval(this.pollingTimer); // 停止轮询进度条
        this.$message.success("文件上传成功!")
      }
      this.showMask = false; // 隐藏遮罩
      clearInterval(this.pollingTimer); // 停止轮询进度条
    },
    beforeUpload(file) {
      try {
        const isExcel =
            file.type === "application/vnd.ms-excel" ||
            file.type ===
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
        if (!isExcel) {
          this.$message.error("只能上传Excel文件");
          return false; // 阻止上传
        } else {
          this.showProgress = true;
          this.showMask = true;

          this.markSuccess = true;
          this.startPollingProgress();
        }
      } catch (error) {
        this.markSuccess = false;
        this.$message.error("只能上传Excel文件");
        return false; // 阻止上传
      }
      this.markSuccess = true;
      return true; // 允许上传
    },
    handleUploadProgress(event, file, fileList) {
      this.uploadProgress = event.percent || 0;
    },

    fetchData() {
      //  带参请求
      axios.get('/rhdata/rhdata_list/', {  //接口改一下
        params: {
          formulation_id_id: this.formulationId,
          temperature_id_id: this.temperatureId,
        }
      }).then(response => {
        this.allData = response.data.data_list;
        this.totalItems = this.allData.length;
        this.updatePageData();
        console.log(response.data)
        if (response.data['msg']) {
          this.$message.error(response.data.msg);
        } else {
          this.$message.success('数据查询成功!')
        }
      }).catch(error => {
        this.$message.error('没有找到该数据:' + error);
      });
    },
    updatePageData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.pagedData = this.allData.slice(start, end);  //这里会根据pagesize截取对应个数的items
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.updatePageData();
    }
  }
};
</script>

<style lang="less" scoped>
.progress_show {
  width: 300px;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.data-form {
  height: 90%;
  display: flex;
  flex-direction: column;
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;

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
