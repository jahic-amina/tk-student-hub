<template>
  <div>

    <div v-if="loading"> Učitavanje...</div>

    <div v-else-if="error"> {{ error }} </div>
    
    <div v-else-if="profile">
      <UserProfileCard :profile="profile" />
      <div>
        <h2>O meni</h2>
        <p>{{ profile.biografija || 'Nije unesena biografija.' }}</p>
      </div>