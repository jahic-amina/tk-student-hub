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
        {{ unreadCount }}
      </span>
    </button>

    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-50 overflow-hidden"
    >
      <div class="p-3 border-b border-gray-100 flex justify-between items-center bg-gray-50">
        <span class="font-semibold text-gray-700 text-sm">Obavještenja</span>
        <button 
          v-if="unreadCount > 0"
          @click="markAllRead" 
          class="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
        >
          Označi sve kao pročitano
        </button>
      </div>

      <div class="max-h-64 overflow-y-auto">
        <div v-if="notifications.length === 0" class="p-4 text-center text-sm text-gray-400">
          Nemate novih obavještenja.
        </div>
        
        <div 
          v-for="notif in notifications" 
          :key="notif.source + '-' + notif.id"
          @click="clickNotification(notif)"
          class="p-3 border-b border-gray-50 hover:bg-gray-50 cursor-pointer transition flex flex-col gap-1"
          :class="{'bg-indigo-50/40 font-medium': !notif.is_read}"
        >
          <p class="text-sm text-gray-800 leading-snug">{{ notif.text }}</p>
          <span class="text-[11px] text-gray-400">{{ formatDate(notif.created_at) }}</span>
        </div>
      </div>

      <div v-if="notifications.length > 0" class="p-2 text-center border-t border-gray-100 bg-gray-50">
        <button @click="clearAll" class="text-xs text-red-500 hover:text-red-700 font-medium">
          Obriši istoriju
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

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length;
});

const fetchNotifications = async () => {
  const results = await Promise.allSettled([
    notificationService.getMyNotifications(),
    forumNotificationService.getMyNotifications()
  ]);

  const generalResult = results[0];
  const forumResult = results[1];

  const generalNotifications =
    generalResult.status === 'fulfilled' &&
    Array.isArray(generalResult.value)
      ? generalResult.value
      : [];

  const forumNotifications =
    forumResult.status === 'fulfilled' &&
    Array.isArray(forumResult.value)
      ? forumResult.value
      : [];

  if (generalResult.status === 'rejected') {
    console.error(
      'Greška pri učitavanju postojećih notifikacija:',
      generalResult.reason
    );
  }

  if (forumResult.status === 'rejected') {
    console.error(
      'Greška pri učitavanju forum notifikacija:',
      forumResult.reason
    );
  }

  notifications.value = [
    ...generalNotifications.map(notification => ({
      ...notification,
      source: 'general'
    })),

    ...forumNotifications.map(notification => ({
      ...notification,
      source: 'forum'
    }))
  ].sort((first, second) => {
    return (
      new Date(second.created_at).getTime() -
      new Date(first.created_at).getTime()
    );
  });
};
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) fetchNotifications();
};

const closeDropdown = () => {
  isOpen.value = false;
};

const markAllRead = async () => {
  const results = await Promise.allSettled([
    notificationService.markAllAsRead(),
    forumNotificationService.markAllAsRead()
  ]);

  results.forEach(result => {
    if (result.status === 'rejected') {
      console.error(result.reason);
    }
  });

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
      await router.push(
        '/forum/tema/' + notif.topic_id
      );
    }
  } catch (error) {
    console.error(
      'Greska pri otvaranju notifikacije:',
      error
    );
  }
};

const clearAll = async () => {
  const confirmed = confirm(
    'Da li sigurno zelite obrisati sva obavjestenja?'
  );

  if (!confirmed) {
    return;
  }

  const forumNotifications =
    notifications.value.filter(
      notification => notification.source === 'forum'
    );

  const requests = [
    notificationService.clearAll(),

    ...forumNotifications.map(notification =>
      forumNotificationService.deleteNotification(
        notification.id
      )
    )
  ];

  const results = await Promise.allSettled(requests);

  results.forEach(result => {
    if (result.status === 'rejected') {
      console.error(result.reason);
    }
  });

  await fetchNotifications();
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  
  let ispravanFormat = dateString;
  
  if (!ispravanFormat.endsWith('Z') && !ispravanFormat.includes('+')) {
    ispravanFormat = ispravanFormat.replace(' ', 'T');
    if (!ispravanFormat.endsWith('Z')) {
      ispravanFormat += 'Z';
    }
  }

  const d = new Date(ispravanFormat);
  
  if (isNaN(d.getTime())) return dateString;
  
  return d.toLocaleString('bs-BA', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false 
  });
};

let interval = null;
onMounted(() => {
  fetchNotifications();
  interval = setInterval(fetchNotifications, 45000);
});

onUnmounted(() => {
  if (interval) clearInterval(interval);
});

const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = function (event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event);
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  }
};
</script>