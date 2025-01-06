from trulens import  TruChain
from trulens.feedback import Feedback, Groundedness
from trulens.feedback.provider.openai import OpenAI as OpenAIFeedback
import data_utils
import llm_utils
import config

openai = OpenAIFeedback()

def get_groundedness():
    """
    Returns the TruLens groundedness feedback.
    """
    return Groundedness(groundedness_provider=openai)

def setup_trulens(app_id, search_table, db_connection):
  """
    Sets up TruLens feedback functions and returns the instrumented TruChain.
    Requires: trulens_utils.groundedness, data_utils.snowflake_search, llm_utils.generate_llm_response
  """

  grounded = get_groundedness()

  f_relevance = Feedback(openai.relevance).on_input_output()

  def run_rag(prompt: str):
      search_results = data_utils.snowflake_search(prompt, search_table, db_connection)
      context_string = "\n".join([f"{result['text']}" for index, result in search_results.iterrows()])
      response = llm_utils.generate_llm_response(prompt, context_string, db_connection)
      return response
  
  tru_chain = TruChain(
        app_id=app_id,
        app_fn=run_rag,
        feedbacks=[
            grounded.on(
                text=grounded.on_output_text,
                context=grounded.on_input_text
            ).with_name("Groundedness"),
           f_relevance
       ],
        config={"project_name": config.TRULENS_PROJECT_NAME}
    )
  return tru_chain