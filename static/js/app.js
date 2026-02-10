// Banco de dados em memória (simulando SQLite)
const DB = {
    usuarios: [],
    cursos: [],
    atividades: [],
    progresso: []
};

// Utilitários
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Navegação entre telas
function showScreen(screenId) {
    $$('.screen').forEach(screen => screen.classList.remove('active'));
    $(`#${screenId}`).classList.add('active');
}

// Toast notifications
function showToast(message, type = 'success') {
    const container = $('#toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'check-circle',
        error: 'times-circle',
        warning: 'exclamation-circle'
    };
    
    toast.innerHTML = `
        <i class="fas fa-${icons[type]}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Dados iniciais de exemplo
function initSampleData() {
    // Cursos de exemplo
    const cursosPadrao = [
        { id: 1, nome: 'Gestão de Tempo', descricao: 'Aprenda a gerenciar seu tempo eficientemente', professor_id: null },
        { id: 2, nome: 'Comunicação', descricao: 'Técnicas de comunicação interpessoal', professor_id: null },
        { id: 3, nome: 'Lógica de Programação', descricao: 'Fundamentos da programação', professor_id: null }
    ];
    
    // Atividades de exemplo
    const atividadesPadrao = [
        {
            id: 1,
            curso_id: 1,
            tipo: 'multipla_escolha',
            pergunta: 'Qual técnica é mais eficaz para priorizar tarefas?',
            opcoes: 'Fazer tudo ao mesmo tempo|Matriz de Eisenhower|Procrastinar|Evitar prazos',
            resposta_correta: 'Matriz de Eisenhower',
            dica: 'Pense em urgência vs importância.'
        },
        {
            id: 2,
            curso_id: 1,
            tipo: 'verdadeiro_falso',
            pergunta: 'A regra dos 2 minutos diz que se uma tarefa leva menos de 2 minutos, deve ser feita imediatamente.',
            opcoes: '',
            resposta_correta: 'verdadeiro',
            dica: 'David Allen criou esta técnica no GTD.'
        },
        {
            id: 3,
            curso_id: 2,
            tipo: 'multipla_escolha',
            pergunta: 'Qual é a principal barreira na comunicação interpessoal?',
            opcoes: 'Falar alto|Falta de escuta ativa|Usar tecnologia|Ser introvertido',
            resposta_correta: 'Falta de escuta ativa',
            dica: 'Ouvir é diferente de esperar para falar.'
        },
        {
            id: 4,
            curso_id: 3,
            tipo: 'palavra_embaralhada',
            pergunta: 'Desembaralhe: RTUNA (estrutura de repetição)',
            opcoes: '',
            resposta_correta: 'while',
            dica: 'É usada quando não sabemos quantas vezes repetir.'
        }
    ];
    
    // Verifica se já existem dados no localStorage
    const saved = localStorage.getItem('edustars_db');
    if (saved) {
        const data = JSON.parse(saved);
        DB.usuarios = data.usuarios || [];
        DB.cursos = data.cursos || cursosPadrao;
        DB.atividades = data.atividades || atividadesPadrao;
        DB.progresso = data.progresso || [];
    } else {
        DB.cursos = cursosPadrao;
        DB.atividades = atividadesPadrao;
        saveDB();
    }
}

function saveDB() {
    localStorage.setItem('edustars_db', JSON.stringify(DB));
}

// Utilitários de data
function getToday() {
    return new Date().toISOString().split('T')[0];
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('pt-BR');
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initSampleData();
    
    // Verifica se há usuário logado
    const currentUser = localStorage.getItem('edustars_user');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        redirectToDashboard(user);
    }
});

// Logout
function logout() {
    localStorage.removeItem('edustars_user');
    showScreen('login-screen');
    showToast('Você saiu do sistema', 'warning');
}