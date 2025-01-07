<template>
	<div class="business-page">
		<div class="business-container">
			<div class="balance-card">
				<div class="balance-header">
					<el-icon class="icon"><Wallet /></el-icon>
					<span class="title">账户余额</span>
				</div>
				<div class="balance-amount">
					<span class="currency">¥</span>
					<span class="amount">{{ balance }}</span>
				</div>
				<div class="account-info">
					<div class="info-item">
						<span class="label">账户类型：</span>
						<span class="value">{{ savingType }}</span>
					</div>
					<div class="info-item">
						<span class="label">卡号：</span>
						<span class="value">{{ cardId }}</span>
					</div>
				</div>
			</div>

			<div class="action-buttons">
				<div class="action-button" @click="router.push('/search/searchDetail')">
					<el-icon class="icon"><Document /></el-icon>
					<span class="text">交易明细</span>
				</div>
				<div class="action-button" @click="router.push('/businessChoices')">
					<el-icon class="icon"><Back /></el-icon>
					<span class="text">返回</span>
				</div>
				<div class="action-button exit" @click="logOut">
					<el-icon class="icon"><SwitchButton /></el-icon>
					<span class="text">退卡</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import useCardStore from "@/store/card.js"
import { Wallet, Document, Back, SwitchButton } from '@element-plus/icons-vue'
import { getBalance } from '@/utils/api'

const router = useRouter()
const cardStore = useCardStore()
const { logout } = cardStore

const balance = ref(0)
const savingType = ref("")
const cardId = ref(localStorage.getItem("cardId"))

onMounted(async () => {
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    const result = await getBalance(userInfo.account_number)
    if (result.success) {
      balance.value = result.balance
      savingType.value = "储蓄卡"  // 由于后端API简化，这里使用固定值
    } else {
      ElMessage.error(result.message || '获取余额失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '获取余额失败')
  }
})

const logOut = () => {
	logout()
	router.push("/")
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

.balance-card {
	background: linear-gradient(135deg, #409EFF 0%, #36a3f7 100%);
	border-radius: 20px;
	padding: 2rem;
	color: white;
	margin-bottom: 2rem;
	box-shadow: 0 8px 32px rgba(64, 158, 255, 0.2);
}

.balance-header {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	margin-bottom: 1.5rem;

	.icon {
		font-size: 1.5rem;
	}

	.title {
		font-size: 1.2rem;
		font-weight: 500;
	}
}

.balance-amount {
	font-size: 2.5rem;
	font-weight: 600;
	margin-bottom: 1.5rem;

	.currency {
		font-size: 2rem;
		margin-right: 0.5rem;
	}
}

.account-info {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;

	.info-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;

		.label {
			opacity: 0.8;
		}

		.value {
			font-weight: 500;
		}
	}
}

.action-buttons {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 1rem;
}

.action-button {
	background: white;
	border-radius: 15px;
	padding: 1.2rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.8rem;
	cursor: pointer;
	transition: all 0.3s ease;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);

	&:hover {
		transform: translateY(-5px);
		box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
	}

	.icon {
		font-size: 1.8rem;
		color: #409EFF;
	}

	.text {
		font-size: 1rem;
		font-weight: 500;
		color: #2c3e50;
	}

	&.exit {
		.icon {
			color: #f56c6c;
		}

		.text {
			color: #f56c6c;
		}

		&:hover {
			background: #fff1f0;
		}
	}
}
</style>
