<template>
  <div class="all-cards">
    <div style="display: flex;">
      <div>
        <el-card class="data-box-card"  v-loading="loadingChart"
            element-loading-text="Loading..."
            :element-loading-spinner="svg"
            element-loading-svg-view-box="-10, -10, 50, 50">
          <div id="mainChart" style="width: 800px; height: 400px;"></div>
          <div id="volumeChart" style="width: 800px; height: 200px;"></div>
        </el-card>
      </div>
      <div style="width: 200px; margin-left: 10px;">
        <el-card class="filter-box-card">
          <el-form :model="filterForm" label-width="80px" style="margin-left: -25px;">
            <div style="display: flex;">
              <el-form-item label="产区" style="width: 50%;">
                <el-select v-model="filterForm.region" placeholder="请选择产区" multiple>
                  <el-option v-for="region in productionRegions" :key="region.value" :label="region.label" :value="region.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="产地" style="width: 50%;">
                <el-select v-model="filterForm.place" placeholder="请选择产地" multiple>
                  <el-option v-for="place in productionPlaces" :key="place.value" :label="place.label" :value="place.value"></el-option>
                </el-select>
              </el-form-item>
            </div>
            <div style="display: flex;">
              <el-form-item label="类型" style="width: 50%;">
                <el-select v-model="filterForm.type" placeholder="请选择类型" multiple>
                  <el-option v-for="type in productionTypes" :key="type.value" :label="type.label" :value="type.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="仓库" style="width: 50%;">
                <el-select v-model="filterForm.warehouseArea" placeholder="请选择仓库" multiple>
                  <el-option v-for="warehouse in productionWarehousesArea" :key="warehouse.value" :label="warehouse.label" :value="warehouse.value"></el-option>
                </el-select>
              </el-form-item>
            </div>
            <el-form-item label="长度">
              <el-slider
                v-model="filterForm.lengthRange"
                range
                :min="25"
                :max="40"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 35: '35' }"
              ></el-slider>
            </el-form-item>
            <el-form-item label="强力">
              <el-slider
                v-model="filterForm.strengthRange"
                range
                :min="25"
                :max="45"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 35: '35' }"
              ></el-slider>
            </el-form-item>
            <el-form-item label="码值">
              <el-slider
                v-model="filterForm.codeValueRange"
                range
                :min="2.5"
                :max="5.5"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 2.5: '2.5', 3.5: '3.5', 4.0: '4.0', 4.5: '4.5', 5.0: '5.0', 5.5: '5.5'}"
              ></el-slider>
            </el-form-item>
            <el-form-item label="回潮">
              <el-slider
                v-model="filterForm.moistureRange"
                range
                :min="0"
                :max="11"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 8.5: '8.5'}"
              ></el-slider>
            </el-form-item>
            <el-form-item label="含杂">
              <el-slider
                v-model="filterForm.impurityRange"
                range
                :min="0"
                :max="15"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 1: '1', 2: '2', 3: '3', 4: '4'}"
              ></el-slider>
            </el-form-item>
            <el-form-item label="长整">
              <el-slider
                v-model="filterForm.lengthIntegrityRange"
                range
                :min="77"
                :max="90"
                show-input
                input-size="small"
                :step="0.1"
                show-stops
                :marks="{ 80: '80', 81: '81', 82: '82', 83: '83', 84: '84'}"
              ></el-slider>
            </el-form-item>
            <el-form-item label="年份">
              <el-slider
                v-model="filterForm.yearRange"
                range
                :min="yearRange.min"
                :max="yearRange.max"
                show-input
                input-size="small"
                :step="1"
                show-stops
                :marks="{ 2021: '2021', 2024: '2024', 2025: '2025'}"
              ></el-slider>
            </el-form-item>
            <el-form-item label="日期范围" style="margin-top: 40px;">
              <el-date-picker
                v-model="filterForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
              ></el-date-picker>
            </el-form-item>
            <el-form-item>
              <div style="display: flex;">
                <el-button class="filter-button" type="primary" @click="applyFilter">应用筛选</el-button>
                <el-button class="filter-button" type="primary" @click="resetFilter">重置筛选</el-button>
              </div>
              <div style="display: flex; margin-top: 20px;">
                <el-button class="filter-button" type="primary" @click="handleCrawler">手动爬数</el-button>
                <el-button class="filter-button" type="danger" @click="showDeleteDialog = true">删除数据</el-button>
              </div>
              <el-dialog
                  v-model="showDeleteDialog"
                  title="删除数据"
                  width="30%"
                  >
                    <el-form-item label="删除日期">
                      <el-date-picker
                        v-model="deleteDate"
                        type="date"
                        placeholder="选择要删除数据的日期"
                        format="YYYY-MM-DD"
                        value-format="YYYY-MM-DD"
                      ></el-date-picker>
                    </el-form-item>
                  <template #footer>
                    <span class="dialog-footer">
                      <el-button @click="showDeleteDialog = false">取消</el-button>
                      <el-button type="danger" @click="performDelete">确认删除</el-button>
                    </span>
                  </template>
                </el-dialog>
            </el-form-item>
          </el-form>
        </el-card>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import { apiUrl, productionRegions, productionPlaces, productionTypes, productionWarehouses, productionWarehousesArea } from '@/config';
