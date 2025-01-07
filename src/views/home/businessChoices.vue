<template>
	<div class="business-page">
		<div class="business-container">
			<div class="business-grid">
				<div class="business-item" @click="router.push('/search')">
					<el-icon class="icon"><Search /></el-icon>
					<span class="text">{{ $t("search") }}</span>
				</div>
				<div class="business-item" @click="router.push('/transfer')">
					<el-icon class="icon"><Money /></el-icon>
					<span class="text">{{ $t("transfer") }}</span>
				</div>
				<div class="business-item" @click="router.push('/withdrawal')">
					<el-icon class="icon"><Wallet /></el-icon>
					<span class="text">{{ $t("withdrawal") }}</span>
				</div>
				<div class="business-item" @click="router.push('/deposit')">
					<el-icon class="icon"><Plus /></el-icon>
					<span class="text">{{ $t("deposit") }}</span>
				</div>
				<div class="business-item" @click="router.push('/changePwd')">
					<el-icon class="icon"><Lock /></el-icon>
					<span class="text">{{ $t("changePwd") }}</span>
				</div>
				<div class="business-item" @click="router.push('/livingpayment')">
					<el-icon class="icon"><Service /></el-icon>
					<span class="text">{{ $t("pay") }}</span>
				</div>
			</div>
			<div class="exit-button" @click="logOut">
				<el-icon class="icon"><SwitchButton /></el-icon>
				<span class="text">{{ $t("exit") }}</span>
			</div>
		</div>
	</div>
</template>

<script setup>
import { useRouter } from "vue-router"
import useCardStore from "@/store/card.js"
import { Search, Money, Wallet, Plus, Lock, Service, SwitchButton } from '@element-plus/icons-vue'

const { logout } = useCardStore()
const router = useRouter()
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

.business-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 1.5rem;
	margin-bottom: 2rem;
}

.business-item {
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

	.icon {
		font-size: 2rem;
		color: #409EFF;
	}

	.text {
		font-size: 1.1rem;
		font-weight: 500;
		color: #2c3e50;
	}
}

.exit-button {
	background: #fff1f0;
	border-radius: 12px;
	padding: 1rem;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 0.5rem;
	cursor: pointer;
	transition: all 0.3s ease;

	&:hover {
		background: #ffccc7;
	}

	.icon {
		font-size: 1.5rem;
		color: #f56c6c;
	}

	.text {
		font-size: 1.1rem;
		font-weight: 500;
		color: #f56c6c;
	}
}
</style>
