<template>
  <div class="helper-view">
    <el-container style="display: flex; flex-direction: column;">
      <el-aside width="200px" style="position: fixed;">
        <el-menu>
          <el-menu-item index="new-chat" @click="addNewChat">
            <el-icon><Plus /></el-icon>
            <span slot="title">新建聊天</span>
          </el-menu-item>
          <el-scrollbar style="height: 615px;">
            <el-menu-item v-for="(chat, index) in chats" :key="index" :index="index.toString()" @click="handleChatSelect(chat.chat_id)">
              <span slot="title">{{ chat.title }}</span>
            </el-menu-item>
          </el-scrollbar>
        </el-menu>
      </el-aside>

      <el-card v-if="activeChat !== 0" class="el-main" ref="mainHeight">
          <div class="chat-messages" ref="chatMessages">
            <div v-if="currentChat" v-for="(message, index) in currentChat.messages" :key="index" class="message" :class="{'message-user': message.user === 'user', 'message-assistant': message.user === 'assistant'}">
              <div :class="{'message-user-text': message.user === 'user', 'message-assistant-text': message.user === 'assistant'}"><span>{{ message.text }}</span></div>
            </div>
          </div>
      </el-card>
      <el-card v-else class="el-main-new">
        <div class="new-chat-container">
          <h1 class="title">您好，有什么我可以帮到您的吗？</h1>
        </div>
        <el-button type="primary" @click="handleAddFile" style="margin-top: 10px;">上传到知识库</el-button>
        <el-upload
          v-model:file-list="fileList"
          class="upload-demo"
          :auto-upload="false"
          :on-change="handleChange"
        >
          <el-button type="primary">选择文件</el-button>
        </el-upload>
      </el-card>
      <div class="flex-container">
        <el-input class="new-chat-input" type="textarea" v-model="inputMessage" placeholder="请输入消息"></el-input>
        <el-button type="primary" class="new-chat-button" @click="giveASentence">发送</el-button>
      </div>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, nextTick, watch } from 'vue'; // 添加 watch 导入
