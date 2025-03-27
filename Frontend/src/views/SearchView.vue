<template>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>棉花仓单批量查询系统</span>
        </div>
      </template>
  
      <div class="toolbar">
        <el-button 
          type="primary" 
          @click="handleQuery"
          :loading="loading"
        >批量查询</el-button>
        <el-button 
          @click="handleDownload"
          :disabled="results.length === 0"
        >导出Excel</el-button>
        <el-button 
          @click="handleClear"
          :disabled="!inputText && results.length === 0"
        >清空</el-button>
      </div>
  
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="10"
        placeholder="请输入仓单号，每行一个（例如：CF2025020500018）"
        resize="none"
        clearable
      />
  
      <el-table
        :data="results"
        style="width: 100%"
        border
        stripe
        height="600px"
        v-loading="loading"
        >
        <!-- 基础信息 -->
        <el-table-column prop="仓单号" label="仓单号" width="160" fixed />
        <el-table-column prop="升贴水" label="升贴水" width="100" />
        <el-table-column prop="交割库" label="交割库" width="150" />
        <el-table-column prop="产地" label="产地" width="120" />
        <el-table-column prop="加工企业" label="加工企业" width="180" />
        <el-table-column prop="组批批号" label="组批批号" width="120" />
        
        <!-- 重量信息 -->
        <el-table-column prop="平均回潮" label="回潮率(%)" width="100" />
        <el-table-column prop="合计公重" label="公重(kg)" width="100" />
        <el-table-column prop="平均含杂" label="含杂率(%)" width="100" />
        
        <!-- 质量指标 -->
        <el-table-column prop="长度平均值" label="长度(mm)" width="100" />
        <el-table-column prop="马克隆值平均值" label="马克隆值" width="100" />
        <el-table-column prop="长度整齐度平均值" label="整齐度(%)" width="100" />
        <el-table-column prop="断裂比强度平均值" label="比强度(cN/tex)" width="120" />
        
        <!-- 颜色级指标 -->
        <el-table-column prop="白棉1级" label="白棉1级(kg)" width="100" />
        <el-table-column prop="白棉2级" label="白棉2级(kg)" width="100" />
        <el-table-column prop="白棉3级" label="白棉3级(kg)" width="100" />
        <el-table-column prop="白棉4级" label="白棉4级(kg)" width="100" />
        <el-table-column prop="白棉5级" label="白棉5级(kg)" width="100" />
        <el-table-column prop="淡点污棉1级" label="淡点污1级(kg)" width="100" />
        <el-table-column prop="淡点污棉2级" label="淡点污2级(kg)" width="100" />
        <el-table-column prop="淡点污棉3级" label="淡点污3级(kg)" width="100" />
        <el-table-column prop="淡黄染棉1级" label="淡黄染1级(kg)" width="100" />
        <el-table-column prop="淡黄染棉2级" label="淡黄染2级(kg)" width="100" />
        <el-table-column prop="淡黄染棉3级" label="淡黄染3级(kg)" width="100" />
        <el-table-column prop="黄染棉1级" label="黄染棉1级(kg)" width="100" />
        <el-table-column prop="黄染棉2级" label="黄染棉2级(kg)" width="100" />
        <el-table-column prop="轧工质量" label="轧工质量" width="100" />
        
        <!-- 状态 -->
        <el-table-column label="状态" width="80" fixed="right">
            <template #default="{ row }">
            <el-tag :type="!row.error ? 'success' : 'danger'" size="small">
                {{ !row.error ? '成功' : '失败' }}
            </el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="error" label="错误信息" width="200" />
        </el-table>
    </el-card>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { ElMessage } from 'element-plus'
  import axios from 'axios'
  import { apiUrl } from '@/config'
  
  // 响应式数据
  const inputText = ref('')
  const results = ref([])
  const loading = ref(false)
  
  // 处理查询
  const handleQuery = async () => {
    if (!inputText.value.trim()) {
      ElMessage.warning('请输入要查询的仓单号')
      return
    }
  
    try {
      loading.value = true
      results.value = []
      
      const codes = getValidCodes()
      if (codes.length === 0) {
        ElMessage.warning('没有有效的仓单号')
        return
      }
  
      const response = await axios.post(`${ apiUrl }/query/`, {
        codes: codes
      })
  
      if (response.data.status === 'success') {
        results.value = response.data.data
        ElMessage.success(`成功查询 ${response.data.count} 条数据`)
      } else {
        ElMessage.error(response.data.error || '查询失败')
      }
    } catch (error) {
      console.error('查询出错:', error)
      ElMessage.error('请求出错: ' + (error.response?.data?.error || error.message))
    } finally {
      loading.value = false
    }
  }


