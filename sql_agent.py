import google.generativeai as genai
import psycopg2
import json
import logging
from datetime import datetime

class TextToSQLAgent:
    """
    Agente de IA para conversão de linguagem natural em SQL PostgreSQL
    com pipeline de QA e rastreabilidade completa.
    """

    def __init__(self, gemini_api_key, db_connection_string):
        # Configurar Gemini
        genai.configure(api_key=gemini_api_key)
        # CORREÇÃO: usar nome atualizado do modelo
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        # Configurar banco de dados
        self.db_connection_string = db_connection_string

        # Configurar logging
        self.setup_logging()

        # Contador de queries
        self.query_count = 0

    def setup_logging(self):
        """Configura sistema de logs estruturado"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Sistema de logs iniciado")

    def convert_to_sql(self, natural_language_query, table_schema=None):
        """
        Converte linguagem natural em SQL PostgreSQL validado

        Args:
            natural_language_query: Pergunta em linguagem natural
            table_schema: Esquema das tabelas (opcional)

        Returns:
            dict: Query SQL, explicação e metadados
        """
        self.query_count += 1
        query_id = f"Q{self.query_count:03d}"

        # Prompt engineering com validação
        prompt = f"""
Você é um especialista em PostgreSQL. Converta a pergunta abaixo em uma query SQL válida.

PERGUNTA: {natural_language_query}

{f"ESQUEMA DAS TABELAS: {table_schema}" if table_schema else ""}

RETORNE UM JSON com esta estrutura exata (sem markdown, sem ```):
{{
  "sql": "query SQL aqui com comentários",
  "explicacao": "explicação breve do que a query faz",
  "validacoes": ["validação1", "validação2", "validação3"],
  "sugestoes": ["sugestão1", "sugestão2"]
}}

REGRAS:
- Use apenas PostgreSQL syntax
- Inclua comentários SQL inline
- Use JOINs explícitos (INNER JOIN, LEFT JOIN)
- Retorne APENAS o JSON, sem texto adicional
"""

        try:
            # Gerar resposta
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Limpar markdown se houver
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            result = json.loads(result_text)

            # Log estruturado
            log_entry = {
                'query_id': query_id,
                'timestamp': datetime.now().isoformat(),
                'natural_language': natural_language_query,
                'sql_generated': result['sql'],
                'status': 'success'
            }

            self.logger.info(f"Query {query_id} gerada: {natural_language_query[:50]}...")

            return {
                'query_id': query_id,
                'sql': result['sql'],
                'explicacao': result['explicacao'],
                'validacoes': result.get('validacoes', []),
                'sugestoes': result.get('sugestoes', []),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Erro ao gerar query {query_id}: {str(e)}")
            return {'error': str(e), 'query_id': query_id}

    def validate_query(self, sql_query):
        """
        Valida a query no banco PostgreSQL usando EXPLAIN

        Args:
            sql_query: Query SQL para validar

        Returns:
            dict: Resultado da validação
        """
        try:
            conn = psycopg2.connect(self.db_connection_string)
            cursor = conn.cursor()

            # Valida a query sem executar
            cursor.execute(f"EXPLAIN {sql_query}")
            plan = cursor.fetchall()

            self.logger.info(f"Query validada com sucesso no PostgreSQL")

            return {
                'status': 'valid',
                'execution_plan': str(plan),
                'message': 'Query SQL válida (testada com EXPLAIN)'
            }

        except Exception as e:
            self.logger.error(f"Erro na validação: {str(e)}")
            return {'status': 'invalid', 'error': str(e)}

        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

    def get_stats(self):
        """Retorna estatísticas de uso do agente"""
        return {
            'total_queries_geradas': self.query_count,
            'timestamp': datetime.now().isoformat()
        }

print("Classe TextToSQLAgent criada com sucesso!")