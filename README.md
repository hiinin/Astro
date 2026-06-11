# Astro — Explorador de Dados da NASA

Plataforma que reúne dados oficiais da NASA em uma interface moderna, consumindo diversas APIs públicas em tempo real.

---

## Pré-requisitos

- **Python 3.10+** instalado
- **Node.js 18+** e **npm** instalados
- Conexão com a internet (para acessar as APIs da NASA)

---

## Instalação

### 1. Backend (Python)

Na raiz do projeto, instale as dependências:

```bash
pip install fastapi
pip install uvicorn
pip install httpx
```

> Essas três bibliotecas são o que o backend precisa para funcionar:
> - `fastapi` — framework web que serve as rotas da API
> - `uvicorn` — servidor ASGI que roda o FastAPI
> - `httpx` — cliente HTTP assíncrono usado para chamar as APIs da NASA

### 2. Frontend (Vue)

Entre na pasta `frontend` e instale as dependências do Node:

```bash
cd frontend
npm install
```

---

## Como Rodar

### 1. Iniciar o Backend

Na **raiz do projeto**, execute:

```bash
python -m uvicorn main:app --port 8002 --reload
```

| Parâmetro | O que faz |
|-----------|-----------|
| `main:app` | Aponta para o objeto `app` dentro do arquivo `main.py` |
| `--port 8002` | Servidor sobe na porta 8002 |
| `--reload` | Reinicia automaticamente ao salvar alterações no código |

O backend estará disponível em: **http://localhost:8002**

### 2. Iniciar o Frontend

Em outro terminal, entre na pasta `frontend` e rode:

```bash
cd frontend
npm run dev
```

O frontend (Vite) vai subir em: **http://localhost:5173** (porta padrão do Vite)

---

## Resumo Rápido

```
Terminal 1 (raiz do projeto):
  python -m uvicorn main:app --port 8002 --reload

Terminal 2 (pasta frontend):
  npm run dev
```

Abra o navegador em **http://localhost:5173** e o projeto estará funcionando.

---

## Estrutura do Projeto

```
Astro/
├── core/              → Backend Python (proxy para APIs da NASA)
│   ├── config.py      → Chave da API e URLs base
│   └── proxy.py       → Cliente HTTP com cache
├── main.py            → Ponto de entrada do FastAPI
├── frontend/          → Aplicação Vue 3
│   ├── src/
│   │   ├── composables/  → Lógica reutilizável (chamadas API, etc.)
│   │   ├── components/   → Componentes de UI
│   │   ├── modules/      → Páginas/views de cada seção
│   │   ├── layouts/      → Layouts (Home e Default)
│   │   └── router/       → Configuração de rotas
│   └── package.json
├── .env               → Variáveis de ambiente
└── README.md          → Este arquivo
```

---

## Observações

- O frontend **não** acessa as APIs da NASA diretamente. Todas as requisições passam pelo backend (`/api/*`), que funciona como proxy com cache.
- O backend mantém cache em memória por 5 minutos para evitar chamadas repetidas.
- Se precisar alterar a API key da NASA, edite o arquivo `core/config.py`.
