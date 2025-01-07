<template>
	<div class="atm-page">
		<div class="atm-content">
			<div class="input-section">
				<h2 class="title">请输入您的密码：</h2>
				<div class="input-container">
					<el-input
						v-model="password"
						placeholder="请输入您的密码"
						:prefix-icon="Lock"
						type="password"
						class="password-input"
					/>
					<p class="input-tip">输入密码时，请注意遮挡</p>
				</div>
			</div>
			<div class="button-section">
				<el-button 
					class="atm-button confirm-button"
					@click="handleLogin"
				>
					{{ $t("confirm") }}
				</el-button>
				<el-button 
					class="atm-button cancel-button"
					@click="router.push('/')"
				>
					{{ $t("back") }}
				</el-button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { Lock } from "@element-plus/icons-vue"
import axios from "axios"

import useCardStore from "@/store/card.js"
const { login } = useCardStore()

const router = useRouter()
// 登录
const password = ref("")
const handleLogin = async () => {
	login("6100700240001078666")

	const res = await axios({
		url: "/userLogin",
		params: {
			cardId:"6100700240001078666",
			password: password.value
		},
		method: "post"
	})
	if (res.data.res === "success") {
		ElMessage.success(res.data.meg)
		router.push("/businessChoices")
	} else {
		ElMessage.error(res.data.meg)
	}
	console.log(res.data)
}
</script>

<style lang="scss" scoped>
.atm-page {
  min-height: 100vh;
  padding: 3.5rem 2rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.atm-content {
  position: relative;
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-section {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
  text-align: center;
}

.title {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.password-input {
  :deep(.el-input__wrapper) {
    padding: 0.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    background: #f8fafc;
  }

  :deep(.el-input__inner) {
    height: 48px;
    font-size: 1.25rem;
    color: #2c3e50;
  }

  :deep(.el-input__prefix) {
    font-size: 1.25rem;
    color: #94a3b8;
  }
}

.input-tip {
  color: #64748b;
  font-size: 0.875rem;
  font-style: italic;
}

.button-section {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
}

.atm-button {
  width: 160px;
  height: 56px;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: 12px;
  background-color: #3498db;
  color: white;
  border: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    filter: brightness(1.1);
  }

  &:active {
    transform: translateY(1px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
}

.confirm-button {
  background-color: #2ecc71;
  
  &:hover {
    background-color: #27ae60;
  }
}

.cancel-button {
  background-color: #e74c3c;
  
  &:hover {
    background-color: #c0392b;
  }
}
</style>
