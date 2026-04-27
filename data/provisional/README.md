# provisional audit knowledge

这个目录用于存放“审计过程中发现、但尚未经过最终结果确认”的临时知识。

## 为什么不能直接进入 normalized RAG

活跃审计中的 candidate、pattern、false-positive 判断、PoC recipe 仍可能在后续验证、独立 review、C4 judging 或最终报告阶段被推翻、降级或改写。

如果提前写入 `data/normalized/`：

- 检索会把未确认假设当成稳定知识召回；
- eval 回归会固化错误或未确认模式；
- 后续审计可能被错误相似案例误导；
- RAG 会混淆“历史确认案例”和“当前审计研究线索”。

## 存放规则

活跃审计期间，只能写入这里：

```text
data/provisional/contests/<contest-slug>/
  candidate_patterns/
  candidate_cases/
  false_positive_candidates/
  validation_recipes/
  eval_candidates/
  notes/
```

这些文件默认不参与正式检索、`validate-data` 的 normalized 数据校验，也不进入 `data/eval/retrieval_queries.jsonl`。

## 归档规则

只有在审计结束并出现最终可引用结果后，才允许从 provisional 归档到正式 RAG：

1. 最终报告、最终提交、judge/sponsor 结果或用户明确确认已经完成；
2. 重新核对 root cause、broken invariant、impact、false-positive 条件；
3. 去掉当前 contest 的偶然细节，抽象成可跨协议复用的 pattern/case/recipe；
4. 写入 `data/normalized/` 对应目录；
5. 只为已经确认的知识补充 `data/eval/retrieval_queries.jsonl`；
6. 运行：

```bash
source .venv/bin/activate
python -m audit_rag.cli.main validate-data
python -m audit_rag.cli.main --help
pytest -q
```

一句话：审计中知识先进 provisional；最终确认后，经过归档审校，才能进入 normalized RAG。
