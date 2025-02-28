# DevHelperBot API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

API inteligente para auxílio no desenvolvimento de software, com processamento de linguagem natural e sistema de feedback integrado.

## 📌 Visão Geral

O DevHelperBot é uma API especializada em ajudar desenvolvedores com conceitos de programação, oferecendo:
- Respostas contextualizadas para perguntas técnicas
- Exemplos de código relevantes
- Sistema de avaliação de respostas
- Autenticação segura de usuários
- Histórico de conversas persistente

## ✨ Principais Funcionalidades

- **Autenticação JWT** com segurança BCrypt
- **Processamento de Linguagem Natural** com NLTK e modelos de ML
- **Sistema de Feedback** para avaliação de respostas
- **Banco de Dados Assíncrono** com PostgreSQL
- **Dockerização** completa do ambiente
- **Testes Automatizados** com pytest

## 🛠 Tecnologias Utilizadas

- **Backend**: FastAPI
- **Banco de Dados**: PostgreSQL + AsyncSQLAlchemy
- **Cache**: Redis
- **NLP**: NLTK + scikit-learn
- **Autenticação**: JWT + BCrypt
- **Contêinerização**: Docker + Docker Compose

## 🚀 Instalação

### Pré-requisitos:
- Docker 20.10+
- Docker Compose 2.0+

### Configuração
1. Clone o repositório:
```bash
git clone https://github.com/FelipeDeMoraes19/DevHelperBot.git
cd DevHelperBot
```

2. Inicie os serviços:
```bash
docker-compose up --build
```

## 🔧 Configuração de Ambiente

### Variáveis de ambiente (configuráveis no docker-compose.yml):
- DATABASE_URL=postgresql+asyncpg://devhelper:secretpassword@postgres:5432/devhelper_db
- REDIS_URL=redis://redis:6379/0
- SECRET_KEY=SUPERSECRETJWTKEY

### 🧪 Testes

- Para executar a suíte de testes:
```bash
docker-compose run app pytest -v
```


