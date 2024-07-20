<template>
  <div class="data-form">
    <div class="top">
      <div class="search-container">
        <el-input v-model="formulationId" placeholder="请输入配方ID"></el-input>
        <el-input v-model="temperatureId" placeholder="请输入温度"></el-input>
        <div class="button-group">

          <el-button @click="showTrainForm = true;" type="primary">训练</el-button>
          <el-button @click="showPredictForm = true;" type="success">预测</el-button>
<!--          <el-button v-if="predictParams.output_path" type="primary" @click="downloadModel">下载模型文件</el-button>-->
          <el-button type="success" @click="fetchData">查询预测结果</el-button>
          <el-button type="success" @click="downloadPredictResult">下载预测结果</el-button>
        </div>
      </div>
    </div>

    <el-dialog :visible="showDialog" title="训练提示" @close="showDialog = false" width="30%"
      custom-class="training-dialog">
      <p>训练已完成</p>
    </el-dialog>

    <el-dialog :visible="showTrainForm" title="训练参数配置" width="500px" @close="showTrainForm = false" class="btnright">
      <el-form :model="inputParams" label-width="120px">
        <el-form-item label="学习率">
          <el-input v-model="inputParams.learning_rate" placeholder="请输入学习率"></el-input>
        </el-form-item>
        <el-form-item label="批大小">
          <el-input v-model="inputParams.batch_size" placeholder="请输入批大小"></el-input>
        </el-form-item>
        <el-form-item label="训练轮数">
          <el-input v-model="inputParams.max_epochs" placeholder="请输入训练轮数"></el-input>
        </el-form-item>
        <el-form-item label="输入时序窗口">
          <el-input v-model="inputParams.in_chunk_len" autosize="" placeholder="请输入输入时序窗口的大小"></el-input>
        </el-form-item>
        <el-form-item label="输出时序窗口">
          <el-input v-model="inputParams.out_chunk_len" placeholder="请输入输出时序窗口的大小"></el-input>
        </el-form-item>
        <div class="button-container" style="display: flex; justify-content: flex-end;">
          <el-button type="primary" @click="trainModel(inputParams)">确定</el-button>
          <el-button @click="showTrainForm = false">取消</el-button>
        </div>
        <div v-if="showMask" class="overlay"></div>
      </el-form>
    </el-dialog>


    <div>
      <input type="file" id="fileInput" style="display:none;">
    </div>

    <el-dialog :visible="showPredictForm" title="预测参数配置" width="400px" @close="showPredictForm = false"
      class="btnright">
      <el-form :model="predictParams" label-width="70px">
        <el-form-item label="预测长度">
          <el-input v-model="predictParams.recursive_chunk_len" placeholder="请输入预测长度"></el-input>
        </el-form-item>
        <!-- <el-form-item label="模型保存地址" label-width="auto">
          <el-upload action="#" ref="modelUpload" :show-file-list="false" :on-success="handleModelUploadSuccess"
            :on-remove="handleModelUploadRemove" :file-list="modelFileList">
            <el-button slot="trigger" size="mini" type="primary">选择文件</el-button>
          </el-upload>
        </el-form-item> -->
        <!-- <el-form-item label="预测结果地址">
          <el-upload action="#" ref="predictUpload" :show-file-list="false" :on-success="handlePredictUploadSuccess"
            :on-remove="handlePredictUploadRemove" :file-list="predictFileList">
            <el-button slot="trigger" size="mini" type="primary">选择文件</el-button>
          </el-upload>
        </el-form-item> -->
        <div class="button-container" style="display: flex; justify-content: flex-end;">
          <el-button type="primary" size="small" @click="handlePredict">确定</el-button>
          <el-button size="small" @click="showPredictForm = false; showMask = false">取消</el-button>
        </div>
        <div v-if="showMask" class="overlay"></div>
      </el-form>
    </el-dialog>


    <el-dialog :visible="trainingInProgress || predictionInProgress" center :show-close="false">
      <div v-if="trainingInProgress">训练中</div>
      <div v-if="predictionInProgress">预测中</div>
      <!-- <el-progress :percentage="progress" :color="trainingInProgress ? '#0c64e8' : '#13ce66'"></el-progress> -->
    </el-dialog>

    <el-table :data="pagedData" style="width: 100%; margin-top: 20px;" stripe>
