<!-- za oznake @username u tekstu, da budu linkovi ka profilu -->
<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

const props = defineProps({
  text: {
    type: String,
    default: ''
  }
});

const parts = computed(() => {
  const text = props.text || '';
  const regex = /@([a-zA-Z0-9_.-]+)/g;

  const result = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      result.push({
        type: 'text',
        value: text.slice(lastIndex, match.index)
      });
    }

    result.push({
      type: 'mention',
      value: match[0],
      username: match[1]
    });

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    result.push({
      type: 'text',
      value: text.slice(lastIndex)
    });
  }

  return result;
});
</script>

<template>
  <span>
    <template v-for="(part, index) in parts" :key="index">
      <RouterLink
        v-if="part.type === 'mention'"
        :to="{ name: 'profile-detail', params: { username: part.username } }"
        class="mention-link"
      >
        {{ part.value }}
      </RouterLink>

      <span v-else>
        {{ part.value }}
      </span>
    </template>
  </span>
</template>

<style scoped>
.mention-link {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}

.mention-link:hover {
  text-decoration: underline;
}
</style>