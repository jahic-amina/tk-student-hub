<script setup>
defineProps({
  comments: { type: Array, required: true }
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
  <div class="mb-6">
    <h2 class="text-lg font-semibold text-slate-700 mb-4">
      {{ comments.length }} {{ comments.length === 1 ? 'Odgovor' : 'Odgovora' }}
    </h2>

    <div class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="bg-white rounded-xl border p-5 flex gap-4 transition-all"
        :class="comment.is_best_answer ? 'border-green-300 bg-green-50/20' : 'border-gray-200 shadow-sm'"
      >
        <div class="flex-1">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2 text-xs text-slate-400">
              <span class="w-5 h-5 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-[8px]">
                {{ getInitials(comment.author?.full_name) }}
              </span>
              <strong class="text-slate-600">{{ comment.author?.full_name || 'Kolega' }}</strong>
              <span>•</span>
              <span>{{ formatDate(comment.created_at) }}</span>
            </div>
            <span v-if="comment.is_best_answer" class="text-[10px] bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold">
              Najbolji odgovor
            </span>
          </div>
          <p class="text-slate-700 leading-relaxed text-sm whitespace-pre-line">{{ comment.content }}</p>
        </div>
      </div>

      <div v-if="comments.length === 0" class="text-center py-8 text-slate-400 bg-white rounded-xl border border-gray-200 shadow-sm">
        Još nema odgovora. Budite prvi!
      </div>
    </div>
  </div>
</template>