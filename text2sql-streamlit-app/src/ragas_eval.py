from ragas import evaluate
from ragas.metrics import ContextPrecision, RubricsScore
import pandas as pd

def evaluate_ragas(responses, user_inputs, retrieved_contexts, references, evaluator_llm):
    context_precision = ContextPrecision(llm=evaluator_llm)
    rubrics_score = RubricsScore(name="helpfulness", rubrics={
        "score1_description": "Response is useless/irrelevant, contains inaccurate/deceptive/misleading information and/or contains harmful/offensive content. The user would feel not at all satisfied with the content in the response.",
        "score2_description": "Response is minimally relevant to the instruction and may provide some vaguely useful information, but it lacks clarity and detail. It might contain minor inaccuracies. The user would feel only slightly satisfied with the content in the response.",
        "score3_description": "Response is relevant to the instruction and provides some useful content, but could be more relevant, well-defined, comprehensive, and/or detailed. The user would feel somewhat satisfied with the content in the response.",
        "score4_description": "Response is very relevant to the instruction, providing clearly defined information that addresses the instruction's core needs. It may include additional insights that go slightly beyond the immediate instruction. The user would feel quite satisfied with the content in the response.",
        "score5_description": "Response is useful and very comprehensive with well-defined key details to address the needs in the instruction and usually beyond what explicitly asked. The user would feel very satisfied with the content in the response.",
    }, llm=evaluator_llm)

    n = len(user_inputs)
    samples = []

    for i in range(n):
        sample = {
            "user_input": user_inputs[i],
            "retrieved_contexts": list(retrieved_contexts),
            "response": responses[i],
            "reference": references[i],
        }
        samples.append(sample)

    ragas_eval_dataset = pd.DataFrame(samples)
    ragas_metrics = [context_precision, rubrics_score]

    result = evaluate(
        metrics=ragas_metrics,
        dataset=ragas_eval_dataset,
    )
    return result