<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  attachments: { type: Array, required: true },
  downloadBaseUrl: { type: String, required: true }
});

const textPreviews = ref({});
const previewAttachment = ref(null);
const previewUrl = ref('');

function getDownloadUrl(attachment) {
  return `${props.downloadBaseUrl}/download/${attachment.id}`;
}

function canPreview(attachment) {
  return (
    attachment.mime_type.startsWith('image/') ||
    attachment.mime_type === 'application/pdf'
  );
}

function getFileIcon(mimeType) {
  if (mimeType.startsWith('image/')) return '🖼️';
  if (mimeType === 'application/pdf') return '📄';
  if (mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return '📝';
  if (mimeType === 'text/plain') return '📃';
  return '📁';
}

function getFileTypeLabel(mimeType) {
  if (mimeType.startsWith('image/')) return 'Slika';
  if (mimeType === 'application/pdf') return 'PDF';
  if (mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return 'Word dokument';
  if (mimeType === 'text/plain') return 'Tekstualni fajl';
  return 'Fajl';
}

function openPreview(attachment) {
  if (!canPreview(attachment)) return;
  previewAttachment.value = attachment;
  previewUrl.value = getDownloadUrl(attachment);
}

function closePreview() {
  previewAttachment.value = null;
  previewUrl.value = '';
}

function downloadFile(attachment) {
  const url = getDownloadUrl(attachment);
  const a = document.createElement('a');
  a.href = url;
  a.download = attachment.filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

onMounted(async () => {
  for (const att of props.attachments) {
    if (att.mime_type === 'text/plain') {
      try {
        const res = await fetch(getDownloadUrl(att));
        const text = await res.text();
        textPreviews.value[att.id] = text.slice(0, 200);
      } catch {}
    }
  }
});
</script>

<template>
  <div>
    <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2">📎 Prilozi</p>

    <ul class="flex flex-wrap gap-3 list-none p-0 m-0">
      <li
        v-for="attachment in attachments"
        :key="attachment.id"
        class="flex flex-col bg-slate-50 dark:bg-slate-700 border border-gray-200 dark:border-slate-600 rounded-lg overflow-hidden w-40"
      >
        <!-- Thumbnail area -->
        <div
          class="w-full h-24 flex items-center justify-center overflow-hidden"
          :class="canPreview(attachment) ? 'cursor-pointer' : 'cursor-default'"
          @click="openPreview(attachment)"
        >
          <!-- Slika -->
          <img
            v-if="attachment.mime_type.startsWith('image/')"
            :src="getDownloadUrl(attachment)"
            :alt="attachment.filename"
            class="w-full h-full object-cover"
          />

          <!-- PDF -->
          <div
            v-else-if="attachment.mime_type === 'application/pdf'"
            class="flex flex-col items-center gap-1 select-none"
          >
            <span class="text-4xl">📄</span>
            <span class="text-[10px] font-bold uppercase text-red-400">Klikni za pregled</span>
          </div>

          <!-- TXT mini preview -->
          <div
            v-else-if="attachment.mime_type === 'text/plain'"
            class="w-full h-full overflow-hidden p-1.5 text-left bg-white dark:bg-slate-800"
          >
            <pre class="text-[8px] text-slate-400 leading-tight pointer-events-none whitespace-pre-wrap">{{ textPreviews[attachment.id] || 'Učitavanje...' }}</pre>
          </div>

          <!-- Ostali fajlovi -->
          <div
            v-else
            class="flex flex-col items-center gap-1 text-slate-400 select-none"
          >
            <span class="text-4xl">{{ getFileIcon(attachment.mime_type) }}</span>
            <span class="text-[10px] font-semibold uppercase text-slate-400">{{ getFileTypeLabel(attachment.mime_type) }}</span>
          </div>
        </div>

        <!-- Meta -->
        <div class="px-2 pt-1.5 pb-0.5">
          <p class="text-[11px] font-medium text-slate-700 dark:text-slate-200 truncate" :title="attachment.filename">
            {{ attachment.filename }}
          </p>
          <p class="text-[10px] text-slate-400">{{ (attachment.file_size / 1024).toFixed(1) }} KB</p>
        </div>

        <!-- Akcije -->
        <div class="flex gap-1 px-2 pb-2 mt-0.5">
          <button
            v-if="canPreview(attachment)"
            @click="openPreview(attachment)"
            class="text-[10px] font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40 px-2 py-0.5 rounded border-none cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-950/70 transition-colors"
          >
            Pregledaj
          </button>
          <button
            @click="downloadFile(attachment)"
            class="text-[10px] font-medium text-slate-500 dark:text-slate-300 border border-gray-300 dark:border-slate-500 px-2 py-0.5 rounded bg-transparent cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-600 transition-colors"
          >
            ⬇ Preuzmi
          </button>
        </div>
      </li>
    </ul>

    <!-- Modal -->
    <teleport to="body">
      <div
        v-if="previewAttachment"
        class="fixed inset-0 z-50 bg-black/60 flex items-center justify-center p-4"
        @click.self="closePreview"
      >
        <div
          class="bg-white dark:bg-slate-800 rounded-xl border border-gray-200 dark:border-slate-700 w-full max-w-3xl flex flex-col shadow-2xl"
          style="max-height: 90vh;"
        >
          <!-- Header -->
          <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100 dark:border-slate-700 flex-shrink-0">
            <span class="text-sm font-semibold text-slate-700 dark:text-slate-200 truncate">
              {{ getFileIcon(previewAttachment.mime_type) }} {{ previewAttachment.filename }}
            </span>
            <button
              @click="closePreview"
              class="text-slate-400 hover:text-slate-700 dark:hover:text-white text-2xl leading-none bg-transparent border-none cursor-pointer ml-4 flex-shrink-0"
            >
              &times;
            </button>
          </div>

          <!-- Body -->
          <div
            class="flex-1 overflow-auto flex items-center justify-center bg-slate-100 dark:bg-slate-900"
            style="min-height: 200px;"
          >
            <img
              v-if="previewAttachment.mime_type.startsWith('image/')"
              :src="previewUrl"
              :alt="previewAttachment.filename"
              class="max-w-full object-contain"
              style="max-height: 70vh;"
            />

            <iframe
              v-else-if="previewAttachment.mime_type === 'application/pdf'"
              :src="previewUrl"
              class="w-full border-none"
              style="height: 70vh;"
            />
          </div>

          <!-- Footer -->
          <div class="flex justify-end gap-2 px-4 py-3 border-t border-gray-100 dark:border-slate-700 flex-shrink-0">
            <button
              @click="closePreview"
              class="text-xs text-slate-500 border border-gray-200 dark:border-slate-600 px-3 py-1.5 rounded-lg bg-transparent cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
            >
              Zatvori
            </button>
            <button
              @click="downloadFile(previewAttachment)"
              class="text-xs font-bold text-white bg-orange-500 hover:bg-orange-400 px-3 py-1.5 rounded-lg border-none cursor-pointer transition-colors"
            >
              ⬇ Preuzmi
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>