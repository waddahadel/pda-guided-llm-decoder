# PDA-Guided LLM Decoder

A lightweight, modular implementation of a **Pushdown Automaton (PDA)-guided decoding algorithm** for enforcing syntactic correctness during Large Language Model (LLM) generation. This project investigates how formal grammar awareness, encoded in a PDA, can be leveraged to ensure valid structured outputs from LLMs.

---

## Motivation

Large Language Models, while powerful, frequently generate syntactically invalid code or structured data (such as JSON, SQL, or programming language snippets). This poses a significant challenge for integrating LLMs into automated workflows, where malformed outputs can lead to system failures or require costly post-processing. This project aims to rigorously address this problem by employing a **Pushdown Automaton** as a real-time syntactic filter during the autoregressive decoding process.


---

## How It Works

The core of the PDA-guided decoding framework modifies the standard LLM generation loop:

1.  **LLM Token Proposal:** At each step of the generation, the Large Language Model produces a probability distribution over its entire vocabulary for the next token.
2.  **Top-k Candidate Selection:** From this distribution, a set of the top-$k$ most probable candidate tokens is extracted.
3.  **PDA Validation Loop:** Each candidate token is then sequentially passed to the PDA for validation. The PDA, maintaining its current state and stack based on the already generated valid prefix, processes the candidate token character by character.
4.  **Token Acceptance:** The first candidate token from the top-$k$ set that is fully accepted by the PDA (meaning its characters form a valid continuation according to the grammar) is selected.
5.  **State Update and Repetition:** The generated sequence is extended with the accepted token, the PDA's state is updated, and the process repeats from step 1 until a complete, syntactically valid output is formed or no valid token can be found.

This methodology ensures, by construction, that the entire generated output strictly adheres to the Context-Free Grammar (CFG) defined for the target language.

---

## Features

* **PDA-based Syntactic Validation:** Guarantees that generated outputs are syntactically correct according to the defined grammar.
* **Modular Design:** The framework separates the core decoding logic from language-specific grammar rules, encapsulated within distinct PDA instances.
* **Extensibility:** Structured for easy adaptation to new grammars and decoding strategies.

---

## Goals

This project serves as a key component of a B.Sc. thesis, focusing on enhancing syntactic correctness in LLM-based language generation through formal grammar-aware methods. It functions as a **research prototype** to explore the efficacy of PDA guidance..


---

## Credits

Developed by [Wadah Elsir](https://github.com/waddahadel) as part of a bachelor’s thesis at Saarland University.

---