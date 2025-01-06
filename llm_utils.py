import snowflake.connector
import config
import json

def generate_llm_response(query, context, conn):
  """
    Generates a response using a Mistral LLM in Snowflake.
  """
  prompt = f"""
      Given the following context: {context}
      Answer the following question: {query}
    """
  sql = f"""
        SELECT cortex.complete(
            '{config.LLM_MODEL}',
             '{prompt}'
            ) as generated_text
     """
  result = execute_query(sql, conn)
  if not result.empty:
    return result["generated_text"].iloc[0]
  return "I am sorry. I cannot provide a response with the context available."