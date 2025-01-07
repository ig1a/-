<template>
	<div class="business-page">
		<div class="business-container">
			<div class="transfer-form">
				<div class="form-header">
					<el-icon class="icon"><Money /></el-icon>
					<span class="title">转账</span>
				</div>

				<div class="form-content">
					<div class="input-group">
						<label class="label">收款账号</label>
						<el-input 
							v-model="cardId" 
							placeholder="请输入收款人账号"
							:maxlength="19"
							class="custom-input"
						>
							<template #prefix>
								<el-icon><CreditCard /></el-icon>
							</template>
						</el-input>
					</div>

					<div class="input-group">
						<label class="label">收款人姓名</label>
						<el-input 
							v-model="name" 
							placeholder="请输入收款人姓名"
							class="custom-input"
						>
							<template #prefix>
								<el-icon><User /></el-icon>
							</template>
						</el-input>
					</div>

					<div class="input-group">
						<label class="label">转账金额</label>
						<el-input-number
							v-model="money"
							:min="0"
							:max="50000"
							:step="100"
							controls-position="right"
							placeholder="请输入转账金额"
							class="custom-input"
						/>
					</div>

					<div class="balance-info">
						<el-icon class="icon"><Wallet /></el-icon>
						<span class="label">当前余额：</span>
						<span class="value">¥{{ balance }}</span>
					</div>
				</div>

				<div class="form-actions">
					<div class="action-button confirm" @click="handleTransfer">
						<el-icon class="icon"><Check /></el-icon>
						<span class="text">确认转账</span>
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
				<span>转账处理中，请稍候...</span>
			</div>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { ElMessage } from "element-plus"
import { Money, CreditCard, User, Wallet, Check, Back, Loading } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const balance = ref(0)

// 表单数据
const cardId = ref("")
const name = ref("")
const money = ref(100)

// 获取余额
onMounted(() => {
	axios({
		url: "/getMoney",
		method: "post",
		params: {
			cardId: localStorage.getItem("cardId")
		}
	}).then((res) => {
		if (res.data.res === "success") {
			balance.value = res.data.object.money
		} else {
			ElMessage.error(res.data.meg)
		}
	})
})

// 处理转账
const handleTransfer = async () => {
	if (!cardId.value || !name.value || !money.value) {
		ElMessage.warning("请填写完整信息")
		return
	}

	if (money.value > balance.value) {
		ElMessage.error("余额不足")
		return
	}

	if (money.value > 50000) {
		ElMessage.warning("单次转账不能超过50000元")
		return
	}

	loading.value = true
	try {
		const res = await axios({
			url: "/transfer",
			method: "post",
			params: {
				cardId: localStorage.getItem("cardId"),
				toCardId: cardId.value,
				toName: name.value,
				money: money.value
			}
		})

		if (res.data.res === "success") {
			ElMessage.success(res.data.meg)
			balance.value = res.data.object
			setTimeout(() => {
				loading.value = false
				router.push("/businessChoices")
			}, 2000)
		} else {
			loading.value = false
			ElMessage.error(res.data.meg)
		}
	} catch (error) {
		loading.value = false
		ElMessage.error("转账失败，请稍后重试")
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

.transfer-form {
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
		gap: 1.5rem;
		margin-bottom: 2rem;
	}

	.input-group {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;

		.label {
			font-size: 1rem;
			color: #606266;
			margin-left: 0.2rem;
		}

		.custom-input {
			width: 100%;

			:deep(.el-input__wrapper) {
				padding: 0.5rem;
				border-radius: 12px;
			}

			:deep(.el-input__prefix) {
				margin-right: 0.5rem;
				color: #909399;
			}
		}
	}
}

.balance-info {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 1rem;
	background: #f0f9eb;
	border-radius: 12px;

	.icon {
		font-size: 1.2rem;
		color: #67c23a;
	}

	.label {
		color: #606266;
	}

	.value {
		font-size: 1.1rem;
		font-weight: 600;
		color: #67c23a;
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

@keyframes rotate {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
</style>
