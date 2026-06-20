<template>
  <div class="relative inline-block text-left" v-click-outside="closeDropdown">
    <button 
      @click="toggleDropdown" 
      class="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none rounded-full hover:bg-gray-100 transition"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
      </svg>
      
      <span 
        v-if="unreadCount > 0" 
        class="absolute top-1 right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-500 rounded-full"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-2 w-96 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden"
    >
      <!-- Header -->
      <div class="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50">
        <div class="flex items-center gap-2">
          <span class="font-bold text-gray-800 text-sm">Obavještenja</span>
          <span 
            v-if="unreadCount > 0"
            class="inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-bold leading-none text-white bg-red-500 rounded-full"
          >
            {{ unreadCount }}
          </span>
        </div>
        <button 
          v-if="unreadCount > 0"
          @click="markAllRead" 
          class="text-xs text-indigo-600 hover:text-indigo-800 font-medium transition-colors"
        >
          Označi sve kao pročitano
        </button>
      </div>

      <!-- Filter tabs -->
      <div class="flex border-b border-gray-100 bg-white">
        <button
          @click="activeFilter = 'all'"
          class="flex-1 py-2 text-xs font-semibold transition-colors"
          :class="activeFilter === 'all'
            ? 'text-indigo-600 border-b-2 border-indigo-500'
            : 'text-gray-400 hover:text-gray-600'"
        >
          Sve ({{ notifications.length }})
        </button>
        <button
          @click="activeFilter = 'unread'"
          class="flex-1 py-2 text-xs font-semibold transition-colors"
          :class="activeFilter === 'unread'
            ? 'text-indigo-600 border-b-2 border-indigo-500'
            : 'text-gray-400 hover:text-gray-600'"
        >
          Nepročitane ({{ unreadCount }})
        </button>
      </div>

      <!-- Lista notifikacija -->
      <div class="overflow-y-auto" style="max-height: 420px;">
        <div v-if="visibleNotifications.length === 0" class="p-6 text-center text-sm text-gray-400 flex flex-col items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 text-gray-300">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
          </svg>
          <span>{{ activeFilter === 'unread' ? 'Nema nepročitanih obavještenja.' : 'Nemate obavještenja.' }}</span>
        </div>
        
        <div 
          v-for="notif in displayedNotifications" 
          :key="notif.source + '-' + notif.id"
          @click="clickNotification(notif)"
          class="px-4 py-3 border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition-colors flex gap-3 items-start"
          :class="{ 'bg-indigo-50/50': !notif.is_read }"
        >
          <!-- Indikator nepročitano -->
          <div class="flex-shrink-0 mt-1.5">
            <span
              v-if="!notif.is_read"
              class="block w-2 h-2 rounded-full bg-indigo-500"
            ></span>
            <span v-else class="block w-2 h-2"></span>
          </div>

          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-800 leading-snug" :class="{ 'font-semibold': !notif.is_read }">
              {{ notif.text }}
            </p>
            <div class="flex items-center gap-2 mt-1">
              <span class="text-[11px] text-gray-400">{{ formatDate(notif.created_at) }}</span>
              <span
                v-if="notif.source === 'forum'"
                class="text-[10px] px-1.5 py-0.5 rounded bg-orange-50 text-orange-500 border border-orange-100 font-medium"
              >
                Forum
              </span>
            </div>
          </div>

          <!-- Arrow -->
          <div v-if="notif.source === 'forum' && notif.topic_id" class="flex-shrink-0 mt-1 text-gray-300">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
              <path fill-rule="evenodd" d="M8.22 5.22a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L11.94 10 8.22 6.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>

        <!-- Prikaži više -->
        <div
          v-if="visibleNotifications.length > pageSize && displayedCount < visibleNotifications.length"
          class="p-3 text-center border-b border-gray-100"
        >
          <button
            @click.stop="loadMore"
            class="text-xs text-indigo-600 hover:text-indigo-800 font-semibold transition-colors inline-flex items-center gap-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
              <path fill-rule="evenodd" d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd" />
            </svg>
            Prikaži još ({{ visibleNotifications.length - displayedCount }} preostalih)
          </button>
        </div>
      </div>

      <!-- Footer -->
      <div v-if="notifications.length > 0" class="px-4 py-2.5 flex justify-between items-center border-t border-gray-100 bg-gray-50">
        <span class="text-[11px] text-gray-400">
          Prikazano {{ Math.min(displayedCount, visibleNotifications.length) }} od {{ visibleNotifications.length }}
        </span>
        <button @click="clearAll" class="text-xs text-red-400 hover:text-red-600 font-medium transition-colors">
          Obriši sve
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { notificationService } from '../services/api';
import { forumNotificationService } from '../services/forumNotifications'; 

