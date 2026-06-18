import { ref, computed, onMounted, onUnmounted } from 'vue';

const BASE_URL = 'http://127.0.0.1:8000';

function getHeaders() {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token');
  const headers = { 'Content-Type': 'application/json' };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
}

async function handleResponse(response, defaultErrorMessage) {
  if (response.ok) {
    return response.json();
  }

  try {
    const errorData = await response.json();
    throw new Error(errorData?.detail || defaultErrorMessage);
  } catch (error) {
    throw new Error(error.message || defaultErrorMessage);
  }
}

export async function toggleTopicLike(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/like`, {
    method: 'POST',
    headers: getHeaders()
  });

  return handleResponse(response, 'Lajkovanje teme nije uspjelo.');
}

// DODATO: Funkcija za dislajk ukoliko ti zatreba
export async function toggleTopicDislike(topicId) {
  const response = await fetch(`${BASE_URL}/forum/topics/${topicId}/dislike`, {
    method: 'POST',
    headers: getHeaders()
  });

  return handleResponse(response, 'Dislajkovanje teme nije uspjelo.');
}

// ISPRAVLJENO: Sada ažurira i lajkove i dislajkove sa tačnim imenima koje Vue komponenta očekuje
export function updateTopicLikeInList(teme, payload) {
  const index = teme.value.findIndex((tema) => tema.id === payload.topicId);

  if (index === -1) return;

  teme.value[index] = {
    ...teme.value[index],
    // Koristimo fallback na trenutne vrijednosti ako payload ne sadrži neki podatak
    likes_count: payload.likesCount !== undefined ? payload.likesCount : teme.value[index].likes_count,
    is_liked: payload.isLiked !== undefined ? payload.isLiked : teme.value[index].is_liked,
    
    dislikes_count: payload.dislikesCount !== undefined ? payload.dislikesCount : teme.value[index].dislikes_count,
    is_disliked: payload.isDisliked !== undefined ? payload.isDisliked : teme.value[index].is_disliked
  };
}

export function useForumLazyLoading({
  teme,
  ukupnoTema,
  trenutnaStranica,
  prikaziPrijave,
  ucitajTeme
}) {
  const isLoadingMore = ref(false);

  const imaJosTema = computed(() => {
    return teme.value.length < ukupnoTema.value;
  });

  const ucitajJosTema = async () => {
    if (isLoadingMore.value) return;
    if (prikaziPrijave.value) return;
    if (!imaJosTema.value) return;

    try {
      isLoadingMore.value = true;
      trenutnaStranica.value += 1;

      await Promise.all([
        ucitajTeme(true),
        new Promise((resolve) => setTimeout(resolve, 600))
      ]);
    } finally {
      isLoadingMore.value = false;
    }
  };

  const handleScroll = () => {
    const skoroDno =
      window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 250;

    if (skoroDno) {
      ucitajJosTema();
    }
  };

  onMounted(() => {
    window.addEventListener('scroll', handleScroll);
  });

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
  });

  return {
    isLoadingMore,
    imaJosTema
  };
}