import { ElLoading, ElMessage } from 'element-plus';

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

// 控制删除对话框的显示
const showDeleteDialog = ref(false);
// 用户选择的删除日期
const deleteDate = ref('');

// 定义 filterForm 的类型
interface FilterForm {
  region: string[];
  place: string[];
  type: string[];
  warehouseArea: string[];
  lengthRange: [number, number];
  strengthRange: [number, number];
  codeValueRange: [number, number];
  moistureRange: [number, number];
  impurityRange: [number, number];
  lengthIntegrityRange: [number, number];
  dateRange: [string, string];
  yearRange: [number, number];
}

// 筛选表单数据
const filterForm = ref<FilterForm>({
  region: [],
  place: [],
  type: [],
  warehouseArea: [],
  lengthRange: [0, 100],
  strengthRange: [0, 100],
  codeValueRange: [0, 10],
  moistureRange: [0, 20],
  impurityRange: [0, 15],
  lengthIntegrityRange: [0, 100],
  dateRange: ['', ''],
  yearRange: [2000, 2025] // 默认值，后续会从后端获取
});

// 年份范围
const yearRange = ref<{ min: number, max: number }>({ min: 2021, max: 2025 });
const handleCrawler = () => {
    // 开启加载动画
    const loading = ElLoading.service({
        lock: false, // 设置为 false 表示不遮挡用户操作
        text: '正在运行爬虫...',
        background: 'rgba(0, 0, 0, 0.7)'
    });

    axios.post(`${apiUrl}/crawler/`)
      .then(response => {
            const task_id = response.data.task_id;
            console.log('Task ID:', task_id);
        })
      .catch(error => {
            console.error('Error starting crawl:', error);
        })
      .finally(() => {
        loading.close();
      });
};
    


// 应用筛选
const applyFilter = () => {
  // 构建请求数据
  const requestData = {
    dateMin: filterForm.value.dateRange[0],
    dateMax: filterForm.value.dateRange[1],
    lengthMax: filterForm.value.lengthRange[1],
    lengthMin: filterForm.value.lengthRange[0],
    strengthMax: filterForm.value.strengthRange[1],
    strengthMin: filterForm.value.strengthRange[0],
    code_valueMax: filterForm.value.codeValueRange[1],
    code_valueMin: filterForm.value.codeValueRange[0],
    moisture_regainMax: filterForm.value.moistureRange[1],
    moisture_regainMin: filterForm.value.moistureRange[0],
    impurity_contentMax: filterForm.value.impurityRange[1],
    impurity_contentMin: filterForm.value.impurityRange[0],
    length_uniformityMax: filterForm.value.lengthIntegrityRange[1],
    length_uniformityMin: filterForm.value.lengthIntegrityRange[0],
    region: filterForm.value.region.join(','),
    place: filterForm.value.place.join(','),
    type: filterForm.value.type.join(','),
    warehouse_area: filterForm.value.warehouseArea.join(','),
    yearMin: filterForm.value.yearRange[0],
    yearMax: filterForm.value.yearRange[1],
  };

  // 发送 POST 请求到后端
  fetchAndRenderData(requestData)
  console.log('应用筛选:', requestData);
};

