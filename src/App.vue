<template>
	<Header />
	<router-view />
</template>

<script setup>
import Header from "./components/layout/Header.vue"
</script>

<style>
#app {
  min-height: 100vh;
  background-color: #f5f6fa;
}
</style>
