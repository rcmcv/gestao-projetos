# 📊 Sistema de Gestão de Projetos

Este é um sistema web desenvolvido em **Python + Flask** para a área de gestão de projetos de uma empresa, com foco em organização, rastreabilidade e geração de relatórios automatizados.  
Ideal para substituir planilhas e arquivos soltos, oferecendo uma base estruturada e intuitiva para gerenciar:

✅ Projetos  
✅ Materiais  
✅ Fornecedores  
✅ Clientes  
✅ Orçamentos  
✅ Relatórios por projeto

---

## 🚀 Funcionalidades

- Controle de usuários com login, senha segura e permissões
- Cadastro de clientes, fornecedores, tipos de materiais, unidades e materiais
- Associação de materiais aos projetos
- Lançamento de orçamentos por fornecedor
- Relatórios com filtro de menor preço
- Exportação futura para PDF/Excel (em construção)
- Estrutura modular, limpa e comentada para facilitar manutenção e crescimento

---

## 🛠️ Tecnologias utilizadas

- Python 3
- Flask
- SQLAlchemy (ORM)
- SQLite
- REST Client (para testes via VSCode)
- Bootstrap (futuramente para frontend)

---

## 💻 Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/gestao-projetos.git
   cd gestao-projetos

---

```bash
## ✅ Crie e ative o ambiente virtual:
python -m venv venv
venv\Scripts\activate  # no Windows

## ✅ Instale as dependências:
pip install -r requirements.txt

## ✅ Crie o banco de dados:
python criar_banco.py

## ✅ Rode o sistema:
python run.py

## ✅ Teste as rotas com REST Client (testes.http) ou Postman.
testes.http

```
---

## 📁 Estrutura do projeto
```bash
gestao_projetos/
│
├── app/
│   ├── models/            # Modelos (tabelas do banco)
│   ├── routes/            # Rotas da API (modularizado por entidade)
│   ├── templates/         # (Futuramente) HTMLs
│   ├── static/            # (Futuramente) arquivos estáticos
│   └── utils/             # Funções auxiliares
│
├── instance/              # Arquivos de configuração e banco local
├── criar_banco.py         # Script para gerar o banco
├── run.py                 # Inicializador da aplicação
├── requirements.txt       # Dependências do projeto
└── testes.http            # Arquivo de requisições REST para teste

---

## 🙋 Autor
Desenvolvido por Roberto Viana – [LinkedIn] – [Portfólio opcional]

---

## ⭐ Quer contribuir?
Fique à vontade para abrir issues ou dar sugestões!
Este projeto está em evolução e sempre aberto para melhorias.