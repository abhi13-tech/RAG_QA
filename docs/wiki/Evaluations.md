Evaluations

Variants
- dense
- dense+rerank
- hybrid
- hybrid+rerank

Metrics
- EM: exact match to gold answer
- F1: token-level F1
- Faithfulness: fraction of answer tokens grounded in contexts
- Retrieval Recall: gold snippet present in top-k

Run
- make eval
- Uses eval/sets/sample.jsonl

Notes
- For real LLM answers, set LLM_MODE=litellm|openrouter and add credentials.

