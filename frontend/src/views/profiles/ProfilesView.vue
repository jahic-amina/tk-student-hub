<template>
  <div>

    <div v-if="loading"> Učitavanje...</div>

    <div v-else-if="error"> {{ error }} </div>