const router = useRouter();

const isOpen = ref(false);
const notifications = ref([]);
const activeFilter = ref('all');
const pageSize = 8;
const displayedCount = ref(pageSize);

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length);

const visibleNotifications = computed(() => {
  if (activeFilter.value === 'unread') return notifications.value.filter(n => !n.is_read);
  return notifications.value;
});

const displayedNotifications = computed(() =>
  visibleNotifications.value.slice(0, displayedCount.value)
);

function loadMore() {
  displayedCount.value += pageSize;
}

const fetchNotifications = async () => {
  const results = await Promise.allSettled([
    notificationService.getMyNotifications(),
    forumNotificationService.getMyNotifications()
  ]);

  const generalResult = results[0];
  const forumResult = results[1];

  const generalNotifications =
    generalResult.status === 'fulfilled' && Array.isArray(generalResult.value)
      ? generalResult.value : [];

  const forumNotifications =
    forumResult.status === 'fulfilled' && Array.isArray(forumResult.value)
      ? forumResult.value : [];

  if (generalResult.status === 'rejected') console.error('Greška pri učitavanju notifikacija:', generalResult.reason);
  if (forumResult.status === 'rejected') console.error('Greška pri učitavanju forum notifikacija:', forumResult.reason);

  notifications.value = [
    ...generalNotifications.map(n => ({ ...n, source: 'general' })),
    ...forumNotifications.map(n => ({ ...n, source: 'forum' }))
  ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
};

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    displayedCount.value = pageSize;
    activeFilter.value = 'all';
    fetchNotifications();
  }
};

const closeDropdown = () => { isOpen.value = false; };

const markAllRead = async () => {
  const results = await Promise.allSettled([
    notificationService.markAllAsRead(),
    forumNotificationService.markAllAsRead()
  ]);
  results.forEach(r => { if (r.status === 'rejected') console.error(r.reason); });
  await fetchNotifications();
};

const clickNotification = async (notif) => {
  try {
    if (!notif.is_read) {
      if (notif.source === 'forum') {
        await forumNotificationService.markAsRead(notif.id);
      } else {
        await notificationService.markAsRead(notif.id);
      }
      notif.is_read = true;
    }

    isOpen.value = false;

    if (notif.source === 'forum' && notif.topic_id) {
      const hash = notif.comment_id ? '#comment-' + notif.comment_id : '';
      await router.push('/forum/tema/' + notif.topic_id + hash);
    }
  } catch (error) {
    console.error('Greska pri otvaranju notifikacije:', error);
  }
};

const clearAll = async () => {
  const confirmed = confirm('Da li sigurno zelite obrisati sva obavjestenja?');
  if (!confirmed) return;

  const forumNotifications = notifications.value.filter(n => n.source === 'forum');
  const requests = [
    notificationService.clearAll(),
    ...forumNotifications.map(n => forumNotificationService.deleteNotification(n.id))
  ];

  const results = await Promise.allSettled(requests);
  results.forEach(r => { if (r.status === 'rejected') console.error(r.reason); });
  await fetchNotifications();
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  let s = dateString;
  if (!s.endsWith('Z') && !s.includes('+')) {
    s = s.replace(' ', 'T');
    if (!s.endsWith('Z')) s += 'Z';
  }
  const d = new Date(s);
  if (isNaN(d.getTime())) return dateString;

  const now = new Date();
  const diffMin = Math.floor((now - d) / 60000);
  const diffH = Math.floor(diffMin / 60);
  const diffD = Math.floor(diffH / 24);

  if (diffMin < 1) return 'Upravo sada';
  if (diffMin < 60) return `Prije ${diffMin} min`;
  if (diffH < 24) return `Prije ${diffH}h`;
  if (diffD < 7) return `Prije ${diffD}d`;

  return d.toLocaleString('bs-BA', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: false
  });
};

let interval = null;
onMounted(() => {
  fetchNotifications();
  interval = setInterval(fetchNotifications, 45000);
});
onUnmounted(() => { if (interval) clearInterval(interval); });

const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) binding.value(event);
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  }
};
</script>