<!--      <el-table-column prop="rh_id" label="数据编号" align="center" width="80px"></el-table-column>-->
      <el-table-column prop="time_min_r" label="时间 (min)" align="center" width="0px"></el-table-column>
      <el-table-column prop="temp_r" label="温度 °C" align="center" width="80px"></el-table-column>
      <el-table-column prop="energy_storage_mod_r" label="储能模量(真实)" align="center"></el-table-column>
      <el-table-column prop="energy_storage_mod_p" label="储能模量(预测)" align="center"></el-table-column>
      <el-table-column prop="loss_mod_r" label="损耗模量(真实)" align="center"></el-table-column>
      <el-table-column prop="loss_mod_p" label="损耗模量(预测)" align="center"></el-table-column>
      <el-table-column prop="loss_factor_r" label="损耗因子(真实)" align="center"></el-table-column>
      <el-table-column prop="loss_factor_p" label="损耗因子(预测)" align="center"></el-table-column>
      <el-table-column prop="complex_viscosity_r" label="复数黏度(真实)" align="center"></el-table-column>
      <el-table-column prop="complex_viscosity_p" label="复数黏度(预测)" align="center"></el-table-column>
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
      showMask: false,
      formulationId: '',
      temperatureId: '',
      showDialog: false,
      showTrainForm: false,
      showPredictForm: false,
      currentPage: 1,
      pageSize: 10,
      totalItems: 0,
      allData: [], // 后端传入的所有数据
      pagedData: [], // 某一页的数据
      inputParams: {
        learning_rate: '',
        batch_size: '',
        max_epochs: '',
        in_chunk_len: '',
        out_chunk_len: ''
      },
      predictParams: {
        recursive_chunk_len: '',
      },
      trainingInProgress: false,
      predictionInProgress: false,
      progress: 0,
    };
  },
  methods: {
    fetchData() {
      //  带参请求
      axios.get('/rhdata/truth_predicted_list/', {
        params: {
          formulation_id: this.formulationId,
          temperature_id: this.temperatureId
        }
      }).then(response => {
        this.allData = response.data;
        this.totalItems = this.allData.length;
        this.updatePageData();
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
    },


    trainModel(params) {   //传入输入的训练数据
      console.log(params);
      this.showMask = true;
      this.trainingInProgress = true;
      // 将训练参数、配方id、温度一起传给后端
      axios.get('/rhdata/process_train/', {
        formulationId: this.formulationId,
        temperatureId: this.temperatureId,
        learning_rate: params.learning_rate,
        batch_size: params.batch_size,
        max_epochs: params.max_epochs,
        in_chunk_len: params.in_chunk_len,
        out_chunk_len: params.out_chunk_len
      }).then(response => {
        // 处理训练结果
        this.$message.success('训练完成:' + response.data.msg);
        this.showMask = false;
        this.trainingInProgress = false;
        this.showTrainForm = false; // 关闭参数配置表单
        this.showDialog = true; // 弹出训练完成提示框
      }).catch(error => {
        this.$message.error('训练失败:' + error);
        this.showMask = false;
        this.trainingInProgress = false;
      });
    },
    handlePredict() {
      this.showMask = true;
      this.predictionInProgress = true;
      // 只将id和温度传给后端
      axios.post('/rhdata/process_predict/', {
        formulationId: this.formulationId,
        temperatureId: this.temperatureId,
      }).then(response => {
        // 处理预测结果
        this.$message.success('预测完成:' + response.data.msg);
        this.showMask = false;
        this.predictionInProgress = false;
      }).catch(error => {
        this.$message.error('预测失败:' + error);
        this.showMask = false;
        this.predictionInProgress = false;
      });
    },

    downloadPredictResult() {
      axios({
        url: '/rhdata/get_predicted_result/', // 替换成你实际的后端 API 地址
        method: 'GET',
        responseType: 'blob', // 指定响应类型为二进制流
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'predicted_data.xlsx');
        document.body.appendChild(link);
        link.click();
      }).catch(error => {
        this.$message.error('下载失败:'+ error);
        this.$message.warning('下载失败，请重试');
      });
    }
  }
};
</script>

<style lang="less" scoped>
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
  /* 使用视窗高度作为高度 */
  display: flex;
  flex-direction: column;

  .top {
    display: flex;
    justify-content: end;
    align-items: center;
    margin-bottom: 20px;

    .search-container {
      display: flex;
      align-items: center;

      .el-input {
        width: 150px;
        margin-right: 20px;
      }
    }

    .button-group {
      display: flex;
      align-items: center;

      .el-button {
        justify-content: end;
        margin-right: 10px;
      }
    }
  }
}
</style>