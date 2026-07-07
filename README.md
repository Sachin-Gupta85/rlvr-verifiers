# ✅ rlvr-verifiers — deterministic reward functions for RLVR

> **Reinforcement Learning with Verifiable Rewards** lives or dies on the
> verifier: a pure, reproducible grader that turns a model's answer into a 0/1
> reward with no model-in-the-loop. This is that grader — answer extraction,
> exact math verification, reward shaping, and batch grading — with **zero**
> dependencies (no SymPy; exact arithmetic via a safe AST evaluator).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Focus](https://img.shields.io/badge/focus-RLVR%20%2F%20verifiable%20rewards-6f42c1)
![Tests](https://img.shields.io/badge/tests-pytest%20(17)-brightgreen)

## 🧩 What's inside
| Piece | Module | What it does |
|---|---|---|
| **Answer extraction** | `answer` | pulls the final answer from chatty output — `\boxed{}`, `#### n` (GSM8K), "the answer is …", or the last number |
| **Safe evaluator** | `expr` | exact-`Fraction` arithmetic via an allow-listed AST walk — untrusted output can't execute code |
| **Verifiers** | `verifiers` | `MathVerifier` (numeric/symbolic), `ExactMatch`, `MultipleChoice`, `Regex` (format) |
| **Reward shaping** | `reward` | correctness + a bounded **format bonus** — the exact signal an RL loop consumes |
| **Batch grading** | `runner` | pass rate + mean reward over a dataset |

## 🧠 Why it's "verifiable"
Every verifier is **pure and deterministic**: same `(response, gold)` → same
reward, always. No LLM judge, no randomness, no floating-point surprises
(`1/2 + 1/3` is compared as exact `5/6`, not `0.8333…`). That's the property an
RL training loop needs to trust its reward.

```
pass rate : 80%   mean reward : 0.780

  ✅ reward=1.00  extracted= '5/6'  gold='5/6'   (numeric match)
  ✅ reward=1.00  extracted='1,000' gold='1000'  (numeric match)
  ✅ reward=0.90  extracted=  '18'  gold='18'    (numeric match)   # GSM8K #### form, not \boxed -> bonus lost
  ❌ reward=0.10  extracted=  '41'  gold='42'    (numeric mismatch 41 != 42)
  ✅ reward=0.90  extracted=   '7'  gold='7'     (numeric match)   # correct, no \boxed -> bonus lost
```

## 🚀 Run
```bash
python -m rlvr        # offline demo: grade a batch with verifiable rewards
```

## ✅ Test
```bash
pip install -r requirements-dev.txt && python -m pytest -q
```

## Why it matters
The verifier is the heart of RLVR (and of any trustworthy math/coding eval). The
hard parts — robust answer extraction, exact comparison without a CAS, and
format-aware reward shaping — are implemented and tested here, safely.

---
MIT licensed. Part of a portfolio of agent-evaluation and LLM-infra projects.
