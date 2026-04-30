# audit-rag 新定位：审计状态化后端

## 结论

audit-rag 不再以“聊天式 RAG”作为主要目标，而是作为合约审计 skill 的状态化后端：

- skill 负责流程、质量门槛、提交格式和何时调用工具。
- audit-rag 负责 lead ledger、triage 证据、suppression 判断、PoC recipe 和可复用知识沉淀。

## 为什么要改

两次实战后暴露出的主要问题不是历史案例不够，而是审计过程中的动态状态容易散：

- lead 查过但状态不清
- PoC 通过但后来发现 duplicate
- 问题看起来像 Medium，最后实际是 QA/Low
- false-positive / downgrade 理由分散在笔记和对话里
- provisional 知识没有统一生命周期

因此，项目价值应从“多召回一些类似 finding”转向“让审计线索不丢、降级有据、PoC 有 recipe”。

## 边界

### c4-contest-auditor skill 负责

- C4 intake / scope-first 流程
- known finding / V12 / public-known suppression 原则
- severity guardrails
- Foundry / cargo 验证纪律
- submission 文件格式、review prompt 和中文翻译约定
- 决定何时调用 audit-rag

### audit-rag 负责

- `lead-ledger.jsonl`：活跃审计线索生命周期
- `triage-lead`：RAG-backed scorecard
- `suppress-check`：duplicate / false-positive / QA downgrade 风险
- `rag-triage/<lead-id>.json`：每个 lead 的原始 triage 证据
- `data/provisional/contests/<slug>/`：活跃审计中尚未确认的候选知识
- `data/normalized/` 和 `data/eval/`：最终确认后的正式知识与回归

## 当前最小实现

CLI：

```bash
python -m audit_rag.cli.main add-lead <contest-slug> <title> [--text ...] [--component ...]
python -m audit_rag.cli.main list-leads <contest-slug>
python -m audit_rag.cli.main triage-lead <contest-slug> <lead-id>
python -m audit_rag.cli.main suppress-check <contest-slug> <lead-id>
```

默认落盘：

```text
data/provisional/contests/<contest-slug>/lead-ledger.jsonl
data/provisional/contests/<contest-slug>/rag-triage/<lead-id>.json
```

## 使用原则

1. 非 trivial lead 先入 ledger，不要只放在对话里。
2. 强 lead 用 `triage-lead`，得到 scorecard 和 PoC recipe。
3. 弱 lead、疑似重复、疑似 QA/Low 的 lead 用 `suppress-check`。
4. audit-rag 输出不是漏洞证明；当前代码 reachability、impact 和 runnable PoC 仍然必须单独验证。
5. 活跃审计知识先放 provisional；最终确认后再 promote 到 normalized/eval。
6. skill Markdown 镜像在 `docs/skills/`，后续本机 skill 更新后运行 `python3.11 scripts/sync_skill_docs.py` 同步到仓库。
