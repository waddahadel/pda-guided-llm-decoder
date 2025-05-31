# PDA-Guided LLM Decoder

A lightweight, modular implementation of a **Pushdown Automaton (PDA)-guided decoding algorithm** for syntactic generation with Large Language Models (LLMs).

This project explores how a PDA — aware of a language's grammar — can be used to enforce syntactic correctness during autoregressive token generation. The system selects the most probable valid token at each step using a grammar-constrained decoding loop.

---

## 🚀 Motivation

Large Language Models often generate **syntactically invalid** code or structured data (like JSON or SQL). We aim to address this problem by using a **Pushdown Automaton** as a syntactic filter during generation.

This approach is inspired by methods like [SynCode](https://arxiv.org/abs/2403.01632), but re-implements the idea from scratch with a focus on simplicity, modularity, and deep understanding.

---

## ⚙️ How It Works

1. The LLM generates a distribution over the next token.
2. The PDA receives the **remainder** of the current sequence and maintains its parsing state.
3. The top-*k* tokens (by model probability) are sequentially passed to the PDA.
4. The first token accepted by the PDA is selected.
5. The process repeats until a complete, syntactically valid output is formed.

This ensures the generated output **follows the grammar** defined by a Context-Free Grammar (CFG), parsed into PDA-compatible form.

---


---

## ✅ Features

- PDA-based syntactic validation at each decoding step.
- HuggingFace model support (GPT-2, Phi, Code models, etc.).
- Easily configurable grammar via EBNF or custom parser.
- Designed for extensibility and experimentation.

---

## 📚 Goals

This project supports a B.Sc. thesis on improving syntactic correctness in language generation through formal grammar-aware methods. It serves both as a **research prototype** and an **educational tool** for understanding grammar-constrained generation.

---

## 📌 TODO

- [ ] PDA implementation with stack transitions
- [ ] Grammar parser or hardcoded rules
- [ ] Integration with HuggingFace models
- [ ] Decoding loop with PDA filtering
- [ ] Evaluation on structured generation tasks (e.g. JSON, Python)

---

## 🧠 Credits

Developed by [Wadah Elsir](https://github.com/waddahadel) as part of a bachelor’s thesis at Saarland University.



