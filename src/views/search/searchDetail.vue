<template>
	<div class="business-page">
		<div class="business-container">
			<div class="title-section">
				<el-icon class="icon"><Document /></el-icon>
				<span class="title">余额信息</span>
			</div>

			<div class="table-section">
				<el-table 
					:data="balanceDetails" 
					style="width: 100%"
					:default-sort="{ prop: 'transDate', order: 'descending' }" 
					v-loading="loading"
					height="100%"
					class="custom-table"
				>
					<el-table-column prop="transDate" label="交易时间" sortable />
					<el-table-column prop="transType" label="交易类别">
						<template #default="scope">
							<el-tag
								:type="getTagType(scope.row.transType)"
								effect="light"
								round
							>
								{{ scope.row.transType }}
							</el-tag>
						</template>
					</el-table-column>
					<el-table-column prop="transMoney" label="交易金额">
						<template #default="scope">
							<span :class="{ 
								'text-success': isDeposit(scope.row.transType),
								'text-danger': !isDeposit(scope.row.transType)
							}">
								{{ formatMoney(scope.row.transMoney) }}
							</span>
						</template>
					</el-table-column>
					<el-table-column prop="remark" label="转账用户" />
				</el-table>
			</div>

			<div class="action-buttons">
				<div class="action-button" @click="receiptDialogVisible = true">
					<el-icon class="icon"><Printer /></el-icon>
					<span class="text">打印凭条</span>
				</div>
				<div class="action-button" @click="router.back()">
					<el-icon class="icon"><Back /></el-icon>
					<span class="text">{{ $t("back") }}</span>
				</div>
				<div class="action-button exit" @click="logOut">
					<el-icon class="icon"><SwitchButton /></el-icon>
					<span class="text">{{ $t("exit") }}</span>
				</div>
			</div>
		</div>

		<el-dialog 
			v-model="receiptDialogVisible" 
			title="打印凭条" 
			width="400px"
			center
			class="custom-dialog"
		>
			<div class="dialog-content">
				<el-icon class="warning-icon"><Warning /></el-icon>
				<span class="dialog-text">确定要打印凭条吗？</span>
			</div>
			<template #footer>
				<div class="dialog-footer">
					<el-button @click="receiptDialogVisible = false">取消</el-button>
					<el-button type="primary" @click="getReceipt">确认打印</el-button>
				</div>
			</template>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import * as XLSX from "xlsx"
import useCardStore from "@/store/card.js"
import { Document, Printer, Back, SwitchButton, Warning } from '@element-plus/icons-vue'

const router = useRouter()
const balanceDetails = reactive([])
const loading = ref(false)
const receiptDialogVisible = ref(false)

// 获取标签类型
const getTagType = (type) => {
	switch (type) {
		case "存入":
			return "success"
		case "取款":
			return "danger"
		case "转账":
			return "warning"
		case "生活缴费":
			return "info"
		default:
			return "info"
	}
}

// 判断是否为存入
const isDeposit = (type) => {
	return type === "存入"
}

// 格式化金额
const formatMoney = (amount) => {
	return `¥ ${Number(amount).toLocaleString()}`
}

// 打印凭条
const getReceipt = () => {
	const data = balanceDetails.map((row) => ({
		交易时间: row.transDate,
		交易类别: row.transType,
		交易金额: row.transMoney,
		转账用户: row.remark
	}))
	const ws = XLSX.utils.json_to_sheet(data)
	const wb = XLSX.utils.book_new()
	XLSX.utils.book_append_sheet(wb, ws, "Sheet1")

	XLSX.writeFile(wb, "凭条.xlsx")
	receiptDialogVisible.value = false
}

// 退卡
const { logout } = useCardStore()
const logOut = () => {
	logout()
	router.push("/")
}

onMounted(() => {
	loading.value = true
	axios({
		url: "/getUserRecepits",
		method: "post",
		params: {
			cardId: localStorage.getItem("cardId")
		}
	}).then((res) => {
		loading.value = false
		for (let i = 0; i < res.data.length; i++) {
			balanceDetails.push(res.data[i])
			balanceDetails[i].transDate = balanceDetails[i].transDate
				.replace("T", " ")
				.slice(0, 16)
			if (res.data[i].transType === 0) {
				balanceDetails[i].transType = "存入"
				balanceDetails[i].remark = res.data[i].cardId
			} else if (res.data[i].transType === 1) {
				balanceDetails[i].transType = "取款"
				balanceDetails[i].remark = "无"
			} else if (res.data[i].transType === 2) {
				balanceDetails[i].transType = "转账"
			} else {
				balanceDetails[i].transType = "生活缴费"
				balanceDetails[i].remark = "无"
			}
		}
	})
})
</script>

<style lang="scss" scoped>
.business-page {
	position: fixed;
	top: 0;
	left: 0;
	height: 100vh;
	width: 100vw;
	margin: 0;
	padding: 2rem;
	display: flex;
	justify-content: center;
	align-items: center;
	background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
	overflow: hidden;
	box-sizing: border-box;
}

.business-container {
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	border-radius: 20px;
	padding: 2rem;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
	width: 90vw;
	height: 90vh;
	max-width: 1200px;
	display: flex;
	flex-direction: column;
	gap: 2rem;
	box-sizing: border-box;
}

.title-section {
	display: flex;
	align-items: center;
	gap: 1rem;
	padding-bottom: 1rem;
	border-bottom: 1px solid rgba(0, 0, 0, 0.1);

	.icon {
		font-size: 2rem;
		color: #409EFF;
	}

	.title {
		font-size: 1.5rem;
		font-weight: 600;
		color: #2c3e50;
	}
}

.table-section {
	flex: 1;
	background: white;
	border-radius: 15px;
	padding: 1rem;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
	overflow: hidden;
	display: flex;
	flex-direction: column;

	.custom-table {
		flex: 1;
		:deep(.el-table__inner-wrapper) {
			height: 100%;
		}
		
		:deep(.el-table__header) {
			font-weight: 600;
			background-color: #f5f7fa;
		}

		:deep(.el-table__body-wrapper) {
			overflow-y: auto;
			height: calc(100% - 40px); // 减去表头高度
		}

		:deep(.el-table__row) {
			transition: all 0.3s ease;

			&:hover {
				background-color: #f5f7fa;
			}
		}
	}
}

.text-success {
	color: #67c23a;
	font-weight: 500;
}

.text-danger {
	color: #f56c6c;
	font-weight: 500;
}

.action-buttons {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
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

	&.exit {
		background: #fff1f0;

		.icon, .text {
			color: #f56c6c;
		}

		&:hover {
			background: #ffccc7;
		}
	}
}

.custom-dialog {
	:deep(.el-dialog__header) {
		margin-right: 0;
		text-align: center;
		font-size: 1.2rem;
		font-weight: 600;
	}

	.dialog-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;

		.warning-icon {
			font-size: 3rem;
			color: #e6a23c;
		}

		.dialog-text {
			font-size: 1.1rem;
			color: #606266;
		}
	}

	.dialog-footer {
		display: flex;
		justify-content: center;
		gap: 1rem;
	}
}
</style>
