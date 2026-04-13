# 🤖 Agente Text-to-SQL (Python + Gemini + PostgreSQL)

## 📌 O que é este projeto?
Este é um Agente de Inteligência Artificial criado em Python. Ele funciona como uma "ponte" entre um usuário comum e um banco de dados relacional. Em vez de escrever códigos complexos, o usuário faz uma pergunta em linguagem natural (ex: *"Qual a receita total de vendas pagas da Loja Física?"*), e o agente usa a API do Google Gemini para traduzir isso em uma consulta SQL válida para PostgreSQL.

Desenvolvi este projeto prático para consolidar meus conhecimentos em engenharia de software básica, integração de APIs e banco de dados durante minha transição de carreira para a área de Dados.

## 🎯 O Problema que este projeto resolve
**O Gargalo de Dados:** Em muitas empresas, gestores, equipes de vendas e marketing precisam de informações rápidas para tomar decisões, mas não sabem escrever código SQL. Isso faz com que eles dependam totalmente da equipe de Engenharia/Análise de Dados até para perguntas simples, criando um gargalo.
**A Solução:** Este agente permite que qualquer pessoa da empresa faça perguntas em português simples. A IA entende a intenção, gera a query SQL e a valida no banco de dados automaticamente. Isso **democratiza o acesso aos dados**, acelera a tomada de decisão e libera a equipe técnica para focar em tarefas mais complexas.

## 🛠 Tecnologias e Ferramentas
- **Linguagem:** Python 3.13
- **Banco de Dados:** PostgreSQL (hospedado em nuvem via Neon DB)
- **Inteligência Artificial:** Google Gemini 2.5 (Generative AI)
- **Bibliotecas:** `psycopg2` (conexão com o banco), `google-generativeai` (IA), `python-dotenv` (segurança) e `jupyter` (testes).

## 💡 O que eu aprendi construindo isso (Meus Destaques)
Como profissional em nível Júnior, este projeto me trouxe aprendizados muito valiosos que vão além de apenas escrever código:
1. **Segurança de Dados:** Aprendi a esconder minhas senhas e chaves de API usando arquivos `.env` e variáveis de ambiente, garantindo que credenciais não vazem no GitHub.
2. **Engenharia de Prompt:** Configurei a IA para não me devolver "textos soltos", mas sim um arquivo **JSON estruturado** com chaves específicas, facilitando a leitura pelo Python.
3. **Tratamento de Erros:** Implementei blocos `try...except` para lidar com falhas de conexão ou mudanças de versão da API do Google, evitando que o programa "quebre" na tela do usuário.
4. **Ambientes Virtuais:** Configurei e gerenciei ambientes isolados (`.venv`) para evitar conflitos de bibliotecas no meu computador.

## 📂 Como o projeto está organizado
- `sql_agent.py`: É o "cérebro" do projeto. Contém a classe principal, as configurações de segurança e a lógica de comunicação com a IA e com o Banco de Dados.
- `demo_uso.ipynb`: Um Jupyter Notebook limpo mostrando o agente funcionando na prática e imprimindo a query SQL.
- `requirements.txt`: Lista de dependências para rodar o projeto.

## 🚀 Como testar localmente
1. Clone este repositório.
2. Crie um ambiente virtual e instale as bibliotecas:
   ```bash
   pip install -r requirements.txt
