<template>
  <div class="activity-feed">
    <div v-if="loading" class="flex flex-col gap-4">
      <div
        v-for="n in 3"
        :key="n"
        class="flex items-start gap-3 animate-pulse"
      >
        <div class="w-10 h-10 rounded-full bg-gray-200 shrink-0"></div>
        <div class="flex flex-col gap-2 flex-1">
          <div class="h-3 bg-gray-200 rounded w-1/3"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
          <div class="h-3 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    </div>

    <div v-else class="flex flex-col gap-4">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="flex items-start gap-3"
      >
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
          :class="iconBg(activity.activity_type)"
        >
          <component :is="iconComponent(activity.activity_type)" class="w-5 h-5" :class="iconColor(activity.activity_type)" />
        </div>

        <div class="flex flex-col">
          <span class="text-sm" :class="typeLabel(activity.activity_type).color">
            {{ typeLabel(activity.activity_type).text }}
          </span>
          <span class="font-medium text-gray-900">{{ activity.title }}</span>
          <span class="text-sm text-gray-500">
            {{ activity.subtitle }} · {{ formatRelativeTime(activity.created_at) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>