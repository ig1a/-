<template>
	<div class="header">
		<div class="header-content">
			<h1 class="title">ATM系统</h1>
			<img src="../../assets/img/yinlian.png" alt="" class="union-pay">
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import dayjs from "dayjs"
import { storeToRefs } from "pinia"
import useCardStore from "@/store/card.js"
const cardStore = useCardStore()

// 卡号
const { cardId } = storeToRefs(cardStore)
</script>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background-color: #F9F5EF;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-content {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  height: 3rem;
}

.title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.union-pay {
  position: absolute;
  right: 1rem;
  height: 2rem;
}
</style>
