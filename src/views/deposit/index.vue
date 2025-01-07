<template>
	<div class="business-page">
		<div class="business-container">
			<div class="deposit-form">
				<div class="form-header">
					<el-icon class="icon"><Money /></el-icon>
					<span class="title">存款</span>
				</div>

				<div class="form-content">
					<div class="balance-card">
						<div class="balance-header">当前余额</div>
						<div class="balance-amount">
							<span class="currency">¥</span>
							<span class="number">{{ balance }}</span>
						</div>
					</div>

					<div class="amount-section">
						<div class="section-title">
							<el-icon><Wallet /></el-icon>
							<span>选择存款金额</span>
						</div>
						
						<div class="amount-grid">
							<div 
								v-for="amount in presetAmounts" 
								:key="amount"
								class="amount-item"
								:class="{ active: selectedAmount === amount }"
								@click="selectedAmount = amount"
							>
								<span class="amount-value">¥{{ amount }}</span>
							</div>
							<div 
								class="amount-item custom"
								:class="{ active: isCustomAmount }"
								@click="showCustomAmountInput"
							>
								<span class="amount-value">自定义金额</span>
							</div>
						</div>
					</div>

					<el-dialog
						v-model="customAmountDialog"
						title="输入存款金额"
						width="300px"
						center
					>
						<el-input-number
							v-model="customAmount"
							:min="1"
							:max="50000"
							:step="100"
							controls-position="right"
							placeholder="请输入金额"
							class="custom-input"
						/>
						<template #footer>
							<div class="dialog-footer">
								<el-button @click="cancelCustomAmount">取消</el-button>
								<el-button type="primary" @click="confirmCustomAmount">确定</el-button>
							</div>
						</template>
					</el-dialog>
				</div>

				<div class="form-actions">
					<div class="action-button confirm" @click="handleDeposit">
						<el-icon class="icon"><Check /></el-icon>
						<span class="text">确认存款</span>
					</div>
					<div class="action-button" @click="router.push('/businessChoices')">
						<el-icon class="icon"><Back /></el-icon>
						<span class="text">返回</span>
					</div>
				</div>
			</div>
		</div>

		<!-- 加载动画 -->
		<el-dialog v-model="loading" width="20%" center :show-close="false">
			<div class="loading-content">
				<el-icon class="loading-icon"><Loading /></el-icon>
				<span>存款处理中，请稍候...</span>
			</div>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { ElMessage } from "element-plus"
import { Money, Wallet, Check, Back, Loading } from '@element-plus/icons-vue'
import { getBalance, deposit } from '@/utils/api'

const router = useRouter()
const loading = ref(false)
const balance = ref(0)

// 预设金额选项
const presetAmounts = [100, 200, 500, 1000, 2000, 5000]
const selectedAmount = ref(null)
const customAmount = ref(0)
const customAmountDialog = ref(false)

const isCustomAmount = computed(() => {
	return !presetAmounts.includes(selectedAmount.value) && selectedAmount.value !== null
})

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

// 显示自定义金额输入框
const showCustomAmountInput = () => {
	customAmountDialog.value = true
}

// 取消自定义金额
const cancelCustomAmount = () => {
	customAmountDialog.value = false
	if (!presetAmounts.includes(selectedAmount.value)) {
		selectedAmount.value = null
	}
}

// 确认自定义金额
const confirmCustomAmount = () => {
	if (customAmount.value > 50000) {
		ElMessage.warning("单次存款不能超过50000元")
		return
	}
	selectedAmount.value = customAmount.value
	customAmountDialog.value = false
}

// 处理存款
const handleDeposit = async () => {
  if (!selectedAmount.value && !isCustomAmount.value) {
    ElMessage.warning('请选择或输入存款金额')
    return
  }

  const amount = isCustomAmount.value ? customAmount.value : selectedAmount.value

  if (amount <= 0) {
    ElMessage.warning('请输入有效金额')
    return
  }

  if (amount > 50000) {
    ElMessage.warning('单次存款不能超过50000元')
    return
  }

  loading.value = true
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    const result = await deposit(userInfo.account_number, amount)
    
    if (result.success) {
      balance.value = result.new_balance
      ElMessage.success('存款成功')
      // 重置选择
      selectedAmount.value = null
      customAmount.value = 0
      customAmountDialog.value = false
    } else {
      ElMessage.error(result.message || '存款失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '存款失败')
  } finally {
    loading.value = false
  }
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
	max-width: 600px;
}

.deposit-form {
	.form-header {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 2rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);

		.icon {
			font-size: 1.8rem;
			color: #409EFF;
		}

		.title {
			font-size: 1.5rem;
			font-weight: 600;
			color: #2c3e50;
		}
	}

	.form-content {
		display: flex;
		flex-direction: column;
		gap: 2rem;
		margin-bottom: 2rem;
	}
}

.balance-card {
	background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
	border-radius: 15px;
	padding: 1.5rem;
	color: white;
	text-align: center;

	.balance-header {
		font-size: 1rem;
		opacity: 0.9;
		margin-bottom: 0.5rem;
	}

	.balance-amount {
		font-size: 2rem;
		font-weight: 600;

		.currency {
			font-size: 1.5rem;
			margin-right: 0.3rem;
		}
	}
}

.amount-section {
	.section-title {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 1rem;
		color: #606266;
		font-size: 1.1rem;

		.el-icon {
			color: #409EFF;
		}
	}
}

.amount-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 1rem;
}

.amount-item {
	background: white;
	border: 2px solid #ebeef5;
	border-radius: 12px;
	padding: 1rem;
	text-align: center;
	cursor: pointer;
	transition: all 0.3s ease;

	&:hover {
		transform: translateY(-2px);
		border-color: #409EFF;
	}

	&.active {
		background: #409EFF;
		border-color: #409EFF;
		color: white;
	}

	.amount-value {
		font-size: 1.1rem;
		font-weight: 500;
	}

	&.custom {
		background: #f5f7fa;

		&.active {
			background: #409EFF;
		}
	}
}

.form-actions {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}

.action-button {
	background: white;
	border-radius: 15px;
	padding: 1rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	cursor: pointer;
	transition: all 0.3s ease;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);

	&:hover {
		transform: translateY(-3px);
		box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
	}

	.icon {
		font-size: 1.5rem;
		color: #606266;
	}

	.text {
		font-size: 1rem;
		font-weight: 500;
		color: #606266;
	}

	&.confirm {
		background: #409EFF;

		.icon, .text {
			color: white;
		}

		&:hover {
			background: #66b1ff;
		}
	}
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

.dialog-footer {
	display: flex;
	justify-content: flex-end;
	gap: 1rem;
	margin-top: 1rem;
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
