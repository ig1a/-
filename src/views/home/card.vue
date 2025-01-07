<template>
	<div class="atm-page">
		<div class="atm-content" v-if="!isPassbook">
			<div class="title">{{ $t("pleasePutCard") }}</div>
			<div class="card-section">
				<div class="card-container">
					<img :src="slotPic" class="slot-image" />
					<div class="card-slot">
						<img :src="cardPic" class="card-image" />
					</div>
				</div>
			</div>
			<div class="button-section">
				<el-button class="atm-button" @click="isPassbook = true">
					{{ $t("passbook") }}
				</el-button>
				<el-button class="atm-button" @click="changeLanguage">
					{{ $t("changeLanguage") }}
				</el-button>
				<el-button class="atm-button confirm-button" @click="router.push('/inputPwd')">
					{{ $t("putCard") }}
				</el-button>
			</div>
		</div>
		<div class="atm-content" v-else>
			<div class="title">{{ $t("pleasePutPassBook") }}</div>
			<div class="card-section">
				<div class="card-container">
					<img :src="slotPic" class="slot-image" />
					<div class="card-slot">
						<img :src="cunzhePic" class="card-image" />
					</div>
				</div>
			</div>
			<div class="button-section">
				<el-button class="atm-button confirm-button" @click="router.push('/inputPwd')">
					{{ $t("putPassBook") }}
				</el-button>
				<el-button class="atm-button cancel-button" @click="isPassbook = false">
					{{ $t("back") }}
				</el-button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { i18n } from "@/utils/i18n"
import { useRouter } from "vue-router"

const router = useRouter()

const slotPic = ref("")
const cardPic = ref("")
const cunzhePic = ref("")

// 存折还是银行卡
const isPassbook = ref(false)
// 切换语言
const changeLanguage = () => {
	i18n.global.locale = i18n.global.locale === "zh-CN" ? "en" : "zh-CN"
}

onMounted(() => {
	slotPic.value = new URL("../../assets/img/slot.png", import.meta.url)
	cardPic.value = new URL("../../assets/img/card.png", import.meta.url)
	cunzhePic.value = new URL("../../assets/img/cunzhe.png", import.meta.url)
})
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
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 600;
  color: #2c3e50;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}

.card-section {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 600px;
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.slot-image {
  width: 70%;
  max-width: 400px;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

.card-slot {
  width: 100%;
  text-align: center;
  height: 250px;
  position: relative;
  overflow: hidden;
}

.card-image {
  width: 50%;
  max-width: 300px;
  position: relative;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
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
