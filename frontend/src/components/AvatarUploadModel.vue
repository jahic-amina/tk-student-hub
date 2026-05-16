<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl p-6 w-96 shadow-xl">

    <div class="flex justify-between items-center mb-6">
        <h2 class="text-lg font-semibold">Uredi profilnu sliku</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">✕</button>
      </div>

    <div class="flex justify-center mb-6">
        <div class="w-32 h-32 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
          <img v-if="preview" :src="preview" class="w-full h-full object-cover" />
          <span v-else class="text-gray-500 text-3xl font-bold">{{ props.initials }}</span>
        </div>
      </div>

    <div class="flex flex-col items-center gap-2 mb-6">
        <button
          @click="triggerFilePicker"
          class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg">Učitaj sliku</button>
        <p class="text-sm text-gray-400">Podrzani formati: JPG, PNG (maks. 5MB)</p>
        <input
          ref="fileInput"
          type="file"
          accept="image/jpeg, image/png"
          class="hidden"
          @change="onFileSelected"
        />
      </div>
       <p v-if="error" class="text-red-500 text-sm text-center mb-4">{{ error }}</p>
      <div class="flex justify-between">
        <button
          @click="$emit('remove')"
          class="border border-gray-300 text-gray-600 px-4 py-2 rounded-lg hover:bg-gray-50">Ukloni sliku</button>
        <button
          @click="onSave"
          :disabled="!selectedFile"
          class="bg-orange-500 text-white px-6 py-2 rounded-lg hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed">Sacuvaj</button>
      </div>
    </div>
  </div>
</template>