const userUrl = {
    register: '/api/users/register',
    login: '/api/users/login',
    info: (id: number) => `/api/users/${id}`,
    credit: (id: number) => `/api/users/${id}/points`,
    add: '/api/admin/users',
    delete: (id: number) => `/api/admin/users/${id}`
}

const bookUrl = {
    search: '/api/books/search',
    getInfo: (id: number) => `/api/books/${id}`,
    reserve: (id: number) => `/api/books/${id}/reserve`,
    updateInfo: (id: number) => `/api/books/${id}`,
    updateStatus: (id: number) => `/api/books/${id}/status`,
    add: '/api/books',
    delete: (id: number) => `/api/books/${id}`
}

const reservationUrl = {
    submit: '/api/reservations',
    getStatus: (rid: number) => `/api/reservations/${rid}`,
    getAllComfirmed: '/api/reservations/confirmed',
    getUserReservations: (uid: number) => `/api/reservations/users/${uid}`,
    cancel: (rid: number) => `/api/reservations/${rid}/cancel`,
    modify: (rid: number) => `/api/reservations/${rid}`,
    delete: (rid: number) => `/api/reservations/${rid}`
}

const activityUrl = {
    getAll: '/api/activities',
    getDetail: (aid: number) => `/api/activities/${aid}`,
    add: '/api/activities',
    update: (aid: number) => `/api/activities/${aid}`,
    delete: (aid: number) => `/api/activities/${aid}`
}

const commentUrl = {
    get: (bid: number) => `/api/books/${bid}/reviews`,
    getDetail: (cid: number) => `/api/reviews/${cid}`,
    sendComment: '/api/reviews',
    update: (cid: number) => `/api/reviews/${cid}`,
    delete: (cid: number) => `/api/reviews/${cid}`
}

export { userUrl, bookUrl, reservationUrl, activityUrl, commentUrl };