import { Plus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus'; // 如果使用了 ElMessage，也需要导入
import axios from 'axios';
import { apiUrl } from '@/config';
import router from '@/router';
import type { UploadProps, UploadUserFile } from 'element-plus'




const fileList = ref<UploadUserFile[]>([])
let formData = new FormData();

const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {
  fileList.value.push(uploadFile);
  formData.append('file', uploadFile.raw as File);
  console.log('上传后', formData);
  console.log('上传文件列表', fileList.value);
};

const handleAddFile = async () => {
  console.log('发送前', formData);
  console.log('发送文件列表', fileList.value);
  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件');
    return;
  }
  try {
    const response = await axios.post(`${apiUrl}/add_file/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('文件上传响应:', response.data);
    if (response.data.message === '文件添加成功') {
      ElMessage.success(response.data.message);
      fileList.value = [];
      formData = new FormData(); // 清空 formData
    } else {
      ElMessage.error('文件上传失败');
    }
  } catch (error) {
    console.error('文件上传失败:', error);
    ElMessage.error('文件上传失败');
  }
};


// 定义聊天数据结构
interface Chat {
  chat_id: number;
  title: string;
  messages: Message[];
  created_at: Date;
  updated_at: Date;
}

interface Message {
  user: 'user' | 'assistant';
  text: string;
}

// 聊天列表
const chats = ref<Chat[]>([]);
// 当前激活的聊天索引
const activeChat = ref<number>(0);
// 输入框内容
const inputMessage = ref<string>('');
// 新聊天标题
const newChatTitle = ref<string>('');

// 获取聊天消息容器的引用
const chatMessages = ref<HTMLElement | null>(null);

const mainHeight = ref<HTMLElement | null>(null);

const scrollToBottom = () => {
  if (chatMessages.value) {
    const container = chatMessages.value as HTMLElement; // 确保类型正确
    console.log('滚动到最底部', chatMessages.value.scrollHeight)
    container.scrollTop = 100;
  }
};

// 获取聊天列表
const fetchChatList = async () => {
  try {
    const response = await axios.get(`${apiUrl}/chatslist/`);
    chats.value = response.data.data;
  } catch (error) {
    console.error('请求失败，失败原因：', error);
  }
};

// 添加新聊天
const addNewChat = () => {
  activeChat.value = 0;
};
// 获取当前聊天
const currentChat = ref<Chat|null>();
// 创建聊天
const giveASentence = () => {
  if (inputMessage.value.trim() === '') {
    ElMessage.warning('请输入内容');
    return;
  }
if (activeChat.value === 0) {
    // 创建新聊天
    const newChat: Chat = {
      chat_id: chats.value.length + 1, // 假设 chat_id 是递增的
      title: '新聊天',
      messages: [{ user: 'user', text: inputMessage.value }],
      created_at: new Date(),
      updated_at: new Date(),
    };
    chats.value.push(newChat);
    activeChat.value = chats.value.length - 1; // 切换到新聊天
    currentChat.value = newChat; // 更新当前聊天
    inputMessage.value = ''; // 清空输入框
  } else {
    if (currentChat.value) {
      currentChat.value.messages.push({ user: 'user', text: inputMessage.value });
      inputMessage.value = '';
    }
  }
  // chats.value.push({ title: newChatTitle.value, messages: [] });
  // activeChat.value = (chats.value.length - 1).toString();
  newChatTitle.value = '';
};

// 处理聊天选择
const handleChatSelect = async (index: number) => {
  nextTick(scrollToBottom); 
  console.log('activeChat changed:', index)
  activeChat.value = index;
  currentChat.value = chats.value[index];
  console.log('currentChat:', currentChat.value)
  if (index !== 0) {
    try {
      const response = await axios.post(`${apiUrl}/chatdetial/`, { 'index': index });
      // router.push({ path: '/index', query: { id: index } });
      currentChat.value.messages = response.data.data;
      
    } catch (error) {
      console.error('请求失败，失败原因：', error);
      ElMessage.error('获取聊天内容失败');
    }
  } else {
    currentChat.value = null;
  }
};

// 监听 activeChat 变化
// watch(activeChat, (newIndex) => {
//   if (newIndex !== 0) {
//     currentChat.value = chats.value[parseInt(newIndex, 10)];
//   } else {
//     currentChat.value = null;
//   }
// });

// 发送消息
const sendMessage = () => {
  if (inputMessage.value.trim() === '') {
    ElMessage.warning('请输入消息');
    return;
  }
  if (currentChat.value) {
    currentChat.value.messages.push({ user: 'user', text: inputMessage.value });
    inputMessage.value = '';
    // 模拟助手回复
    setTimeout(() => {
      if (currentChat.value) {
        currentChat.value.messages.push({ user: 'assistant', text: '这是助手的回复' });
        nextTick(() => {
          if (chatMessages.value) {
            chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
          }
        });
      }
    }, 1000);
  }
};

// 挂载后自动创建一个默认聊天
onMounted(() => {
  fetchChatList();
  // addNewChat();
});
</script>

<style scoped>
.upload-demo {
  /* background-color: aqua; */
  /* position: fixed; */
  margin-top: 20px;
  bottom: 4vh;
  left: 4vh;
}

/* .el-upload__tip {
  position: fixed;
  bottom: 0;
  left: 1vh;
  background-color: blue;
  max-width: 20vh;
} */

.helper-view {
  height: 90vh;
}

.el-aside {
  background-color: #f5f7fa;
}

.el-main-new {
  display: flex;
  margin-left: 215px;
  overflow-y: auto; /* 内容超出时显示垂直滚动条 */
  height: 80vh;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.flex-container {
  display: flex;
  align-items: center;
  margin-left: 215px;
  height: 10vh;
  margin-top: 3vh;
}

.new-chat-input {
  font-size: 20px;
  width: 100%;
}

.new-chat-button {
  margin-left: 20px;
  height: 100%;
}


.title {
  font-size: 40px;
  color: black;
}


.chat-input {
  padding: 10px;
  border-top: 1px solid #ebeef5;
  margin-bottom: 10px;
  position: fixed;
}

.el-main {
  display: flex;
  flex-direction: column;
  margin-left: 215px;
  overflow-y: auto; /* 内容超出时显示垂直滚动条 */
  height: 80vh;
  padding: 10px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  border-bottom: 1px solid #ebeef5;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  width: 100%;
}

.message-user {
  align-self: flex-end;
  display: flex;
  justify-content: right;
}

.message-assistant {
  align-self: flex-start;
  display: flex;
  justify-content: left;
}

.message-user-text {
  background-color: #dbf0f3;
  border-radius: 5px;
  padding: 10px;
}

.message-assistant-text {
  background-color: #f0f9eb;
  border-radius: 5px;
  padding: 10px;
}


.new-chat-container h3 {
  margin-bottom: 20px;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>