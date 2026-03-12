
---

### Guideline 1: Ask the LLM to analyze complexity and inefficiencies before writing the final code[2,3]
**Description:**  
When requesting performance improvements, require the LLM to first identify bottlenecks in the current implementation, analyze time and space complexity, and then propose and implement a more efficient approach.s

**Reasoning:**  
Optimization quality improves when the model explicitly reasons about inefficiencies before generating code. This structured “analyze first, optimize second” approach activates performance reasoning rather than surface-level rewriting. Research shows that critique-based and self-optimization prompting improves efficiency-oriented outputs by encouraging bottleneck detection and complexity comparison [2][3].

**Bad Prompt Example (Typical Developer Request):**
```
This function is running slow. Can you optimize it?
Here is the code:
```

**Good Example:**
```
The following function is correct but too slow for large inputs.

First, identify the main bottleneck in the current implementation.
Analyze its time and space complexity.
Explain how a more efficient approach would improve complexity.
Then provide the optimized implementation.

Assume input size can reach 10^5.
Return the final optimized code.
```

---

### Guideline 2: Tell the LLM it is allowed to change the algorithm, not just the code style [1]
**Description:**  
Explicitly instruct the LLM that it may completely replace the algorithm and data structures if needed. Clarify that performance improvement is the goal, not stylistic refactoring.

**Reasoning:**  
LLMs often preserve inefficient structure unless explicitly permitted to change it. Significant performance improvements usually require switching algorithms or data structures rather than applying minor code-level edits [1].

> 

**Bad Prompt Example**
```
Can you refactor this code to make it faster without changing too much?
Try to keep the same structure.
```

**Good Example:**
```
Improve the performance of the following function.

You may completely change the algorithm and data structures if needed.
Do not preserve the current approach if it is inefficient.
Focus on reducing time complexity rather than small refactoring changes.

Return only the optimized implementation.
```

---

### Guideline 3: Explicitly ask it to optimize for worst-case input size while preserving correctness [4]
**Description:**  
Instruct the LLM to assume maximum input constraints and ensure the solution remains correct and efficient under worst-case scenarios.

**Reasoning:**  
Without explicit worst-case constraints, the model may optimize for average cases or small inputs, leading to poor scalability. Mentioning maximum input size encourages the selection of scalable algorithms and discourages quadratic solutions [4].


**Bad Prompt Example (Typical Developer Request):**
```
The code works but feels slow when the data gets big.
Can you improve it?
```

**Best Prompt Example:**
```
The current implementation times out for large inputs.

Assume input size is at the maximum constraint (n up to 10^6).
The solution must remain correct.
Optimize specifically for worst-case performance and avoid quadratic-time solutions.

Return the optimized implementation.
```

---

## 2. References

[1] Jain, N., et al. *Learning Performance-Improving Code Edits.* arXiv:2302.07867v5.  

[2] *EFFI-LEARNER: Enhancing Efficiency of Generated Code via Self-Optimization.* arXiv: 2405.15189v4

[3] Zhu, et al. *More Than Just Functional: LLM-as-a-Critique for Efficient Code Generation.* arXiv: NeurIPS 2025.  

[4] GPT-5.2 .

---