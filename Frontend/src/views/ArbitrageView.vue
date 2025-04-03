<template>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-card class="card-box">
        <el-form :model="formData" label-width="16vh" :label-position="'right'" width="600px" @submit.prevent="handleSubmit" >
          <el-form-item label="近月合约">
            <el-input v-model="formData.near_code" placeholder="输入近月合约代码，格式例如：CF2505" />
          </el-form-item>
          <el-form-item label="远月合约">
            <el-input v-model="formData.far_code" placeholder="输入远月合约代码，格式例如：CF2504" />
          </el-form-item>
          <el-form-item label="交易费用">
            <el-input-number v-model="formData.trading_fee" :precision="2" :step="0.01" />
          </el-form-item>
          <el-form-item label="交割费用">
            <el-input-number v-model="formData.delivery_fee" :precision="2" :step="0.01" />
          </el-form-item>
          <el-form-item label="仓储费用">
            <el-input-number v-model="formData.storage_fee" :precision="2" :step="0.01" />
          </el-form-item>
          <el-form-item label="资金费用">
            <el-input-number v-model="formData.capital_cost" :precision="2" :step="0.01" />
          </el-form-item>
          <el-form-item label="增值税">
            <el-input-number v-model="formData.vat" :precision="2" :step="0.01" />
          </el-form-item>
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="formData.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            ></el-date-picker>
          </el-form-item>
          <el-form-item label="期货合约的最后交易日和交割日">
            <span>期货合约的最后交易日为合约月份的第</span>
            <el-input-number v-model="formData.last_trade_day" :precision="0" :step="1" style="width: 100px; margin: 0 5px;" />
            <span>个交易日。</span>
            <span>期货合约的最后交割日为最后交易日后的第</span>
            <el-input-number v-model="formData.last_delivery_day" :precision="0" :step="1" style="width: 100px; margin: 0 5px;" />
            <span>个交易日。</span>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit">提交</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
    <el-col :span="12">
      <el-card class="info-box" v-loading="loadingChart"
            element-loading-text="Loading..."
            :element-loading-spinner="svg"
            element-loading-svg-view-box="-10, -10, 50, 50">
        <el-tabs v-model="activeExchange">
          <!-- 大商所(DCE)表格 -->
          <el-tab-pane label="大商所" name="dce">
              <div class="table-wrapper">
                <el-table :data="infoForm.dce" border class="custom-table">
                  <el-table-column prop="品种" label="品种" width="120" />
                  <el-table-column prop="代码" label="代码" width="100" />
                  <el-table-column prop="合约单位（吨/手）" label="合约单位" width="150">
                    <template #default="{ row }">{{ row["合约单位（吨/手）"] }} 吨/手</template>
                  </el-table-column>
                  <el-table-column prop="最小交割单位" label="最小交割单位" width="180" />
                  <el-table-column prop="最后交易日" label="最后交易日" width="150" />
                  <el-table-column prop="交割月份" label="交割月份" width="150" />
                  <el-table-column prop="交割类型" label="交割类型" width="150" />
                  <el-table-column prop="仓单类型" label="仓单类型" width="180" />
                  <el-table-column prop="仓单有效期" label="仓单有效期" width="180" />
                  <el-table-column prop="仓储费（元/吨·天）" label="仓储费" width="150">
                    <template #default="{ row }">{{ row["仓储费（元/吨·天）"] }} 元/吨·天</template>
                  </el-table-column>
                  <el-table-column prop="注意" label="注意事项" />
                </el-table>
              </div>
          </el-tab-pane>

          <!-- 郑商所(CZCE)表格 -->
          <el-tab-pane label="郑商所" name="czce">
            <!-- 添加带有滚动样式的 div -->
            <div style="height: 80vh; overflow: auto;">
              <el-table :data="infoForm.czce" border style="width: 100%">
                <el-table-column prop="品种" label="品种" width="120" />
                <el-table-column prop="代码" label="代码" width="100" />
                <el-table-column prop="合约单位（吨/手）" label="合约单位" width="150">
                  <template #default="{row}">{{ row['合约单位（吨/手）'] }} 吨/手</template>
                </el-table-column>
                <el-table-column prop="最小交割单位" label="最小交割单位" width="180" />
                <el-table-column prop="交割月份" label="交割月份" width="150" />
                <el-table-column prop="交割类型" label="交割类型" width="150" />
                <el-table-column prop="仓单类型" label="仓单类型" width="180" />
                <el-table-column prop="是否生成仓单" label="是否生成仓单" width="150">
                  <template #default="{row}">
                    <el-tag :type="row['是否生成仓单'] ? 'success' : 'danger'">
                      {{ row['是否生成仓单'] ? '是' : '否' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="仓单有效期" label="仓单有效期" width="180" />
                <el-table-column prop="仓储费（元/吨·天）" label="仓储费" width="150">
                  <template #default="{row}">{{ row['仓储费（元/吨·天）'] }} 元/吨·天</template>
                </el-table-column>
                <el-table-column prop="注意" label="注意事项" />
              </el-table>
            </div>
          </el-tab-pane>

          <!-- 上期所能源中心(INE)表格 -->
          <el-tab-pane label="上期所、能源中心" name="ine">
            <!-- 添加带有滚动样式的 div -->
            <div style="height: 80vh; overflow: auto;">
              <el-table :data="infoForm.ine" border style="width: 100%">
                <el-table-column prop="品种" label="品种" width="120" />
                <el-table-column prop="代码" label="代码" width="100" />
                <el-table-column prop="合约单位（吨/手）" label="合约单位" width="150">
                  <template #default="{row}">{{ row['合约单位（吨/手）'] }} 吨/手</template>
                </el-table-column>
                <el-table-column prop="交割单位" label="交割单位" width="150" />
                <el-table-column prop="最后交易日" label="最后交易日" width="150" />
                <el-table-column prop="仓单有效期" label="仓单有效期" width="180" />
                <el-table-column prop="仓储费（元/吨·天）" label="仓储费" width="150">
                  <template #default="{row}">{{ row['仓储费（元/吨·天）'] }} 元/吨·天</template>
                </el-table-column>
                <el-table-column prop="注意" label="注意事项" />
              </el-table>
            </div>
          </el-tab-pane>

          <!-- 广期所(GFEX)表格 -->
          <el-tab-pane label="广期所" name="gfex">
            <!-- 添加带有滚动样式的 div -->
            <div style="height: 80vh; overflow: auto;">
              <el-table :data="infoForm.gfex" border style="width: 100%">
                <el-table-column prop="品种" label="品种" width="120" />
                <el-table-column prop="代码" label="代码" width="100" />
                <el-table-column prop="合约单位（吨/手）" label="合约单位" width="150">
                  <template #default="{row}">{{ row['合约单位（吨/手）'] }} 吨/手</template>
                </el-table-column>
                <el-table-column prop="最小交割单位" label="最小交割单位" width="180" />
                <el-table-column prop="最后交易日" label="最后交易日" width="150" />
                <el-table-column prop="交割月份" label="交割月份" width="150" />
                <el-table-column prop="交割类型" label="交割类型" width="150" />
                <el-table-column prop="仓单类型" label="仓单类型" width="180" />
                <el-table-column prop="仓单有效期" label="仓单有效期" width="180" />
                <el-table-column prop="仓储费（元/吨·天）" label="仓储费" width="150">
                  <template #default="{row}">{{ row['仓储费（元/吨·天）'] }} 元/吨·天</template>
                </el-table-column>
                <el-table-column prop="注意" label="注意事项" />
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { onMounted, reactive, ref } from 'vue';
import axios from 'axios';
import { apiUrl } from '@/config';

const loadingChart = ref(true)
const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `

const formData = reactive({
  near_code: '',
  far_code: '',
  storage_fee: 0,
  trading_fee: 0,
  delivery_fee: 0,
  capital_cost: 0,
  vat: 0,
  stamp_duty: 0,
  cost_tax: 0,
  // delivery_date: '',
  dateRange: ['', ''],
  // last_trade_day: 0,
  // last_delivery_day: 0,
});

// 处理表单提交
const handleSubmit = async () => {
  try {
    // 发送数据到后端
    const response = await axios.post(`${ apiUrl }/calculate/`, formData);
    console.log('Data submitted successfully:', response.data);
  } catch (error) {
    console.error('Error submitting data:', error);
  }
};


const activeExchange = ref('dce'); 

const infoForm = reactive({
    dce: [],
    czce: [],
    ine: [],
    gfex: []
});

onMounted(async () => {
    try {
        const response = await axios.get(`${apiUrl}/info/`);
        console.log(response.data);
        infoForm.dce = response.data.data.DCE;
        infoForm.czce = response.data.data.CZCE;
        infoForm.ine = response.data.data.INE;
        infoForm.gfex = response.data.data.GFEX;
        loadingChart.value = false;
    } catch (error) {
        console.error('读取商所数据有误', error);
    }
});

</script>

<style scoped>
.card-box {
  padding: 20px;
  /* width: 95vh; */
  height: 94vh;
}

.info-box {
  padding: 20px;
  /* width: 95vh; */
  height: 94vh;
}


.el-form {
  max-width: 800px;
  margin: 0 auto;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  width: 100%;
}

.el-input-number {
  width: 200px;
  margin: 0 5px;
}

.table-wrapper {
  height: 80vh; 
  overflow-y: auto;
  width: calc(100% - 20px);
  overflow-x: auto;
}

.custom-table .el-table__body-wrapper {
  overflow-x: hidden !important;
}
</style>    