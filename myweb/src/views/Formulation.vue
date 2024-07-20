<template>
  <div class="allviews">
    <div class="add">
      <el-dialog title="配方数据" :visible.sync="dialogFormVisible" :before-close="handleClose">
        <el-form ref="form" :model="form" :inline="true" :rules="rules">
          <el-form-item label="配方id" prop="formulation_id" :label-width="formLabelWidth">
            <el-input v-model="form.formulation_id" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="PBT" :label-width="formLabelWidth">
            <el-input v-model="form.pbt" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="TDI" :label-width="formLabelWidth">
            <el-input v-model="form.tdi" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="三苯基铋" :label-width="formLabelWidth">
            <el-input v-model="form.tri_bis" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="A3" :label-width="formLabelWidth">
            <el-input v-model="form.athree" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="T313" :label-width="formLabelWidth">
            <el-input v-model="form.bonding_agent" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="AP(40-60目)" :label-width="formLabelWidth">
            <el-input v-model="form.ap_small" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="AP(100-140目)" :label-width="formLabelWidth">
            <el-input v-model="form.ap_large" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="AI粉" :label-width="formLabelWidth">
            <el-input v-model="form.ai_powder" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="交联剂TMP" :label-width="formLabelWidth">
            <el-input v-model="form.tmp" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="二乙二醇" :label-width="formLabelWidth">
            <el-input v-model="form.die_gly" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="三乙二醇" :label-width="formLabelWidth">
            <el-input v-model="form.tri_glycol" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="后添TDI" :label-width="formLabelWidth">
            <el-input v-model="form.add_tdi" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </div>
      </el-dialog>
      <div class="manage">
        <el-button type="primary" @click="setVisible">
          + 新增
        </el-button>
        <el-form :model="formulation" inline="true" class="search">
          <el-form-item>
            <el-input placeholder="请输入配方ID" v-model="formulation.id" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">查 询 </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <!-- 表格 -->
    <div class="common-tabel">
      <el-table :data="tableData" style="width: 100%; max-height: 90vh; overflow: auto;" class="table" stripe >
        <el-table-column prop="formulation_id" label="配方ID" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="pbt" label="PBT" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="tdi" label="TDI" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="tri_bis" label="三苯基铋" width="80px" align="center">
        </el-table-column>
        <el-table-column prop="athree" label="A3" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="bonding_agent" label="T313" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="ap_small" label="AP(40-60目)" align="center">
        </el-table-column>
        <el-table-column prop="ap_large" label="AP(100-140目)" align="center">
        </el-table-column>
        <el-table-column prop="ai_powder" label="AI粉" width="70px" align="center">
        </el-table-column>
        <el-table-column prop="tmp" label="交联剂TMP" align="center">
        </el-table-column>
        <el-table-column prop="die_gly" label="二乙二醇" align="center">
        </el-table-column>
        <el-table-column prop="tri_glycol" label="三乙二醇" align="center">
        </el-table-column>
        <el-table-column prop="add_tdi" label="后添TDI" width="80px" align="center">
        </el-table-column>
        <el-table-column label="操作" width="150px" align="center">
          <template slot-scope="scope">
            <el-button @click="handleEdit(scope.row.formulation_id, scope.row)" size="mini">
              编辑
            </el-button>
            <el-button @click="handleDelete(scope.row.formulation_id, scope.row)" type="danger" size="mini">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pager">
        <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
                       layout="total, prev, pager, next, jumper" :total="totalItems">
          <!-- total的计算 -->
        </el-pagination>
      </div>

    </div>
  </div>
</template>

<style lang="less" scoped>
.allviews {
  height: 90%;
  .manage {
    display: flex;
    justify-content: space-between;
    align-items: start;
  }
}
</style>

<script>
import {getFormulation, addFormulation, editFormulation, delFormulation} from '@/api'

export default {
  data() {
    return {
      //tableHeight: '500px',
      formulation: {  //用于规定必填项
        id: ''
      },
      totalItems: 0,
      allData: [],
      tableData: [],
      currentFormulation: null,
      modalType: 0,  //0表示新增的弹窗 1表示编辑
      currentPage: 1,
      pageSize: 10,
      tableHeight: 0,
      dialogFormVisible: false,
      form: {
        formulation_id: '',
        formulation_name: '',
        pbt: '',
        tdi: '',
        tri_bis: '',
        athree: '',
        bonding_agent: '',
        ap_small: '',
        ap_large: '',
        ai_powder: '',
        tmp: '',
        die_gly: '',
        tri_glycol: '',
        add_tdi: ''
      },
      rules: {   //表单的填写规则
        formulation_id: [
          {required: true, message: '请输入id', trigger: 'blur'}
        ]
      },
      formLabelWidth: '120px',
    };
  },
  mounted() {
    this.getList()
  },
  methods: {
    async getList() {
      await getFormulation({params: {...this.pageData, ...this.formulation}}).then(({data}) => {
        if (data && data.formulations) {
          this.allData = data.formulations;
          this.totalItems = this.allData.length;
          this.updatePageData();
          this.$message.success('数据查询成功!')
        } else {
          this.tableData = [];
        }

      }).catch(error => {
        this.$message.error('没有查询到对应的配方!');
      });
    },
    async onSubmit() {
      // 查询搜索
      await this.getList()
    },
    addFormulation(newFormulation) {
      addFormulation(newFormulation).then(response => {
        this.getList();
        this.dialogFormVisible = false;
        this.$message.success('新配方已被添加!');
      }).catch(error => {
        this.$message.error('新配方添加失败!');
      });
    },
    editFormulation(formulation) {
      editFormulation(formulation).then(response => {
        this.getList();
        this.dialogFormVisible = false;
        this.$message.success('配方编辑成功!');
      }).catch(error => {
        this.$message.error('配方编辑失败!' + error);
      });
    },
    handleClose() {
      //点击关闭或者取消 就清除内容 然后关闭窗口
      this.$refs.form.resetFields()
      this.dialogFormVisible = false
    },
    submitForm() {
      this.$refs.form.validate(valid => {
        if (valid) {
          if (this.modalType === 0) {
            this.addFormulation(this.form);
          } else {
            this.editFormulation(this.form);
          }
          this.$refs.form.resetFields();
        }
      });
    },
    setVisible() {
      this.dialogFormVisible = true
      this.modalType = 0
    },
    handleEdit(index, row) {
      this.modalType = 1
      this.dialogFormVisible = true
      this.form = JSON.parse(JSON.stringify(row))
    },
    handleDelete(index, row) {
      this.$confirm(' 配方删除后将会级联删除对应的热力学数据，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delFormulation({id: row.formulation_id}).then(() => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
          this.getList();  //重新获取列表

        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    updatePageData() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.tableData = this.allData.slice(start, end);  //这里会根据pagesize截取对应个数的items
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.getList()

    }
  },

}
</script>
