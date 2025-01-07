<template>
	<div class="business-page">
		<div class="business-container">
			<div class="amount-grid">
				<div class="amount-item" v-for="amount in amounts" :key="amount" @click="getCash(amount)">
					<span class="amount">¥{{ amount }}</span>
				</div>
				<div class="amount-item custom" @click="showCustomInput = true">
					<el-icon class="icon"><Edit /></el-icon>
					<span class="text">自定义金额</span>
				</div>
			</div>

			<div class="info-section">
				<div class="balance-info">
					<el-icon class="icon"><Wallet /></el-icon>
					<span class="label">当前余额：</span>
					<span class="value">¥{{ balance }}</span>
				</div>
				<div class="exit-button" @click="router.push('/businessChoices')">
					<el-icon class="icon"><Back /></el-icon>
					<span class="text">返回</span>
				</div>
			</div>

			<!-- 自定义金额对话框 -->
			<el-dialog v-model="showCustomInput" title="请输入取款金额" width="30%" center>
				<div class="custom-input">
					<el-input-number 
						v-model="customAmount" 
						:min="0" 
						:max="20000"
						:step="100"
						controls-position="right"
						placeholder="请输入金额"
					/>
				</div>
				<template #footer>
					<div class="dialog-footer">
						<el-button @click="showCustomInput = false">取消</el-button>
						<el-button type="primary" @click="handleCustomAmount">
							确认
						</el-button>
					</div>
				</template>
			</el-dialog>

			<!-- 加载动画 -->
			<el-dialog v-model="loading" width="20%" center :show-close="false">
				<div class="loading-content">
					<el-icon class="loading-icon"><Loading /></el-icon>
					<span>正在出钞，请稍候...</span>
				</div>
			</el-dialog>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { ElMessage } from "element-plus"
import { Edit, Wallet, Back, Loading } from '@element-plus/icons-vue'
import { getBalance, withdraw } from '@/utils/api'

const router = useRouter()
const balance = ref(0)
const loading = ref(false)
const showCustomInput = ref(false)
const customAmount = ref(100)

// 预设金额选项
const amounts = [100, 200, 500, 1000, 2000, 5000]

// 获取余额
onMounted(async () => {
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    const result = await getBalance(userInfo.account_number)
    if (result.success) {
      balance.value = result.balance
    } else {
      ElMessage.error(result.message || '获取余额失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '获取余额失败')
  }
})

// 取款
const getCash = async (amount) => {
  if (amount > balance.value) {
    ElMessage.error("余额不足")
    return
  }

  loading.value = true
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    const result = await withdraw(userInfo.account_number, amount)
    
    if (result.success) {
      balance.value = result.new_balance
      ElMessage.success('取款成功')
      showCustomInput.value = false
    } else {
      ElMessage.error(result.message || '取款失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '取款失败')
  } finally {
    loading.value = false
  }
}

// 处理自定义金额
const handleCustomAmount = () => {
  if (!customAmount.value) {
    ElMessage.warning('请输入取款金额')
    return
  }
  if (customAmount.value > 20000) {
    ElMessage.warning('单次取款不能超过20000元')
    return
  }
  getCash(customAmount.value)
}
</script>

<style lang="scss" scoped>
.business-page {
	min-height: 100vh;
	padding: 3.5rem 2rem 2rem;
	display: flex;
	justify-content: center;
	align-items: center;
	background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.business-container {
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	border-radius: 20px;
	padding: 2rem;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
	width: 100%;
	max-width: 800px;
}

.amount-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 1.5rem;
	margin-bottom: 2rem;
}

.amount-item {
	background: white;
	border-radius: 15px;
	padding: 1.5rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	cursor: pointer;
	transition: all 0.3s ease;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);

	&:hover {
		transform: translateY(-5px);
		box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
		background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
	}

	&.custom {
		background: #f0f9ff;

		&:hover {
			background: #e6f4ff;
		}

		.icon {
			font-size: 2rem;
			color: #409EFF;
		}

		.text {
			font-size: 1.1rem;
			font-weight: 500;
			color: #409EFF;
		}
	}

	.amount {
		font-size: 1.5rem;
		font-weight: 600;
		color: #2c3e50;
	}
}

.info-section {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-top: 2rem;
	padding-top: 1.5rem;
	border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.balance-info {
	display: flex;
	align-items: center;
	gap: 0.5rem;

	.icon {
		font-size: 1.5rem;
		color: #67c23a;
	}

	.label {
		font-size: 1.1rem;
		color: #606266;
	}

	.value {
		font-size: 1.3rem;
		font-weight: 600;
		color: #67c23a;
	}
}

.exit-button {
	background: #f4f4f5;
	border-radius: 12px;
	padding: 0.8rem 1.2rem;
	display: flex;
	align-items: center;
	gap: 0.5rem;
	cursor: pointer;
	transition: all 0.3s ease;

	&:hover {
		background: #e9e9eb;
	}

	.icon {
		font-size: 1.2rem;
		color: #606266;
	}

	.text {
		font-size: 1rem;
		font-weight: 500;
		color: #606266;
	}
}

.custom-input {
	display: flex;
	justify-content: center;
	padding: 1rem 0;
}

.dialog-footer {
	display: flex;
	justify-content: center;
	gap: 1rem;
	padding-top: 1rem;
}

.loading-content {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	padding: 1rem;

	.loading-icon {
		font-size: 2rem;
		color: #409EFF;
		animation: rotate 1s linear infinite;
	}
}

@keyframes rotate {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
</style>