// 处理CSV下载
const handleDownload = () => {
  if (results.value.length === 0) {
    ElMessage.warning('没有可导出的数据')
    return
  }

  try {
    loading.value = true
    
    // 1. 准备表头 - 与表格列顺序一致
    const headers = [
      '仓单号', '升贴水', '交割库', '产地', '加工企业', '组批批号',
      '回潮率(%)', '公重(kg)', '含杂率(%)', 
      '长度(mm)', '马克隆值', '整齐度(%)', '比强度(cN/tex)',
      '白棉1级(kg)', '白棉2级(kg)', '白棉3级(kg)', '白棉4级(kg)', '白棉5级(kg)',
      '淡点污1级(kg)', '淡点污2级(kg)', '淡点污3级(kg)',
      '淡黄染1级(kg)', '淡黄染2级(kg)', '淡黄染3级(kg)',
      '黄染棉1级(kg)', '黄染棉2级(kg)', '轧工质量'
    ]

    // 2. 准备数据行
    const dataRows = results.value.map(item => {
      return [
        `"${item['仓单号']}"`,
        `"${item['升贴水'] || ''}"`,
        `"${item['交割库'] || ''}"`,
        `"${item['产地'] || ''}"`,
        `"${item['加工企业'] || ''}"`,
        `"${item['组批批号'] || ''}"`,
        `"${item['平均回潮'] || ''}"`,
        `"${item['合计公重'] || ''}"`,
        `"${item['平均含杂'] || ''}"`,
        `"${item['长度平均值'] || ''}"`,
        `"${item['马克隆值平均值'] || ''}"`,
        `"${item['长度整齐度平均值'] || ''}"`,
        `"${item['断裂比强度平均值'] || ''}"`,
        `"${item['白棉1级'] || ''}"`,
        `"${item['白棉2级'] || ''}"`,
        `"${item['白棉3级'] || ''}"`,
        `"${item['白棉4级'] || ''}"`,
        `"${item['白棉5级'] || ''}"`,
        `"${item['淡点污棉1级'] || ''}"`,
        `"${item['淡点污棉2级'] || ''}"`,
        `"${item['淡点污棉3级'] || ''}"`,
        `"${item['淡黄染棉1级'] || ''}"`,
        `"${item['淡黄染棉2级'] || ''}"`,
        `"${item['淡黄染棉3级'] || ''}"`,
        `"${item['黄染棉1级'] || ''}"`,
        `"${item['黄染棉2级'] || ''}"`,
        `"${item['轧工质量'] || ''}"`
      ].join(',')
    })

    // 3. 合并CSV内容
    const csvContent = [
      headers.join(','),
      ...dataRows
    ].join('\n')

    // 4. 创建Blob对象
    const blob = new Blob(["\uFEFF" + csvContent], {
      type: 'text/csv;charset=utf-8;'
    })

    // 5. 创建下载链接
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.href = url
    link.download = `棉花仓单数据_${new Date().toISOString().slice(0, 10)}.csv`
    document.body.appendChild(link)
    link.click()

    // 6. 清理
    setTimeout(() => {
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }, 100)

    ElMessage.success('CSV导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
  
  // 清空数据
  const handleClear = () => {
    inputText.value = ''
    results.value = []
  }
  
  // 获取有效的仓单号列表
  const getValidCodes = () => {
    return [...new Set(
      inputText.value
        .split('\n')
        .map(s => s.trim())
        .filter(s => /^CF\d{13}$/.test(s))  // 简单验证仓单号格式
    )]
  }
  </script>
  
  <style scoped>
  .box-card {
    max-width: 98%;
    margin: 20px auto;
  }
  
  .toolbar {
    margin-bottom: 15px;
    display: flex;
    justify-content: flex-start;
    gap: 10px;
  }
  
  .el-textarea {
    margin-top: 10px;
  }
  
  :deep(.el-table .cell) {
    white-space: nowrap;
  }
  
  :deep(.el-table__body-wrapper) {
    overflow-x: auto;
  }
  </style>