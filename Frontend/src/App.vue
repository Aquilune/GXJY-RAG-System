<template>
  <div class="app-container">
    <div class="sidebar">
      <div class="header">
        <h1>期货信息自动化系统</h1>
      </div>
      <el-menu 
        active-text-color="#ffd04b"
        background-color="#2c3e50"
        class="enhanced-menu"
        default-active="2"
        text-color="#ecf0f1"
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
          <span>基差筛选</span>
        </el-menu-item>
        <el-menu-item index="/trend">
          <el-icon><TrendCharts /></el-icon>
          <span>价差趋势</span>
        </el-menu-item>
        <el-menu-item index="/map">
          <el-icon><MapLocation /></el-icon>
          <span>地图指引</span>
        </el-menu-item>
        <el-menu-item index="/search">
          <el-icon><Search /></el-icon>
          <span>仓单查询</span>
        </el-menu-item>
        <el-menu-item index="/calculate">
          <el-icon><Cpu /></el-icon>
          <span>升贴水计算</span>
        </el-menu-item>
        <el-menu-item index="/helper">
          <el-icon><ChatDotRound /></el-icon>
          <span>期货助手</span>
        </el-menu-item>
      </el-menu>
      
      <!-- 底部信息区域 -->
      <div class="sidebar-footer">
        <div class="system-info">
          <el-icon><info-filled /></el-icon>
          <span>v1.0.0</span>
        </div>
      </div>
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
  Cpu,
  DataAnalysis,
  Files,
  Monitor,
  InfoFilled
} from '@element-plus/icons-vue';

const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};

const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style scoped lang="scss">
.app-container {
  display: flex;
  min-height: 100vh;
  position: relative;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 优化后的侧边栏样式 */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
  
  .header {
    text-align: center;
    padding: 20px 16px;
    color: #fff;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    h1 {
      font-size: 18px;
      font-weight: 500;
      margin: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
  
  .enhanced-menu {
    flex: 1;
    overflow-y: auto;
    border-right: none;
    padding: 8px 0;
    
    /* 滚动条样式 */
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-thumb {
      background-color: rgba(255, 255, 255, 0.2);
      border-radius: 3px;
    }
    
    &::-webkit-scrollbar-track {
      background-color: transparent;
    }
    
    :deep(.el-menu-item),
    :deep(.el-sub-menu__title) {
      height: 48px;
      line-height: 48px;
      margin: 4px 8px;
      border-radius: 6px;
      transition: all 0.2s ease;
      
      &:hover {
        background-color: rgba(255, 255, 255, 0.1);
      }
      
      &.is-active {
        background-color: rgba(255, 208, 75, 0.1);
        color: #ffd04b !important;
        font-weight: 500;
      }
      
      .el-icon {
        font-size: 18px;
        margin-right: 12px;
        color: inherit;
      }
    }
    
    :deep(.el-sub-menu) {
      .el-menu-item {
        min-width: auto;
        padding-left: 56px !important;
      }
    }
  }
  
  .sidebar-footer {
    padding: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    
    .system-info {
      display: flex;
      align-items: center;
      color: rgba(255, 255, 255, 0.6);
      font-size: 12px;
      
      .el-icon {
        margin-right: 8px;
        font-size: 14px;
      }
    }
  }
}

/* 内容区域优化 */
.content {
  flex: 1;
  padding: 24px;
  background-color: #f5f7fa;
  margin-left: 240px;
  min-height: 100vh;
  overflow-y: auto;
}
</style>