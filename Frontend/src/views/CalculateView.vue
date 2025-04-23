<template>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>棉花升贴水参数配置</span>
        </div>
      </template>
  
      <div class="toolbar">
        <el-select v-model="selectedConfigName" placeholder="选择参数版本" style="width: 200px">
          <el-option
            v-for="config in configList"
            :key="config.name"
            :label="config.name"
            :value="config.name"
          />
        </el-select>
        <el-button @click="handleLoadConfig">加载</el-button>
        <el-input v-model="selectedConfigName" placeholder="输入参数模板名" style="width: 200px" />
        <el-button type="success" @click="handleSaveConfig">保存为新版本</el-button>
      </div>
  
      <el-divider>长度/比强参数</el-divider>
      <el-table :data="lengthStrengthParams" border style="width: 100%; margin-bottom: 20px;" fit>
        <el-table-column prop="range" label="长度范围" min-width="120" />
        <el-table-column
          v-for="price in priceHeaders"
          :key="price"
          :label="price"
          :prop="price"
          min-width="60"
        >
          <template #default="{ row }">
            <el-input v-model="row[price]" size="small" />
          </template>
        </el-table-column>
      </el-table>
  
      <el-row :gutter="20">
        <el-col :span="12">
          <el-divider>马克隆值参数</el-divider>
          <el-table :data="micronaireParams" border style="width: 100%; table-layout: auto;" fit>
            <el-table-column prop="range" label="马克隆值范围" />
            <el-table-column prop="value" label="升贴水值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
  
        <el-col :span="12">
          <el-divider>手扯长度/机扯长度参数</el-divider>
          <el-table :data="handMachineLengthParams" border style="width: 100%" fit>
            <el-table-column prop="range" label="长度范围" />
            <el-table-column prop="value" label="升贴水值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
  
        <el-col :span="12">
          <el-divider>轧工质量参数</el-divider>
          <el-table :data="processingQualityParams" border style="width: 100%" fit>
            <el-table-column prop="condition" label="条件" />
            <el-table-column prop="value" label="升贴水值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
  
        <el-col :span="12">
          <el-divider>产地参数</el-divider>
          <el-table :data="originParams" border style="width: 100%" fit>
            <el-table-column prop="region" label="地区" />
            <el-table-column prop="value" label="升贴水值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
  
        <el-col :span="12">
          <el-divider>纤维品质参数</el-divider>
          <el-table :data="fiberQualityParams" border style="width: 100%" fit>
            <el-table-column prop="condition" label="品质条件" />
            <el-table-column prop="value" label="升贴水值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
  
        <el-col :span="12">
          <el-divider>拒收标准</el-divider>
          <el-table :data="rejectionCriteria" border style="width: 100%" fit>
            <el-table-column prop="parameter" label="参数" />
            <el-table-column prop="value" label="拒收值">
              <template #default="{ row }">
                <el-input v-model="row.value" size="small" />
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { ElMessage } from 'element-plus'
  
  // 配置管理
  const configList = ref([
    { name: '2425建发_升帖水' },
    { name: '默认配置' }
  ])
  const selectedConfigName = ref('2425建发_升帖水')
  
  // 长度/比强参数
  const priceHeaders = ref(['$25', '$26', '$26.5', '$27', '$27.5', '$28', '$28.5', '$29', '$30'])
  const lengthStrengthParams = ref([
    { range: 'L27-27.9', '$25': -600, '$26': -400, '$26.5': -350, '$27': -250, '$27.5': -200, '$28': -150, '$28.5': -150, '$29': -150, '$30': -150 },
    { range: 'L28-28.4', '$25': -500, '$26': -200, '$26.5': -175, '$27': -75, '$27.5': -25, '$28': 25, '$28.5': 25, '$29': 50, '$30': 75 },
    { range: 'L28.5-28.9', '$25': -500, '$26': -175, '$26.5': -150, '$27': -50, '$27.5': 0, '$28': 50, '$28.5': 50, '$29': 75, '$30': 100 },
    { range: 'L29-29.9', '$25': -500, '$26': -150, '$26.5': -125, '$27': -25, '$27.5': 25, '$28': 75, '$28.5': 75, '$29': 150, '$30': 200 },
    { range: 'L30+', '$25': -500, '$26': -125, '$26.5': -100, '$27': 0, '$27.5': 50, '$28': 125, '$28.5': 125, '$29': 200, '$30': 250 }
  ])
  
  const micronaireParams = ref([
    { range: '3.0-3.2', value: -400 },
    { range: '3.3-3.4', value: -400 },
    { range: '3.5-3.6', value: -400 },
    { range: '3.7-3.8', value: -200 },
    { range: '3.9', value: 0 },
    { range: '4.0-4.2', value: 0 },
    { range: '4.3-4.7', value: 30 },
    { range: '4.8', value: 0 },
    { range: '4.9', value: 0 },
    { range: '5.0-5.1', value: -100 },
    { range: '5.2-5.3', value: -200 },
    { range: '5.4以上', value: -200 }
  ])
  
  const handMachineLengthParams = ref([
    { range: '手1.0以下', value: 30 },
    { range: '手1.1-1.5', value: 30 },
    { range: '手1.6-1.9', value: 30 },
    { range: '手2.0-2.5', value: 30 },
    { range: '手2.6-2.9', value: 0 },
    { range: '机2.0以下', value: 30 },
    { range: '机2.0-2.5', value: 30 },
    { range: '机2.6-2.9', value: 0 },
    { range: '3.0-3.1', value: -50 },
    { range: '3.2', value: -100 },
    { range: '3.3-3.5', value: -100 },
    { range: '3.6-3.9', value: -300 },
    { range: '4.0-4.5', value: -500 },
    { range: '4.6-4.9', value: -1000 },
    { range: '5.0-5.5', value: -1000 },
    { range: '5.6以上', value: 1000 }
  ])
  
  const processingQualityParams = ref([
    { condition: 'P3>10%', value: -100 },
    { condition: 'P3>30%', value: -200 },
    { condition: 'P3>50%', value: -300 },
    { condition: '异纤>1包', value: -200 }
  ])
  
  const originParams = ref([
    { region: '金电', value: 0 },
    { region: '库尔勒', value: 0 },
    { region: '博乐', value: -30 },
    { region: '阿克苏', value: 0 },
    { region: '喀什', value: -50 },
    { region: '乌鲁木齐', value: 30 },
    { region: '哈密吐鲁番', value: 0 },
    { region: '其它', value: 0 }
  ])
  
  const fiberQualityParams = ref([
    { condition: '31及以上≥85%&21及以上≥80%', value: 0 },
    { condition: '31及以上≥85%&21及以上≥50%', value: -50 },
    { condition: '31及以上≥85%&21及以上<50%', value: 0 },
    { condition: '41/12及以上≥85%&31及以上≥50%', value: -50 },
    { condition: '41/12及以上≥85%&31及以上<50%', value: -100 },
    { condition: '15% <41/12以下≤30%', value: -350 },
    { condition: '30% <41/12以下≤50%', value: -550 },
    { condition: '41/12以下>50%', value: -800 }
  ])
  
  const rejectionCriteria = ref([
    { parameter: '长度', value: '<27' },
    { parameter: '强力', value: '<25' },
    { parameter: '马值', value: '<3.5' },
    { parameter: '马值', value: '>6' },
    { parameter: '含杂', value: '>4.5' }
  ])
  
  const handleLoadConfig = () => {
    ElMessage.info(`加载参数配置: ${selectedConfigName.value}`)
  }
  
  const handleSaveConfig = () => {
    const versionName = prompt('请输入新配置名称')
    if (versionName) {
      configList.value.push({ name: versionName })
      ElMessage.success(`已保存为新版本: ${versionName}`)
    }
  }
  </script>
  
  <style scoped>
  .box-card {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
  }
  .toolbar {
    margin-bottom: 15px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .el-divider {
    margin: 20px 0;
  }
  .el-table :deep(.cell),
  .el-table :deep(th > .cell) {
    text-align: center;
  }
  </style>
  