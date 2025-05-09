<template>
  <div class="cotton-config-container">
    <!-- 顶部导航栏 -->
    <el-menu 
      mode="horizontal" 
      v-model="activeTab" 
      @select="handleTabChange"
      class="config-nav"
    >
      <el-menu-item index="premium">棉花升贴水参数配置</el-menu-item>
      <el-menu-item index="certificate">上传证书数据</el-menu-item>
      <el-menu-item index="policy">政策性参数修改</el-menu-item>
    </el-menu>

    <!-- 内容区域 -->
    <div class="config-content">
      <!-- 升贴水参数配置 -->
      <div v-show="activeTab === 'premium'">
        <el-card class="box-card">
          <div class="toolbar">
            <el-select v-model="selectedConfigName" placeholder="选择参数版本" style="width: 200px">
              <el-option
                v-for="config in configList"
                :key="config.id"
                :label="config.name"
                :value="config.id"
              />
            </el-select>
            <el-button @click="handleLoadConfig">加载</el-button>
            <el-button type="danger" @click="confirmDeleteConfig" :disabled="!selectedConfigName">删除</el-button>
            <el-input v-model="newConfigName" placeholder="输入参数模板名" style="width: 200px" />
            <el-button type="success" @click="handleSaveConfig">保存为新版本</el-button>
          </div>

          <el-divider>长度/比强参数</el-divider>
          <el-table :data="allParams.lengthStrengthParams" border style="width: 100%; margin-bottom: 20px;" fit>
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
              <el-table :data="allParams.micronaireParams" border style="width: 100%; table-layout: auto;" fit>
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
              <el-table :data="allParams.handMachineLengthParams" border style="width: 100%" fit>
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
              <el-table :data="allParams.processingQualityParams" border style="width: 100%" fit>
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
              <el-table :data="allParams.originParams" border style="width: 100%" fit>
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
              <el-table :data="allParams.fiberQualityParams" border style="width: 100%" fit>
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
              <el-table :data="allParams.rejectionCriteria" border style="width: 100%" fit>
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
      </div>

      <!-- 证书数据上传 -->
      <div v-show="activeTab === 'certificate'">
        <el-card class="upload-card">
          <template #header>
            <div class="card-header">
              <span>棉花品质证书上传</span>
              <el-button 
                type="primary" 
                size="small"
                @click="downloadTemplate"
                :icon="Download">
                下载模板
              </el-button>
            </div>
          </template>

          <!-- 文件上传区域 -->
          <el-upload
            class="cert-uploader"
            drag
            :action="uploadUrl"
            :headers="headers"
            :data="uploadParams"
            :before-upload="validateFile"
            :on-success="handleSuccess"
            :on-error="handleError"
            :show-file-list="false"
            accept=".xlsx,.xls,.csv">
            <el-icon class="upload-icon"><UploadFilled /></el-icon>
            <div class="upload-text">
              <p>拖拽证书文件到此处或</p>
              <el-button type="primary">点击上传</el-button>
            </div>
            <template #tip>
              <div class="upload-tips">
                <el-tag type="info">支持格式: XLS/XLSX/CSV</el-tag>
                <el-tag type="info">最大文件: 10MB</el-tag>
              </div>
            </template>
          </el-upload>

          <!-- 上传历史表格 -->
          <el-table 
            :data="certificateList" 
            v-loading="loading"
            style="width: 100%; margin-top: 20px"
            empty-text="暂无上传记录">
            <el-table-column prop="cert_id" label="证书编号" width="180" />
            <el-table-column prop="original_name" label="文件名" show-overflow-tooltip />
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="statusMap[row.status].type">
                  {{ statusMap[row.status].text }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="upload_time" label="上传时间" width="180" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button 
                  size="small" 
                  @click="previewCertificate(row.cert_id)"
                  :disabled="row.status !== 'success'">
                  计算结果
                </el-button>
                <el-popconfirm 
                  title="确认删除此证书?" 
                  @confirm="deleteCertificate(row.cert_id)">
                  <template #reference>
                    <el-button size="small" type="danger">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>

      <!-- 政策性参数 -->
      <div v-show="activeTab === 'policy'">
        <el-card class="policy-params-card">
          <template #header>
            <div class="card-header">
              <span>政策性参数修改</span>
              <el-button type="primary" @click="saveParams" style="float: right">保存修改</el-button>
            </div>
          </template>

          <el-table :data="policyParams" border style="width: 100%" :span-method="arraySpanMethod">
            <el-table-column prop="index" label="序号" width="80" align="center" />
            <el-table-column prop="indicator" label="指标" width="150" align="center" />
            <el-table-column
            v-for="(col, idx) in premiumCols"
            :key="'premium_' + idx"
            :label="idx === 0 ? '升水替代品（元/吨）' : ''"
            align="center"
            width="120"
          >
            <template #default="{ row, $index }">
              <el-input-number
                v-if="$index % 2 === 1"
                v-model="row['premium_' + idx]"
                :min="-1000"
                :max="1000"
                :step="50"
                controls-position="right"
                size="small"
              />
              <span v-else>{{ row['premium_' + idx] || '-' }}</span>
            </template>
          </el-table-column>


            <el-table-column prop="base" label="基准品" width="120" align="center">
              <template #default="{ row, $index }">
                <span v-if="$index % 2 === 0">{{ row.base || '-' }}</span>
              </template>
            </el-table-column>

            <el-table-column label="贴水替代品（元/吨）" align="center">
              <el-table-column v-for="(col, idx) in discountCols" :key="'discount_'+idx" :label="col" align="center" width="120">
                <template #default="{ row, $index }">
                  <el-input-number
                    v-if="$index % 2 === 1"
                    v-model="row['discount_' + idx]"
                    :min="-1000"
                    :max="1000"
                    :step="50"
                    controls-position="right"
                    size="small"
                  />
                  <span v-else>{{ row['discount_' + idx] || '-' }}</span>
                </template>
              </el-table-column>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { apiUrl } from '@/config'

// 配置管理
const configList = ref([])
const selectedConfigName = ref('')
const newConfigName = ref('')

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

// 当前激活的标签页
const activeTab = ref('premium')

// 证书上传相关数据
const certificateList = ref([
  { name: '2023年度质量证书', date: '2023-05-15', status: '已验证' },
  { name: '2023年度产地证书', date: '2023-05-10', status: '待审核' }
])




// 切换标签页
const handleTabChange = (index) => {
  activeTab.value = index
}

// 上传成功处理
const handleUploadSuccess = (response) => {
  // 处理上传成功逻辑
}

// 保存政策性参数
const savePolicyParams = () => {
  // 保存逻辑
}

// 表格列配置
const premiumCols = ref(['11', '21'])
const discountCols = ref(['41', '12', '22'])

// 政策参数数据
const policyParams = ref([
  // 颜色级
  { 
    index: 1, 
    indicator: '颜色级',
    premium_0: '11', premium_1: '21', premium_2: '31', premium_3: '41', premium_4: '12', premium_5: '22',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 300, premium_1: 150, premium_2: 0, premium_3: -350, premium_4: -300, premium_5: -500,
    base: '',
    discount_0: ''
  },
  // 长度mm
  { 
    index: 2, 
    indicator: '长度mm',
    premium_0: '≥30', premium_1: '29', premium_2: '28', premium_3: '', premium_4: '', premium_5: '',
    base: '',
    discount_0: '27'
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 400, premium_1: 200, premium_2: 0, premium_3: '', premium_4: '', premium_5: '',
    base: '',
    discount_0: -300
  },
  // 马克隆值
  { 
    index: 3, 
    indicator: '马克隆值',
    premium_0: 'A', premium_1: 'B(B1, B2)', premium_2: 'C2', premium_3: '', premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 100, premium_1: 0, premium_2: '', premium_3: -100, premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  // 断裂比强度
  { 
    index: 4, 
    indicator: '断裂比强度',
    premium_0: 'S1', premium_1: 'S2', premium_2: 'S3', premium_3: 'S4', premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 300, premium_1: 150, premium_2: 0, premium_3: -250, premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  // 长度整齐度
  { 
    index: 5, 
    indicator: '长度整齐度',
    premium_0: 'U1', premium_1: 'U2', premium_2: 'U3', premium_3: 'U4', premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 300, premium_1: 200, premium_2: 0, premium_3: -200, premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  // 轧工质量
  { 
    index: 6, 
    indicator: '轧工质量',
    premium_0: 'P1', premium_1: 'P2', premium_2: 'P3', premium_3: '', premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: 100, premium_1: 0, premium_2: '', premium_3: -300, premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  // 异性纤维
  { 
    index: 7, 
    indicator: '异性纤维',
    premium_0: '/', premium_1: '发现未超过1包的', premium_2: '发现超过1包的，每多发现1包增加贴水', premium_3: '', premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  },
  { 
    index: '', 
    indicator: '升贴水',
    premium_0: '/', premium_1: 0, premium_2: '', premium_3: -200, premium_4: '', premium_5: '',
    base: '',
    discount_0: ''
  }
])

// 所有参数数据
const allParams = ref({
  lengthStrengthParams,
  micronaireParams,
  handMachineLengthParams,
  processingQualityParams,
  originParams,
  fiberQualityParams,
  rejectionCriteria,
  policyParams
})


// 合并单元格方法
const arraySpanMethod = ({ rowIndex, columnIndex }) => {
  if (columnIndex === 0 || columnIndex === 1) {
    if (rowIndex % 2 === 0) {
      return {
        rowspan: 2,
        colspan: 1
      }
    } else {
      return {
        rowspan: 0,
        colspan: 0
      }
    }
  }
  return {
    rowspan: 1,
    colspan: 1
  }
}

// 保存参数
const saveParams = () => {
  console.log('保存的参数数据:', policyParams.value)
  ElMessage.success('参数保存成功')
}

// 加载配置列表
const loadConfigList = async () => {
  try {
    const response = await axios.get(`${ apiUrl }/calculate/configs/`)
    configList.value = response.data.data
    if (configList.value.length > 0) {
      selectedConfigName.value = configList.value[0].id
    }
  } catch (error) {
    ElMessage.error('加载配置列表失败')
    console.error(error)
  }
}

// 加载配置
const handleLoadConfig = async () => {
  try {
    const response = await axios.get(`${apiUrl}/calculate/configs/${selectedConfigName.value}/`)
    const configData = response.data.data // 根据后端返回结构调整
    
    // 逐个更新每个参数组
    lengthStrengthParams.value = configData.length_strength_params || []
    micronaireParams.value = configData.micronaire_params || []
    handMachineLengthParams.value = configData.hand_machine_length_params || []
    processingQualityParams.value = configData.processing_quality_params || []
    originParams.value = configData.origin_params || []
    fiberQualityParams.value = configData.fiber_quality_params || []
    rejectionCriteria.value = configData.rejection_criteria || []
    policyParams.value = configData.policy_params || []
    
    ElMessage.success(`配置加载成功: ${configData.name}`)
  } catch (error) {
    ElMessage.error('加载失败: ' + error.response?.data?.error || error.message)
    console.error('加载配置错误:', error)
  }
}

// 删除配置确认对话框
const confirmDeleteConfig = () => {
  if (!selectedConfigName.value) {
    ElMessage.warning('请选择要删除的配置')
    return
  }

  const currentConfig = configList.value.find(c => c.id === selectedConfigName.value)
  
  ElMessageBox.confirm(
    `确定要永久删除配置 "${currentConfig.name}" 吗？此操作不可恢复。`,
    '警告',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    handleDeleteConfig()
  }).catch(() => {
    ElMessage.info('删除操作已取消')
  })
}

// 执行删除操作
const handleDeleteConfig = async () => {
  try {
    const response = await axios.delete(`${apiUrl}/calculate/configs/${selectedConfigName.value}/`)
    ElMessage.success('配置删除成功')
    loadConfigList() // 刷新配置列表
    selectedConfigName.value = '' // 清空选择
  } catch (error) {
    ElMessage.error('删除配置失败: ' + (error.response?.data?.message || error.message))
    console.error('删除配置错误详情:', error.response?.data || error)
  }
}


// 保存配置
const handleSaveConfig = async () => {
  if (!newConfigName.value) {
    ElMessage.warning('请输入配置名称')
    return
  }

    // 调试：打印当前参数状态
    console.log('当前所有参数:', {
    lengthStrengthParams: lengthStrengthParams.value,
    micronaireParams: micronaireParams.value,
    handMachineLengthParams: handMachineLengthParams.value,
    processingQualityParams: processingQualityParams.value,
    originParams: originParams.value,
    fiberQualityParams: fiberQualityParams.value,
    rejectionCriteria: rejectionCriteria.value,
    policyParams: policyParams.value
  })

  const configData = {
    name: newConfigName.value,
    length_strength_params: lengthStrengthParams.value,
    micronaire_params: micronaireParams.value,
    hand_machine_length_params: handMachineLengthParams.value,
    processing_quality_params: processingQualityParams.value,
    origin_params: originParams.value,
    fiber_quality_params: fiberQualityParams.value,
    rejection_criteria: rejectionCriteria.value,
    policy_params: policyParams.value
  }

  console.log('准备发送的数据:', configData) // 调试用
  

  // const configData = {
  //   name: newConfigName.value,
  //   ...Object.fromEntries(
  //     Object.entries(allParams.value).map(([key, value]) => [key, value.value])
  //   )
  // }
  
  try {
    const response = await axios.post(`${ apiUrl }/calculate/configs/`, configData)
    ElMessage.success('配置保存成功')
    newConfigName.value = ''
    loadConfigList() // 刷新配置列表
  } catch (error) {
    ElMessage.error('保存配置失败')
    console.error(error)
  }
}

// 初始化加载配置列表
onMounted(() => {
  loadConfigList()
})


// 上传配置
const uploadUrl = computed(() => `${apiUrl}/calculate/certificates/upload/`)
const uploadParams = ref({
  source: 'web_upload'
})

// 状态映射
const statusMap = {
  pending: { text: '待处理', type: 'warning' },
  processing: { text: '计算中', type: '' },
  success: { text: '已完成', type: 'success' },
  failed: { text: '失败', type: 'danger' }
}

// 数据列表
const loading = ref(false)

// 文件验证
const validateFile = (file) => {
  const isExcel = ['application/vnd.ms-excel', 
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
                 .includes(file.type)
  const isUnder10M = file.size / 1024 / 1024 < 10

  if (!isExcel) {
    ElMessage.error('仅支持Excel文件格式')
    return false
  }
  if (!isUnder10M) {
    ElMessage.error('文件大小不能超过10MB')
    return false
  }
  return true
}

// 上传成功处理
const handleSuccess = (response) => {
  if (response.code === 200) {
    ElMessage.success('证书上传成功')
    fetchCertificates()
  } else {
    ElMessage.error(response.message || '上传处理失败')
  }
}

// 错误处理
const handleError = (err) => {
  console.error('上传错误:', err)
  ElMessage.error('文件上传失败，请检查网络或联系管理员')
}

// 获取证书列表
const fetchCertificates = async () => {
  try {
    loading.value = true
    const res = await axios.get(`${apiUrl}/calculate/certificates/`)
    certificateList.value = res.data.data
  } catch (error) {
    ElMessage.error('获取证书列表失败')
  } finally {
    loading.value = false
  }
}

// 下载模板
const downloadTemplate = () => {
  window.open(`${import.meta.env.VITE_API_BASE}/templates/cotton_cert.xlsx`)
}

// 预览证书
const previewCertificate = (id) => {
  window.open(`/certificate-preview/${id}`)
}

// 删除证书
const deleteCertificate = async (id) => {
  try {
    await axios.delete(`${ apiUrl }/certificates/${id}/`)
    ElMessage.success('删除成功')
    fetchCertificates()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

// 初始化加载
fetchCertificates()
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

.upload-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cert-uploader {
  padding: 20px;
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
}

.upload-icon {
  font-size: 48px;
  color: var(--el-color-primary);
  margin: 20px 0;
}

.upload-text {
  margin-bottom: 20px;
}

.upload-tips {
  margin-top: 10px;
  display: flex;
  gap: 8px;
  justify-content: center;
}
</style>
