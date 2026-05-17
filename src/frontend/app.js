let currentTab = 'active'; 
let isLoginMode = true;    
let bootstrapModal = null;

const authBlock = document.getElementById('auth-block');
const mainContent = document.getElementById('main-content');
const wishesContainer = document.getElementById('wishes-container');
const btnLogout = document.getElementById('btn-logout');
const pageTitle = document.getElementById('page-title');

document.addEventListener('DOMContentLoaded', () => {
    bootstrapModal = new bootstrap.Modal(document.getElementById('wishModal'));
    
    loadWishes();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('tab-active').addEventListener('click', (e) => { e.preventDefault(); switchTab('active'); });
    document.getElementById('tab-archive').addEventListener('click', (e) => { e.preventDefault(); switchTab('archive'); });

    document.getElementById('toggle-auth-mode').addEventListener('click', (e) => {
        e.preventDefault();
        isLoginMode = !isLoginMode;
        document.getElementById('auth-title').innerText = isLoginMode ? 'Вход в систему' : 'Регистрация';
        document.getElementById('btn-auth-submit').innerText = isLoginMode ? 'Войти' : 'Создать аккаунт';
        e.target.innerText = isLoginMode ? 'Создать аккаунт' : 'Уже есть аккаунт? Войти';
    });

    document.getElementById('auth-form').addEventListener('submit', handleAuth);
    document.getElementById('wish-form').addEventListener('submit', handleSaveWish);
    document.getElementById('btn-logout').addEventListener('click', handleLogout);

    document.getElementById('btn-open-modal').addEventListener('click', () => {
        document.getElementById('wishModalLabel').innerText = 'Новое желание';
        document.getElementById('wish-id').value = '';
        document.getElementById('wish-form').reset();
        bootstrapModal.show();
    });
}

function switchTab(tab) {
    currentTab = tab;
    document.getElementById('tab-active').classList.toggle('active', tab === 'active');
    document.getElementById('tab-archive').classList.toggle('active', tab === 'archive');
    
    if (tab === 'active') {
        pageTitle.innerText = 'Мои желания';
        document.getElementById('btn-open-modal').classList.remove('hidden');
    } else {
        pageTitle.innerText = 'Архив';
        document.getElementById('btn-open-modal').classList.add('hidden');
    }
    loadWishes();
}

async function loadWishes() {
    const isBoughtQuery = currentTab === 'archive';
    try {
        const response = await fetch(`/api/wishes/?is_bought=${isBoughtQuery}`);
        if (response.status === 401) {
            authBlock.classList.remove('hidden');
            mainContent.classList.add('hidden');
            document.getElementById('btn-logout').classList.add('hidden');
            return;
        }
        const wishes = await response.json();
        authBlock.classList.add('hidden');
        mainContent.classList.remove('hidden');
        document.getElementById('btn-logout').classList.remove('hidden');
        renderWishes(wishes);
    } catch (err) {
        console.error("Ошибка сети:", err);
    }
}

function renderWishes(wishes) {
    wishesContainer.innerHTML = '';
    
    if (!wishes || !Array.isArray(wishes) || wishes.length === 0) {
        wishesContainer.innerHTML = `
            <div class="col-12 d-flex flex-column align-items-center justify-content-center text-center w-100" style="min-height: 60vh;">
                <p class="text-muted m-0 tracking-wide fw-semibold fs-5">Список пуст</p>
            </div>`;
        return;
    }

    wishes.forEach(wish => {
        const actionButton = currentTab === 'active' 
            ? `<button class="btn btn-sm btn-custom-secondary w-100 mb-2" onclick="toggleWishStatus(${wish.id}, true)">Выполнить</button>`
            : `<button class="btn btn-sm btn-custom-secondary w-100 mb-2" onclick="toggleWishStatus(${wish.id}, false)">Вернуть в список</button>`;

        const linkButton = wish.link 
            ? `<a href="${wish.link}" target="_blank" class="btn btn-sm btn-outline-secondary w-100 mb-2" style="border-color: #e5e5e5; color: #555;">Ссылка</a>` 
            : '';

        const cardHtml = `
            <div class="col">
                <div class="card h-100 card-wish border-0 shadow-sm">
                    <div class="card-body d-flex flex-column p-4">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h5 class="card-title fw-bold m-0 text-truncate" style="max-width: 70%;">${wish.title}</h5>
                            <span class="badge badge-${wish.priority} px-2 py-1 small fw-normal">${wish.priority}</span>
                        </div>
                        <p class="card-text text-muted small flex-grow-1 text-truncate-3 mb-3">${wish.description || 'Без описания'}</p>
                        <p class="fw-bold mb-4" style="color: #2d3748;">${wish.price ? wish.price.toLocaleString('ru-RU') + ' ₽' : '0 ₽'}</p>
                        
                        <div class="mt-auto">
                            ${linkButton}
                            ${actionButton}
                            <div class="d-flex justify-content-between mt-2 px-1">
                                <button class="btn btn-sm btn-link text-muted p-0 small" style="text-decoration: none;" onclick="openEditModal(${wish.id})">Изменить</button>
                                <button class="btn btn-sm btn-link text-danger p-0 small" style="text-decoration: none;" onclick="deleteWish(${wish.id})">Удалить</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        wishesContainer.insertAdjacentHTML('beforeend', cardHtml);
    });
}

async function openEditModal(id) {
    try {
        const response = await fetch(`/api/wishes/${id}`);
        if (!response.ok) {
            alert('Не удалось загрузить данные желания');
            return;
        }
        const wish = await response.json();

        document.getElementById('wishModalLabel').innerText = 'Редактировать желание';
        document.getElementById('wish-id').value = wish.id; // Прописываем ID
        document.getElementById('wish-title').value = wish.title;
        document.getElementById('wish-link').value = wish.link || '';
        document.getElementById('wish-price').value = wish.price || 0;
        document.getElementById('wish-priority').value = wish.priority;
        document.getElementById('wish-desc').value = wish.description || '';

        bootstrapModal.show();
    } catch (err) {
        console.error(err);
    }
}

async function handleSaveWish(e) {
    e.preventDefault();
    
    const wishId = document.getElementById('wish-id').value;
    
    const payload = {
        title: document.getElementById('wish-title').value,
        link: document.getElementById('wish-link').value || null,
        price: parseFloat(document.getElementById('wish-price').value) || 0,
        priority: document.getElementById('wish-priority').value,
        description: document.getElementById('wish-desc').value || null
    };

    const url = wishId ? `/api/wishes/${wishId}` : '/api/wishes/';
    const method = wishId ? 'PATCH' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            bootstrapModal.hide();
            loadWishes();
        } else {
            alert('Ошибка при сохранении');
        }
    } catch (err) {
        console.error(err);
    }
}

async function handleAuth(e) {
    e.preventDefault();
    const username = document.getElementById('auth-username').value;
    const password = document.getElementById('auth-password').value;
    const endpoint = isLoginMode ? '/api/auth/login' : '/api/auth/register';
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (!response.ok) { alert(data.detail || 'Ошибка'); return; }
        
        if (isLoginMode) { loadWishes(); } 
        else { alert('Регистрация успешна! Войдите в аккаунт.'); isLoginMode = true; switchTab('active'); }
    } catch (err) { alert('Ошибка соединения'); }
}

async function toggleWishStatus(id, newStatus) {
    try {
        await fetch(`/api/wishes/${id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_bought: newStatus })
        });
        loadWishes();
    } catch (err) { console.error(err); }
}

async function deleteWish(id) {
    if (!confirm('Удалить карточку?')) return;
    try {
        const response = await fetch(`/api/wishes/${id}`, { method: 'DELETE' });
        if (response.ok) loadWishes();
    } catch (err) { console.error(err); }
}

async function handleLogout() {
    await fetch('/api/auth/logout', { method: 'POST' });
    location.reload();
}