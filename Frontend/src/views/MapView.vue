<template>
  <el-card><div v-html="htmlContent"></div></el-card>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const htmlContent = ref<string>('');

onMounted(async () => {
  try {
    // const response = await axios.get('/src/assets/cottonFactory.html');
    // htmlContent.value = response.data;
  } catch (error) {
    console.error('读取 HTML 文件失败:', error);
  }
});
</script>

<style scoped>
</style>