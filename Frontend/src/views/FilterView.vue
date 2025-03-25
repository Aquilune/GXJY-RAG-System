<template>
    <div class="select-filter">
        <el-card>
            <el-form :model="filterForm" label-width="80px" style="margin-left: -25px;">
            <div style="display: flex;">
              <el-form-item label="产区" style="width: 50%;">
                <el-select v-model="filterForm.region" placeholder="请选择产区">
                  <el-option v-for="region in productionRegions" :key="region.value" :label="region.label" :value="region.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="产地" style="width: 50%;">
                <el-select v-model="filterForm.place" placeholder="请选择产地">
                  <el-option v-for="place in productionPlaces" :key="place.value" :label="place.label" :value="place.value"></el-option>
                </el-select>
              </el-form-item>
            </div>
            <div style="display: flex;">
              <el-form-item label="类型" style="width: 50%;">
                <el-select v-model="filterForm.type" placeholder="请选择类型">
                  <el-option v-for="type in productionTypes" :key="type.value" :label="type.label" :value="type.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="仓库" style="width: 50%;">
                <el-select v-model="filterForm.warehouse" placeholder="请选择仓库">
                  <el-option v-for="warehouse in productionWarehouses" :key="warehouse.value" :label="warehouse.label" :value="warehouse.value"></el-option>
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
                :min="2021"
                :max="2025"
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
            </el-form-item>
          </el-form>
        </el-card>
        <el-card style="margin-top: 10px;">
            <el-table :data="tableData" style="width: 100%">
                <el-table-column prop="batch_number" label="批号"></el-table-column>
                <el-table-column prop="production_area" label="产区"></el-table-column>
                <el-table-column prop="production_place" label="产地"></el-table-column>
                <el-table-column prop="type" label="类型"></el-table-column>
                <el-table-column prop="warehouse" label="仓库"></el-table-column>
                <el-table-column prop="length" label="长度"></el-table-column>
                <el-table-column prop="strength" label="强力"></el-table-column>
                <el-table-column prop="code_value" label="码值"></el-table-column>
                <el-table-column prop="moisture_regain" label="回潮"></el-table-column>
                <el-table-column prop="impurity_content" label="含杂"></el-table-column>
                <el-table-column prop="length_uniformity" label="长整"></el-table-column>
                <el-table-column prop="outbound_basis" label="出库基差"></el-table-column>
            </el-table>
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[50, 100, 200]"
                v-model:page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="totalDataCount"
            ></el-pagination>
        </el-card>
    </div>
</template>

<script lang="ts" setup>
import { apiUrl, productionRegions, productionPlaces, productionTypes, productionWarehouses } from '@/config';
import axios from 'axios';
import { onMounted, ref } from 'vue';

// 定义 filterForm 的类型
interface FilterForm {
  region: string;
  place: string;
  type: string;
  warehouse: string;
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
  region: '',
  place: '',
  type: '',
  warehouse: '',
  lengthRange: [0, 100],
  strengthRange: [0, 100],
  codeValueRange: [0, 10],
  moistureRange: [0, 20],
  impurityRange: [0, 15],
  lengthIntegrityRange: [0, 100],
  dateRange: ['', ''],
  yearRange: [2000, 2025] // 默认值，后续会从后端获取
});

// 分页相关状态
const currentPage = ref(1);
const pageSize = ref(50);
const totalDataCount = ref(0);
const tableData = ref([]);
const totalPages = ref();
const applyFilter = () => {
    const requestData = {
        ...filterForm.value,
        page: currentPage.value,
        page_size: pageSize.value
    };
    console.log(requestData)
    axios.post(`${apiUrl}/filter/`, requestData)
        .then(response => {
            tableData.value = response.data.data;
            totalDataCount.value = response.data.pagination.total_count;
            currentPage.value = response.data.pagination.current_page;
            pageSize.value = response.data.pagination.page_size;
            totalPages.value = response.data.pagination.total_pages;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

// 处理每页显示数量变化的方法
const handleSizeChange = (newSize: number) => {
  pageSize.value = newSize;
  currentPage.value = 1;
  
  console.log("页数变化后"+pageSize.value)
  applyFilter();
};

// 处理当前页码变化的方法
const handleCurrentChange = (newPage: number) => {
  currentPage.value = newPage;
  console.log("页数"+pageSize.value)
  applyFilter();
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
      default:
        filterForm.value[key] = '';
    }
  });
  // 重置筛选后可以重新请求原始数据并更新图表
  currentPage.value = 1;
  applyFilter();
};

onMounted(() => {
    applyFilter();
})

</script>

<style scoped>

</style>