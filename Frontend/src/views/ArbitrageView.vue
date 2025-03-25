<template>
  <el-card class="card-box">
    <el-form :model="formData" label-width="auto" :label-position="'right'" width="600px" @submit.prevent="handleSubmit" >
      <el-form-item label="近月合约">
        <el-input v-model="formData.near_code" placeholder="输入近月合约代码，格式例如：CF2505" />
      </el-form-item>
      <el-form-item label="远月合约">
        <el-input v-model="formData.far_code" placeholder="输入远月合约代码，格式例如：CF2504" />
      </el-form-item>
      <el-form-item label="交易费用">
        <el-input-number v-model="formData.trading_fee" :precision="2" :step="0.1" />
      </el-form-item>
      <el-form-item label="交割费用">
        <el-input-number v-model="formData.delivery_fee" :precision="2" :step="0.1" />
      </el-form-item>
      <el-form-item label="资金费用">
        <el-input-number v-model="formData.capital_cost" :precision="2" :step="0.1" />
      </el-form-item>
      <el-form-item label="增值税">
        <el-input-number v-model="formData.vat" :precision="2" :step="0.1" />
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
</template>

<script lang="ts" setup>
import { reactive } from 'vue';
import axios from 'axios';

// 定义表单数据模型
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
  delivery_date: '',
  last_trade_day: 0,
  last_delivery_day: 0
});

// 处理表单提交
const handleSubmit = async () => {
  try {
    // 发送数据到后端
    const response = await axios.post('/api/your-endpoint', formData);
    console.log('Data submitted successfully:', response.data);
  } catch (error) {
    console.error('Error submitting data:', error);
  }
};

</script>

<style scoped>
.card-box {
  padding: 20px;
  width: 178vh;
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
</style>