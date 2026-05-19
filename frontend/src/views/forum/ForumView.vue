<script setup>
import { computed, onMounted, ref } from "vue";
import {
  getTopics,
  getTopicById,
  incrementTopicView,
} from "../../services/forum";

const topics = ref([]);
const selectedTopic = ref(null);

const search = ref("");
const isLoadingTopics = ref(false);
const isLoadingTopic = ref(false);
const errorMessage = ref("");

const sortedComments = computed(() => {
  if (!selectedTopic.value || !selectedTopic.value.comments) {
    return [];
  }

  return selectedTopic.value.comments;
});

function formatDate(dateValue) {
  if (!dateValue) {
    return "";
  }

  return new Intl.DateTimeFormat("bs-BA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(dateValue));
}

function getInitials(name) {
  if (!name) {
    return "?";
  }

  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function shortenText(text, maxLength = 150) {
  if (!text) {
    return "";
  }

  const cleanText = text.replace(/\s+/g, " ").trim();

  if (cleanText.length <= maxLength) {
    return cleanText;
  }

  return cleanText.slice(0, maxLength).trimEnd() + "...";
}

async function loadTopics() {
  isLoadingTopics.value = true;
  errorMessage.value = "";

  try {
    topics.value = await getTopics({
      search: search.value,
    });
  } catch (error) {
    console.error(error);
    errorMessage.value = "Greška: teme se trenutno ne mogu učitati.";
  } finally {
    isLoadingTopics.value = false;
  }
}

async function openTopic(topicId) {
  isLoadingTopic.value = true;
  errorMessage.value = "";

  try {
    await incrementTopicView(topicId);
    selectedTopic.value = await getTopicById(topicId);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  } catch (error) {
    console.error(error);
    errorMessage.value = "Greška: detalji teme se trenutno ne mogu učitati.";
  } finally {
    isLoadingTopic.value = false;
  }
}

async function backToList() {
  selectedTopic.value = null;
  await loadTopics();

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

async function applySearch() {
  selectedTopic.value = null;
  await loadTopics();
}

onMounted(async () => {
  await loadTopics();
});
</script>

<template>
  <div class="forum-page">
    <div v-if="errorMessage" class="error-box">
      {{ errorMessage }}
    </div>

    <!-- LISTA TEMA -->
    <section v-if="!selectedTopic" class="forum-list-page">
      <div class="forum-header-card">
        <div>
          <p class="eyebrow">Forum</p>
          <h1>Teme na forumu</h1>
          <p>Klikni na temu da otvoriš detaljan prikaz, komentare i statistiku.</p>
        </div>

        <div class="search-box">
          <input
            v-model="search"
            type="text"
            placeholder="Pretraži teme..."
            @keyup.enter="applySearch"
          />

          <button type="button" @click="applySearch">
            Traži
          </button>
        </div>
      </div>

      <div v-if="isLoadingTopics" class="empty-card">
        Učitavanje tema...
      </div>

      <div v-else-if="topics.length === 0" class="empty-card">
        Nema tema za prikaz.
      </div>

      <div v-else class="topics-wrapper">
        <article
          v-for="topic in topics"
          :key="topic.id"
          class="topic-preview-card"
          @click="openTopic(topic.id)"
        >
          <div class="topic-meta-row">
            <span class="category-badge">
              {{ topic.category?.name || "Bez kategorije" }}
            </span>

            <span
              v-for="tag in topic.tags"
              :key="tag"
              class="tag-badge"
            >
              #{{ tag }}
            </span>

            <span
              v-if="topic.has_best_answer"
              class="best-answer-small"
            >
              Ima najbolji odgovor
            </span>
          </div>

          <h2>{{ shortenText(topic.title, 150) }}</h2>

          <p class="topic-summary">
            {{ shortenText(topic.summary, 150) }}
          </p>

          <div class="topic-preview-footer">
            <div class="author-line">
              <span class="avatar">
                {{ getInitials(topic.author?.full_name) }}
              </span>

              <span>{{ topic.author?.full_name || "Nepoznat korisnik" }}</span>
              <span>•</span>
              <span>{{ formatDate(topic.created_at) }}</span>
              <span>•</span>
              <span>{{ topic.comments_count }} odgovora</span>
              <span>•</span>
              <span>{{ topic.views_count }} pregleda</span>
            </div>

            <button
              type="button"
              class="open-button"
              @click.stop="openTopic(topic.id)"
            >
              Otvori temu
            </button>
          </div>
        </article>
      </div>
    </section>

    <!-- DETALJAN PRIKAZ TEME -->
    <section v-else class="thread-page">
      <button type="button" class="back-button" @click="backToList">
        ← Nazad na listu
      </button>

      <div v-if="isLoadingTopic" class="empty-card">
        Učitavanje teme...
      </div>

      <template v-else>
        <article class="thread-card">
          <div class="thread-top-row">
            <div class="vote-column">
              <button type="button" disabled>⌃</button>
              <strong>{{ selectedTopic.stats?.votes_count || 0 }}</strong>
              <button type="button" disabled>⌄</button>
            </div>

            <div class="thread-main-content">
              <div class="topic-meta-row">
                <span class="category-badge">
                  {{ selectedTopic.category?.name || "Bez kategorije" }}
                </span>

                <span
                  v-for="tag in selectedTopic.tags"
                  :key="tag"
                  class="tag-badge"
                >
                  #{{ tag }}
                </span>
              </div>

              <h1>{{ selectedTopic.title }}</h1>

              <div class="thread-author-line">
                <span class="avatar large">
                  {{ getInitials(selectedTopic.author?.full_name) }}
                </span>

                <span>{{ selectedTopic.author?.full_name || "Nepoznat korisnik" }}</span>
                <span>•</span>
                <span>{{ formatDate(selectedTopic.created_at) }}</span>
              </div>

              <p class="thread-content">
                {{ selectedTopic.content }}
              </p>

              <div class="inline-stats">
                <span>
                  <strong>{{ selectedTopic.stats?.comments_count || 0 }}</strong>
                  odgovora
                </span>

                <span>
                  <strong>{{ selectedTopic.views_count }}</strong>
                  pregleda
                </span>

                <span>
                  <strong>{{ selectedTopic.stats?.votes_count || 0 }}</strong>
                  glasova
                </span>

                <span>
                  <strong>{{ selectedTopic.stats?.has_best_answer ? "Da" : "Ne" }}</strong>
                  najbolji odgovor
                </span>
              </div>

              <div class="thread-actions">
                <button type="button" disabled>☆ Dodaj u omiljene</button>
                <button type="button" disabled>⚑ Prijavi</button>
                <button type="button" disabled>↗ Dijeli</button>
              </div>
            </div>
          </div>
        </article>

        <section class="comments-section">
          <h2>
            {{ selectedTopic.stats?.comments_count || 0 }} odgovora
          </h2>

          <div v-if="sortedComments.length === 0" class="empty-card">
            Ova tema trenutno nema komentara.
          </div>

          <template v-else>
            <article
              v-for="comment in sortedComments"
              :key="comment.id"
              class="comment-card"
              :class="{ best: comment.is_best_answer }"
            >
              <div class="vote-column comment-votes">
                <button type="button" disabled>⌃</button>
                <strong>{{ comment.votes_count }}</strong>
                <button type="button" disabled>⌄</button>
              </div>

              <div class="comment-content">
                <div class="comment-header">
                  <div class="comment-author">
                    <span class="avatar">
                      {{ getInitials(comment.author?.full_name) }}
                    </span>

                    <strong>{{ comment.author?.full_name || "Nepoznat korisnik" }}</strong>
                    <span>•</span>
                    <span>{{ formatDate(comment.created_at) }}</span>
                  </div>

                  <span
                    v-if="comment.is_best_answer"
                    class="best-answer-badge"
                  >
                    Najbolji odgovor
                  </span>
                </div>

                <p>{{ comment.content }}</p>

                <div class="comment-actions">
                  <button type="button" disabled>↗ Dijeli</button>
                  <button type="button" disabled>⚑ Prijavi</button>
                </div>
              </div>
            </article>
          </template>
        </section>
      </template>
    </section>
  </div>
</template>

<style scoped>
.forum-page {
  max-width: 1120px;
  margin: 0 auto;
  padding: 48px 20px;
  color: #0f172a;
}

.error-box {
  margin-bottom: 16px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #b91c1c;
  border-radius: 14px;
  padding: 14px 16px;
}

.forum-list-page,
.thread-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.forum-header-card,
.topic-preview-card,
.thread-card,
.comment-card,
.empty-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.forum-header-card {
  padding: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.eyebrow {
  margin: 0 0 6px;
  color: #f97316;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.forum-header-card h1,
.thread-main-content h1 {
  margin: 0;
  font-size: 28px;
  line-height: 1.2;
  color: #020617;
}

.forum-header-card p {
  margin: 8px 0 0;
  color: #64748b;
}

.search-box {
  display: flex;
  gap: 10px;
  min-width: 360px;
}

.search-box input {
  flex: 1;
  min-width: 0;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 11px 13px;
  outline: none;
}

.search-box input:focus {
  border-color: #fb923c;
}

.search-box button,
.open-button {
  border: none;
  background: #f97316;
  color: white;
  border-radius: 12px;
  padding: 11px 16px;
  font-weight: 700;
  cursor: pointer;
}

.search-box button:hover,
.open-button:hover {
  background: #ea580c;
}

.topics-wrapper {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.topic-preview-card {
  padding: 22px;
  cursor: pointer;
  transition: 0.15s ease;
}

.topic-preview-card:hover {
  border-color: #fdba74;
  transform: translateY(-1px);
}

.topic-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.category-badge,
.tag-badge,
.best-answer-small {
  border-radius: 999px;
  padding: 5px 9px;
  font-size: 12px;
  font-weight: 800;
}

.category-badge {
  background: #fff7ed;
  color: #ea580c;
}

.tag-badge {
  background: #eff6ff;
  color: #2563eb;
}

.best-answer-small {
  background: #dcfce7;
  color: #15803d;
}

.topic-preview-card h2 {
  margin: 0;
  font-size: 20px;
  color: #020617;
}

.topic-summary {
  margin: 10px 0 0;
  color: #475569;
  line-height: 1.7;
}

.topic-preview-footer {
  margin-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.author-line,
.thread-author-line {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
  flex-wrap: wrap;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: #e2e8f0;
  color: #64748b;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
}

.avatar.large {
  width: 40px;
  height: 40px;
  font-size: 13px;
}

.back-button {
  width: fit-content;
  border: none;
  background: transparent;
  color: #334155;
  font-weight: 700;
  cursor: pointer;
  padding: 6px 0;
}

.back-button:hover {
  color: #f97316;
}

.thread-card {
  padding: 28px;
}

.thread-top-row {
  display: grid;
  grid-template-columns: 48px 1fr;
  gap: 24px;
}

.vote-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #334155;
}

.vote-column button {
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 24px;
  line-height: 1;
}

.vote-column strong {
  font-size: 18px;
}

.thread-author-line {
  margin-top: 18px;
}

.thread-content {
  margin: 24px 0 0;
  color: #1e293b;
  line-height: 1.9;
  font-size: 17px;
  white-space: pre-line;
}

.inline-stats {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.inline-stats span {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  color: #64748b;
  border-radius: 999px;
  padding: 7px 11px;
  font-size: 13px;
}

.inline-stats strong {
  color: #0f172a;
  margin-right: 4px;
}

.thread-actions {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.thread-actions button,
.comment-actions button {
  border: 1px solid #e5e7eb;
  background: white;
  color: #475569;
  border-radius: 10px;
  padding: 9px 12px;
  font-weight: 600;
}

.comments-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.comments-section h2 {
  margin: 0;
  font-size: 22px;
  color: #020617;
}

.comment-card {
  padding: 20px;
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 18px;
}

.comment-card.best {
  border-color: #86efac;
  background: #f0fdf4;
}

.comment-votes button {
  font-size: 21px;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.comment-author {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  flex-wrap: wrap;
}

.comment-author strong {
  color: #020617;
}

.best-answer-badge {
  background: #16a34a;
  color: white;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 800;
}

.comment-content p {
  margin: 14px 0 0;
  color: #1e293b;
  line-height: 1.8;
  white-space: pre-line;
}

.comment-actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.empty-card {
  padding: 40px;
  text-align: center;
  color: #64748b;
}

@media (max-width: 850px) {
  .forum-header-card {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    min-width: 0;
    flex-direction: column;
  }

  .topic-preview-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .thread-top-row,
  .comment-card {
    grid-template-columns: 1fr;
  }

  .vote-column {
    flex-direction: row;
    justify-content: flex-start;
  }
}
</style>