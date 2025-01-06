from trulens_eval import Tru, Feedback, TruLlama
from trulens_eval.feedback import Groundedness
from trulens_eval.feedback.provider.openai import OpenAI as OpenAIFeedback
import config

openai = OpenAIFeedback()

def get_groundedness():
  """
  Returns the trulens groundedness feedback.
  """
  return Groundedness(groundedness_provider=openai)

def setup_trulens(app_id, search_table, db_connection):
  """
    Sets up TruLens feedback functions and returns the instrumented Llama.
    Requires: trulens_utils.groundedness, data_utils.snowflake_search, llm_utils.generate_llm_response
  """

  grounded = get_groundedness()

  f_relevance = Feedback(openai.relevance).on_input_output()

  def run_rag(prompt: str):
      search_results = data_utils.snowflake_search(prompt, search_table, db_connection)
      context_string = "\n".join([f"{result['text']}" for index, result in search_results.iterrows()])
      response = llm_utils.generate_llm_response(prompt, context_string, db_connection)
      return response
  
  tru_llama = TruLlama(
        app_id=app_id,
        app_fn=run_rag,
        feedbacks=[
            grounded.groundedness_measure.on(
                text=grounded.groundedness_measure.on_output_text,
                context=grounded.groundedness_measure.on_input_text
            ).with_name("Groundedness"),
           f_relevance
       ],
        config={"project_name": config.TRULENS_PROJECT_NAME}
    )
  return tru_llama