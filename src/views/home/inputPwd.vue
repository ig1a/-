<template>
	<div class="business-page">
		<div class="business-container">
			<div class="password-form">
				<div class="form-header">
					<el-icon class="icon"><Key /></el-icon>
					<span class="title">请输入密码</span>
				</div>

				<div class="form-content">
					<div class="security-tips">
						<el-alert
							type="warning"
							:closable="false"
							show-icon
						>
							<template #title>
								<div class="tips-content">
									请注意周围环境，确保无人窥视您的密码输入
								</div>
							</template>
						</el-alert>
					</div>

					<div class="password-display">
						<div class="dots-container">
							<div 
								v-for="i in 6" 
								:key="i"
								class="password-dot"
								:class="{ filled: password.length >= i }"
							></div>
						</div>
					</div>

					<div class="numpad">
						<div class="numpad-grid">
							<div 
								v-for="num in shuffledNumbers" 
								:key="num"
								class="numpad-button"
								@click="appendNumber(num)"
								:class="{ disabled: password.length >= 6 }"
							>
								{{ num }}
								<div class="button-highlight"></div>
							</div>
							<div 
								class="numpad-button function"
								@click="clearPassword"
							>
								<el-icon><Delete /></el-icon>
								<span>清除</span>
							</div>
							<div 
								class="numpad-button function"
								@click="backspace"
							>
								<el-icon><Back /></el-icon>
								<span>退格</span>
							</div>
						</div>
					</div>
				</div>

				<div class="form-actions">
					<div class="action-button confirm" @click="handleLogin" :class="{ disabled: password.length !== 6 }">
						<el-icon class="icon"><Check /></el-icon>
						<span class="text">确认</span>
					</div>
					<div class="action-button" @click="router.push('/')">
						<el-icon class="icon"><Close /></el-icon>
						<span class="text">取消</span>
					</div>
				</div>
			</div>
		</div>

		<!-- 加载动画 -->
		<el-dialog v-model="loading" width="20%" center :show-close="false">
			<div class="loading-content">
				<el-icon class="loading-icon"><Loading /></el-icon>
				<span>验证中，请稍候...</span>
			</div>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { ElMessage } from "element-plus"
import { Key, Delete, Back, Check, Close, Loading } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const password = ref("")
const numbers = ref([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

// 随机打乱数字键盘
const shuffledNumbers = computed(() => {
	const shuffled = [...numbers.value]
	for (let i = shuffled.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
	}
	return shuffled
})

// 添加数字
const appendNumber = (num) => {
	if (password.value.length < 6) {
		password.value += num
		if (password.value.length === 6) {
			handleLogin()
		}
	}
}

// 退格
const backspace = () => {
	password.value = password.value.slice(0, -1)
}

// 清除密码
const clearPassword = () => {
	password.value = ""
}

// 处理登录
const handleLogin = async () => {
	if (password.value.length !== 6) {
		ElMessage.warning("请输入6位密码")
		return
	}

	loading.value = true
	try {
		// 测试用密码: 123456
		if (password.value === "123456") {
			ElMessage.success("验证成功")
			setTimeout(() => {
				loading.value = false
				router.push("/businessChoices")
			}, 1000)
			return
		}
		
		const res = await axios({
			url: "/checkPassword",
			method: "post",
			params: {
				cardId: localStorage.getItem("cardId"),
				password: password.value
			}
		})

		if (res.data.res === "success") {
			ElMessage.success("验证成功")
			setTimeout(() => {
				loading.value = false
				router.push("/businessChoices")
			}, 1000)
		} else {
			loading.value = false
			ElMessage.error(res.data.meg)
			clearPassword()
		}
	} catch (error) {
		loading.value = false
		ElMessage.error("验证失败，请稍后重试")
		clearPassword()
	}
}

// 每次进入页面时重新打乱数字键盘
onMounted(() => {
	numbers.value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
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
	box-sizing: border-box;
}

.business-container {
	background: rgba(255, 255, 255, 0.9);
	backdrop-filter: blur(10px);
	border-radius: 20px;
	padding: 2rem;
	box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
	width: 100%;
	max-width: 450px;
	max-height: 90vh;
	overflow-y: auto;
}

.password-form {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
}

.form-header {
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

.form-content {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
}

.security-tips {
	.tips-content {
		font-size: 0.9rem;
	}
}

.password-display {
	background: #f5f7fa;
	border-radius: 10px;
	padding: 1rem;

	.dots-container {
		display: flex;
		justify-content: space-between;
		max-width: 240px;
		margin: 0 auto;
	}
}

.password-dot {
	width: 20px;
	height: 20px;
	border-radius: 50%;
	border: 2px solid #dcdfe6;
	transition: all 0.2s ease;

	&.filled {
		background-color: #409EFF;
		border-color: #409EFF;
	}
}

.numpad {
	margin: 1rem 0;

	.numpad-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem;
		max-width: 360px;
		margin: 0 auto;
	}
}

.numpad-button {
	position: relative;
	background: white;
	border-radius: 10px;
	padding: 1rem;
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 1.2rem;
	font-weight: 500;
	color: #2c3e50;
	cursor: pointer;
	transition: all 0.3s ease;
	border: 1px solid #ebeef5;
	overflow: hidden;

	&:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

		.button-highlight {
			transform: scale(2);
			opacity: 0;
		}
	}

	&.disabled {
		opacity: 0.6;
		cursor: not-allowed;

		&:hover {
			transform: none;
			box-shadow: none;
		}
	}

	&.function {
		font-size: 1rem;
		background: #f5f7fa;

		.el-icon {
			margin-right: 0.5rem;
		}
	}
}

.button-highlight {
	position: absolute;
	top: 50%;
	left: 50%;
	width: 100%;
	height: 100%;
	background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
	transform: translate(-50%, -50%) scale(0);
	opacity: 1;
	transition: all 0.3s ease;
}

.form-actions {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
	margin-top: 1rem;
}

.action-button {
	background: white;
	border-radius: 10px;
	padding: 0.8rem;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0.5rem;
	cursor: pointer;
	transition: all 0.3s ease;
	border: 1px solid #ebeef5;

	&:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.icon {
		font-size: 1.2rem;
		color: #606266;
	}

	.text {
		font-size: 0.9rem;
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

		&.disabled {
			background: #a0cfff;
			cursor: not-allowed;

			&:hover {
				transform: none;
				box-shadow: none;
			}
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
		animation: rotate 2s linear infinite;
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
