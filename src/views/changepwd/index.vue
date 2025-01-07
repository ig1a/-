<template>
	<div class="business-page">
		<div class="business-container">
			<div class="password-form">
				<div class="form-header">
					<el-icon class="icon"><Lock /></el-icon>
					<span class="title">修改密码</span>
				</div>

				<div class="form-content">
					<div class="security-tips">
						<el-alert
							type="info"
							:closable="false"
							show-icon
						>
							<template #title>
								<div class="tips-content">
									<p>为了您的账户安全：</p>
									<ul>
										<li>密码长度必须为6位数字</li>
										<li>新密码不能与原密码相同</li>
										<li>请勿使用生日等易猜测的数字</li>
									</ul>
								</div>
							</template>
						</el-alert>
					</div>

					<div class="input-groups">
						<div class="input-group">
							<label class="label">当前密码</label>
							<el-input
								v-model="currentPassword"
								type="password"
								placeholder="请输入当前密码"
								maxlength="6"
								show-password
								:show-word-limit="true"
								class="custom-input"
							>
								<template #prefix>
									<el-icon><Key /></el-icon>
								</template>
							</el-input>
						</div>

						<div class="input-group">
							<label class="label">新密码</label>
							<el-input
								v-model="newPassword"
								type="password"
								placeholder="请输入新密码"
								maxlength="6"
								show-password
								:show-word-limit="true"
								class="custom-input"
							>
								<template #prefix>
									<el-icon><EditPen /></el-icon>
								</template>
							</el-input>
						</div>

						<div class="input-group">
							<label class="label">确认新密码</label>
							<el-input
								v-model="confirmPassword"
								type="password"
								placeholder="请再次输入新密码"
								maxlength="6"
								show-password
								:show-word-limit="true"
								class="custom-input"
							>
								<template #prefix>
									<el-icon><Check /></el-icon>
								</template>
							</el-input>
						</div>
					</div>

					<div class="password-strength" v-if="newPassword">
						<div class="strength-label">密码强度：</div>
						<div class="strength-indicator">
							<div 
								class="strength-bar"
								:class="passwordStrengthClass"
								:style="{ width: passwordStrength + '%' }"
							></div>
						</div>
						<span class="strength-text" :class="passwordStrengthClass">
							{{ passwordStrengthText }}
						</span>
					</div>
				</div>

				<div class="form-actions">
					<div class="action-button confirm" @click="handleChangePassword">
						<el-icon class="icon"><Check /></el-icon>
						<span class="text">确认修改</span>
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
				<span>密码修改中，请稍候...</span>
			</div>
		</el-dialog>
	</div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"
import { ElMessage } from "element-plus"
import { Lock, Key, EditPen, Check, Back, Loading } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)

// 表单数据
const currentPassword = ref("")
const newPassword = ref("")
const confirmPassword = ref("")

// 密码强度计算
const passwordStrength = computed(() => {
	if (!newPassword.value) return 0
	
	let strength = 0
	const pwd = newPassword.value
	
	// 长度检查
	if (pwd.length >= 6) strength += 30
	
	// 数字多样性检查
	const uniqueDigits = new Set(pwd.split('')).size
	strength += uniqueDigits * 10
	
	// 连续数字检查
	let hasConsecutive = false
	for (let i = 0; i < pwd.length - 2; i++) {
		if (
			Number(pwd[i]) + 1 === Number(pwd[i + 1]) && 
			Number(pwd[i + 1]) + 1 === Number(pwd[i + 2])
		) {
			hasConsecutive = true
			break
		}
	}
	if (!hasConsecutive) strength += 20

	return Math.min(strength, 100)
})

const passwordStrengthClass = computed(() => {
	const strength = passwordStrength.value
	if (strength >= 80) return 'strong'
	if (strength >= 50) return 'medium'
	return 'weak'
})

const passwordStrengthText = computed(() => {
	const strength = passwordStrength.value
	if (strength >= 80) return '强'
	if (strength >= 50) return '中'
	return '弱'
})

// 处理密码修改
const handleChangePassword = async () => {
	// 输入验证
	if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
		ElMessage.warning("请填写完整信息")
		return
	}

	if (newPassword.value !== confirmPassword.value) {
		ElMessage.error("两次输入的新密码不一致")
		return
	}

	if (newPassword.value === currentPassword.value) {
		ElMessage.error("新密码不能与当前密码相同")
		return
	}

	if (!/^\d{6}$/.test(newPassword.value)) {
		ElMessage.error("密码必须为6位数字")
		return
	}

	loading.value = true
	try {
		const res = await axios({
			url: "/changePassword",
			method: "post",
			params: {
				cardId: localStorage.getItem("cardId"),
				oldPassword: currentPassword.value,
				newPassword: newPassword.value
			}
		})

		if (res.data.res === "success") {
			ElMessage.success("密码修改成功")
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
		ElMessage.error("密码修改失败，请稍后重试")
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

.password-form {
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

.security-tips {
	.tips-content {
		p {
			margin-bottom: 0.5rem;
			font-weight: 500;
		}

		ul {
			list-style: none;
			margin: 0;
			padding: 0;

			li {
				margin-left: 1rem;
				position: relative;
				
				&:before {
					content: "•";
					position: absolute;
					left: -1rem;
				}
			}
		}
	}
}

.input-groups {
	display: flex;
	flex-direction: column;
	gap: 1.5rem;
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

.password-strength {
	display: flex;
	align-items: center;
	gap: 1rem;
	padding: 0.5rem;

	.strength-label {
		color: #606266;
		white-space: nowrap;
	}

	.strength-indicator {
		flex: 1;
		height: 6px;
		background: #ebeef5;
		border-radius: 3px;
		overflow: hidden;
	}

	.strength-bar {
		height: 100%;
		transition: all 0.3s ease;

		&.weak {
			background: #f56c6c;
		}

		&.medium {
			background: #e6a23c;
		}

		&.strong {
			background: #67c23a;
		}
	}

	.strength-text {
		font-size: 0.9rem;
		font-weight: 500;

		&.weak {
			color: #f56c6c;
		}

		&.medium {
			color: #e6a23c;
		}

		&.strong {
			color: #67c23a;
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

@keyframes rotate {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
</style>
