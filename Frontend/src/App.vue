<template>
  <div class="app-container">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="header">
        <h1>期货信息自动化系统</h1>
      </div>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#545c64"
        class="el-menu-vertical-demo"
        default-active="2"
        text-color="#fff"
        @open="handleOpen"
        @close="handleClose"
        router
      >
        <el-menu-item index="/arbitrage">
          <el-icon><Bell /></el-icon>
          <span>交割套利</span>
        </el-menu-item>
        <el-menu-item index="/filter">
          <el-icon><Filter /></el-icon>
          <span>易棉筛选</span>
        </el-menu-item>
        <el-menu-item index="/trend">
          <el-icon><TrendCharts /></el-icon>
          <span>价差趋势</span>
        </el-menu-item>
        <el-menu-item index="/map">
          <el-icon><MapLocation /></el-icon>
          <span>地图指引</span>
        </el-menu-item>
        <el-menu-item index="/helper">
          <el-icon><ChatDotRound /></el-icon>
          <span>期货助手</span>
        </el-menu-item>
      </el-menu>
    </div>
    <!-- 右侧内容区域 -->
    <div class="content">
      <RouterView />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { RouterView } from 'vue-router';
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue';

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  position: relative;
}

.sidebar {
  width: 200px;
  background-color: #545c64;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  overflow-y: hidden;
}

.header {
  text-align: center;
  padding: 20px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 8px;
  color: #fff;
}

.content {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  margin-left: 200px;
  overflow-y: auto;
}
</style>