// 执行删除操作
const performDelete = () => {
  if (!deleteDate.value) {
    ElMessage.warning('请选择要删除数据的日期');
    return;
  }
  const loading = ElLoading.service({
        lock: false, // 设置为 false 表示不遮挡用户操作
        text: '正在删除数据...',
        background: 'rgba(0, 0, 0, 0.7)'
    });
  axios.delete(`${apiUrl}/deleteData/${deleteDate.value}/`)
    .then(response => {
      ElMessage.success('数据删除成功');
      showDeleteDialog.value = false;
      // 可以在这里重新获取数据并更新图表
      fetchAndRenderData({
        dateMax: '2099-12-31',
        dateMin: '1900-01-01',
      });
    })
    .catch(error => {
      console.error('Error deleting data:', error);
      ElMessage.error('数据删除失败:' + error);
    })
    .finally(() => {
      loading.close();
    });
};

// 重置筛选
const resetFilter = () => {
  (Object.keys(filterForm.value) as Array<keyof typeof filterForm.value>).forEach(key => {
    switch (key) {
      case 'dateRange':
        filterForm.value[key] = ['', ''];
        break;
      case 'lengthRange':
      case 'strengthRange':
      case 'codeValueRange':
      case 'moistureRange':
      case 'impurityRange':
      case 'lengthIntegrityRange':
      case 'yearRange':
        filterForm.value[key] = [0, 100];
        if (key === 'codeValueRange') {
          filterForm.value[key] = [0, 10];
        }
        if (key === 'moistureRange') {
          filterForm.value[key] = [0, 20];
        }
        if (key === 'impurityRange') {
          filterForm.value[key] = [0, 15];
        }
        if (key === 'yearRange') {
          filterForm.value[key] = [2021, 2025];
        }
        break;
      case 'region':
      case 'place':
      case 'type':
      case 'warehouseArea':
        // 修复：将 string[] 类型的字段重置为空数组 []
        filterForm.value[key] = [];
        break;
      default:
        break;
    }
  });
  applyFilter();
};

