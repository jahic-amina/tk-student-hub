const BASE_URL = 'http://127.0.0.1:8000';

function getHeaders() {
  const token =
    localStorage.getItem('token') ||
    localStorage.getItem('access_token');

  const headers = {
    'Content-Type': 'application/json'
  };

  if (token) {
    headers.Authorization = 'Bearer ' + token;
  }

  return headers;
}

async function handleResponse(response, defaultErrorMessage) {
  if (response.status === 204) {
    return null;
  }

  if (response.ok) {
    return response.json();
  }

  let message = defaultErrorMessage;

  try {
    const errorData = await response.json();
    message = errorData.detail || defaultErrorMessage;
  } catch {
    message = defaultErrorMessage;
  }

  throw new Error(message);
}

export const forumNotificationService = {
  async getMyNotifications() {
    const response = await fetch(
      BASE_URL + '/forum/notifications/me',
      {
        method: 'GET',
        headers: getHeaders()
      }
    );

    return handleResponse(
      response,
      'Ucitavanje forum obavjestenja nije uspjelo.'
    );
  },

  async markAsRead(notificationId) {
    const response = await fetch(
      BASE_URL +
        '/forum/notifications/' +
        notificationId +
        '/read',
      {
        method: 'PATCH',
        headers: getHeaders()
      }
    );

    return handleResponse(
      response,
      'Oznacavanje forum obavjestenja nije uspjelo.'
    );
  },

  async markAllAsRead() {
    const response = await fetch(
      BASE_URL + '/forum/notifications/read-all',
      {
        method: 'PATCH',
        headers: getHeaders()
      }
    );

    return handleResponse(
      response,
      'Oznacavanje svih forum obavjestenja nije uspjelo.'
    );
  },

  async deleteNotification(notificationId) {
    const response = await fetch(
      BASE_URL +
        '/forum/notifications/' +
        notificationId,
      {
        method: 'DELETE',
        headers: getHeaders()
      }
    );

    return handleResponse(
      response,
      'Brisanje forum obavjestenja nije uspjelo.'
    );
  }
};


