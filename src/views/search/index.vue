<template>
	<div class="business-page">
		<div class="business-container">
			<div class="title-section">
				<el-icon class="icon"><Search /></el-icon>
				<span class="title">查询服务</span>
			</div>

			<div class="search-options">
				<div class="search-option" @click="router.push('/search/balance')">
					<el-icon class="icon"><Wallet /></el-icon>
					<span class="text">余额查询</span>
					<div class="description">查看您的账户余额和账户信息</div>
				</div>
				<div class="search-option" @click="router.push('/search/detail')">
					<el-icon class="icon"><Document /></el-icon>
					<span class="text">明细查询</span>
					<div class="description">查看您的交易记录和流水明细</div>
				</div>
			</div>

			<div class="action-buttons">
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
import { useRouter } from "vue-router"
import useCardStore from "@/store/card.js"
import { Search, Wallet, Document, Back, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const { logout } = useCardStore()
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
	display: flex;
	flex-direction: column;
	gap: 2rem;
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

.search-options {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1.5rem;
	padding: 1rem;
}

.search-option {
	background: white;
	border-radius: 15px;
	padding: 2rem;
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

	.icon {
		font-size: 2.5rem;
		color: #409EFF;
	}

	.text {
		font-size: 1.2rem;
		font-weight: 500;
		color: #2c3e50;
	}

	.description {
		font-size: 0.9rem;
		color: #606266;
		text-align: center;
	}
}

.action-buttons {
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
</style>
