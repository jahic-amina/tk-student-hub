<script setup>
defineProps({
  topic: { type: Object, required: true }
});

function formatDate(dateValue) {
  if (!dateValue) return "";
  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dateValue));
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map((part) => part[0]).join("").slice(0, 2).toUpperCase();
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6 mb-6">
    <h1 class="text-2xl font-bold text-slate-900 mb-4">{{ topic.title }}</h1>
    
    <div class="flex items-center gap-2 text-xs text-slate-500 mb-4 bg-slate-50 p-2 rounded-lg w-fit">
      <span class="w-6 h-6 rounded-full bg-orange-500 text-white flex items-center justify-center font-bold text-[10px]">
        {{ getInitials(topic.author?.full_name) }}
      </span>
      <span class="font-semibold text-slate-700">{{ topic.author?.full_name || 'Student' }}</span>
      <span>•</span>
      <span>{{ formatDate(topic.created_at) }}</span>
      <span>•</span>
      <span>👁️ {{ topic.views_count || 0 }} pregleda</span>
    </div>

    <p class="text-slate-700 leading-relaxed whitespace-pre-line">{{ topic.content }}</p>
  </div>
</template>