// 获取数据并更新图表
const fetchAndRenderData = (requestData: any) => {
  loadingChart.value = true; 
  axios.post(`${apiUrl}/comparison/`, requestData)
    .then(response => {
      const data = response.data.chart_data;

      // 初始化主图表 ECharts 实例
      const mainChart = echarts.init(document.getElementById('mainChart'));
      // 初始化数据量图表 ECharts 实例
      const volumeChart = echarts.init(document.getElementById('volumeChart'));

      // 提取日期、中位数、25% 分位数和 75% 分位数数据
      const dates = data.map((item: { date: any; }) => item.date);
      const medians = data.map((item: { median: any; }) => item.median);
      const max = data.map((item: { max: any; }) => item.max);
      const min = data.map((item: { min: any; }) => item.min);
      const q25s = data.map((item: { q25: any; }) => item.q25);
      const q75s = data.map((item: { q75: any; }) => item.q75);
      const volume = data.map((item: { volume: any; }) => item.volume);
      const totalWeight = data.map((item: { total_weight: any; }) => item.total_weight);

      // 配置主图表选项
      const mainOption = {
        title: {
          text: '出库基差中位数与分位数区间',
          left: 'center'
        },
        legend: {
          data: ['中位数', '分位数区间'],
          top: 35,
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisPointer: {
            type: 'shadow'
          }
        },
        yAxis: {
          type: 'value',
          name: '数值'
        },
        series: [
          {
            name: '中位数',
            data: medians,
            type: 'line',
            itemStyle: {
              color: 'red'
            },
            label: {
              show: true,
              position: 'top'
            }
          },
          {
            name: '分位数区间',
            type: 'candlestick',
            data: dates.map((_: any, index: string | number) => [q25s[index], q75s[index], min[index], max[index]]),
            itemStyle: {
              color: 'blue',
              color0: 'green', // 当收盘价低于开盘价时的颜色
              borderColor: 'blue',
              borderColor0: 'green'
            },
            label: {
              show: false // 烛台图一般不显示标签
            }
          }
        ]
      };

      // 配置数据量图表选项
      const volumeOption = {
        legend: {
          data: ['数据量', '总重量'],
          position: 'top'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: dates,
          axisPointer: {
            type: 'shadow'
          }
        },
        yAxis: 
        {
      type: 'value',
      name: '总重量',
      position: 'left',
      axisLine: {
        show: true,
      },
      axisLabel: {
        formatter: '{value}'
      }
    },
        series: [
          {
            name: '总重量',
            type: 'bar',
            data: totalWeight,
            itemStyle: {
              color: 'orange'
            }
          }
        ]
      };

      // 使用配置项显示主图表
      mainChart.setOption(mainOption);
      // 使用配置项显示数据量图表
      volumeChart.setOption(volumeOption);
      ElMessage.success('数据获取成功');
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      ElMessage.error('数据获取失败:' + error);
    })
    .finally(() => {
      loadingChart.value = false;  // 不管成功还是失败，结束后隐藏加载
    });
};

onMounted(() => {

  // 恢复 WebSocket 连接和进度
  const taskId = localStorage.getItem('taskId');
  const storedProgress = localStorage.getItem('crawlProgress');

  if (taskId && storedProgress) {
    const progress = parseInt(storedProgress, 10);
    const socket = new WebSocket(`ws://localhost:8000/ws/progress/${taskId}/`);

    socket.onopen = () => {
      console.log('WebSocket 连接已恢复');
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const progress = data.progress;
      const error = data.error;

      const progressBar = document.getElementById('progress-bar');
      if (progressBar) {
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
      }

      localStorage.setItem('crawlProgress', progress.toString());

      if (progress === 100) {
        socket.close();
        localStorage.removeItem('taskId');
        localStorage.removeItem('crawlProgress');
        alert('数据获取任务已完成');
      } else if (progress === -1) {
        socket.close();
        localStorage.removeItem('taskId');
        localStorage.removeItem('crawlProgress');
        alert(`任务失败: ${error}`);
      }
    };

    socket.onclose = () => {
      console.log('WebSocket 连接已关闭');
    };

    // 初始化进度条
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
      progressBar.textContent = `${progress}%`;
    }
  }
    fetchAndRenderData({
      dateMax: '2099-12-31',
      dateMin: '1900-01-01',
    });
  
});
</script>


<style scoped>
.data-box-card {
  text-align: center;
  width: 110vh;   
  height: 94vh;
}

.filter-box-card {
  overflow-y: scroll;
  text-align: center;
  width: 70vh;
  height: 94vh;
  justify-content: center;
}

.el-card-crawler {
  text-align: center;
  height: 20px; /* 自动调整高度 */
  justify-content: center;
}

.el-slider {
  width: 100%;
}

.filter-button {
  width: 150px;
}

.progress-bar-container {
  width: 100%;
  background-color: #f3f3f3;
  border-radius: 25px;
  overflow: hidden;
}

.progress-bar {
  height: 30px;
  background-color: #4caf50;
  text-align: center;
  line-height: 30px;
  color: white;
  border-radius: 25px;
}
</style>