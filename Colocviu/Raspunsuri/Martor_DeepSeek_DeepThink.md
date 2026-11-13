**事实与意见的区分**：以下对 dossier 数字的引用是事实；对“这意味着什么”的判断是我的意见，并标注置信度。文献引用仅限我实际打开的页面。

---

**Q1. 重建是否可能只是假象？**

R1–R3 的核心弱点是**竞争者 B_strong 与 D1/D2 在定义上近乎共线**。D1 被定义为全参数更新的欧氏范数 \(\|\Delta\theta\|\)；而 Adam 的更新近似为 \(\eta \hat{m}/\sqrt{\hat{v}}\)，因此 \(\Sigma\eta\|\hat{m}\|\) 或 \(\Sigma\eta\|\hat{g}\|/\sqrt{\cdot}\) 不是“独立遥测”，而是 D1 的解析近似。Muon 论文明确记录 AdamW 的 update RMS 通常在 0.2–0.4，dossier 也引用了这一机制。这意味着 R1 中 D1 的 \(R^2=0.94\)（\(\Delta N+\Sigma\eta\|\hat{m}\|\)）和 R3 中 D1 的 0.86–0.95 **至少部分是同义反复**。G2 失败并不能自动推出“D1 无信息”，只能推出“D1 的信息已被一个与它数学上接近的项吸收”。置信度：高。

**其他可信假象**：(i) **训练/测试泄漏**：R1 说“test on each tech3 run, training on the other four runs”，如果是按时间窗口随机划分而非按运行（run）留一，那么同一优化轨迹的相邻窗口会同时出现在训练和测试中，夸大 \(R^2\)。dossier 没有明确说“leave-one-run-out”在 R1 中是如何实现的；R5 明确写了“leave one seed out”，R1 没有。检查：按 run 分组交叉验证，报告 per-run 的 \(R^2\) 及其分布。(ii) **窗口长度**：8 步窗口可能短于“时钟”的意图尺度；但 R5 的 869 个窗口和 R3 的区间设计不同，窗口长度的影响未被系统扫描。检查：对窗口长度 \(\{8,16,32,64\}\) 做敏感性分析，看 \(R^2\) 是否随窗口单调上升——如果“时钟”的信息只在长窗口才出现，那它就不是 step-level 的时钟。(iii) **速率 vs 累积值**：预测速率 \(\rho=\Delta c_e/\Delta N\) 在差分后放大了高频噪声；累积值的可预测性可能更高也可能更低，但 dossier 没有报告累积值的 \(R^2\)。检查：对累积 \(c_e(t)\) 本身做 leave-one-run-out 重建，而不仅是速率。(iv) **合成任务**：40 个任意事实的任务族可能产生高度相似的优化轨迹（相同的键-值格式、相同的 64 个值 token），使遥测与时钟的相关性被任务同质性放大。检查：在 F6 的 distractor 条件下重复 G2；dossier 自己已经显示 F6 是唯一“no cheap scalar reconstructs D3”的族，这说明合成任务并非完全同质，但需要确认 F6 的 G2 失败是否稳健。

**R5–R6 的 LM 重建**：\(\Sigma\eta\|\hat{m}\|\) 对 \(\tau\) 速率的 \(R^2=0.94\)【dossier §4】。同样，\(\tau\) 被定义为 LoRA 因子上的 \(\Sigma\|\Delta\theta\|\)，而 \(\Delta\theta\) 在 Adam 下近似正比于 \(\eta\hat{m}/\sqrt{\hat{v}}\)，所以 \(\Sigma\eta\|\hat{m}\|\) 是 \(\tau\) 的“一步近似”。**这不是一个独立的预测器，而是一个重新表述的时钟。** 要证明 \(\tau\) 无信息，需要用**不包含任何梯度/矩信息的纯调度变量**（\(\Sigma\eta\)）作为竞争者；dossier 显示纯调度只有 0.67（Imtech1）和 0.58（Imtech2），这确实说明 \(\tau\) 不能被纯学习率调度重建。但这只排除了“\(\tau\) 只是学习率表”的平凡假设，并没有排除“\(\tau\) 是 Adam 矩统计的确定性函数”这一更根本的平凡性。

**Q2. G2 失败后，H1 还值得跑吗？**

**对 D1、D1_rel、D2 和 FOREVER \(\tau\)：不。** G2 的预定规则是“held-out \(R^2 \ge 0.90\) 则不可识别”。dossier 的 R1、R3、R5、R6 一致显示这些时钟的速率被 B_strong 中的单项（\(\Sigma\eta\|\hat{m}\|\) 或类似项）以 \(R^2\ge 0.86\) 重建。继续用这些时钟跑 H1，即使 H1“显著”，也无法区分是时钟的独特信息还是遥测的共线信息。**正确的科学报告是：关闭参数时钟的 H1 线，把 G2 失败作为主要结果报告，并明确说明“这个失败是信息性的——它表明 Adam 类优化器的参数距离时钟在数学上接近于矩统计的函数”**。这本身是一个可发表的负面结果，前提是分析按 run 分组、报告 per-run 分布，并包含一个**解析近似**的显示（\(\Delta\theta\) 与 \(\eta\hat{m}/\sqrt{\hat{v}}\) 的相关性）。

**Q3. D3 对 C10c 在 F6 中是真实问题还是设计假象？**

F6 是唯一“没有廉价标量重建 D3”的族，这**可能是一个真实信号，但也可能是 F6 的设计使 C10c 失效**。C10c 是“参考电池 R 上逐项损失变化的均值”。F6 的 distractor 段有 30% 标签噪声；标签噪声会直接污染 C10c 的损失变化，因为 C10c 在噪声标签上计算损失变化，而 D3 是**函数输出的 \(\sqrt{3}\) 散度**，对标签噪声不敏感——它只看模型在 128 个从未训练的 prompt 上的输出分布。因此，F6 中 D3 的优势可能仅仅反映了“D3 的探针不受训练标签噪声影响”，而不是“函数时钟携带了超出同成本函数统计的信息”。置信度：中等。

**决定性的、可预注册的测试**：在 F6 上，预注册比较两个模型对**同一目标 T1（half A 上的损失增加）** 的预测 \(R^2\)：(a) D3；(b) C10c；(c) 一个**打乱探针顺序的 D3 版本 D3_shuffled**——在相同的 128 个探针上计算函数距离，但把 8 步块之间的配对随机打乱，从而保留“函数探针”的成本和敏感性，但破坏“累积时间”的语义。如果 D3 在 (a) 中优于 (b) **且** 优于 (c)，那么“函数累积”有独特信息；如果 D3 只优于 C10c 但不优于 D3_shuffled，则 F6 的效应只是“函数探针 vs 损失标量”，与“时间”无关。**通过标准**：D3 相对于 C10c 的 held-out \(R^2\) 增益的 95% bootstrap 下界 > 0，且 D3 相对于 D3_shuffled 的增益下界 > 0；两者必须同时满足。**成本**：F6 已有 1 seed/族；要得到稳定的 bootstrap，需要至少 5 seeds × F6 的 20,480 步。按 12.3 runs/hour 计算，5 个 F6 runs ≈ 5 × (20480/3072? 不，dossier 说 12.3 个完整 synthetic-world runs/hour，一个 run 包括 childhood+life) ≈ 0.4 小时；但需要多个种子和 D3/C10c/D3_shuffled 的重算（D3 每 8 步一次，forward passes 在已有日志中可能可复用）。保守估计：**6–10 小时**（包括分析和 bootstrap）。这在小 laptop 上是可承受的。

**Q4. FOREVER 可以公平地声称什么？**

R5–R8 能支持的最强公平声明是：**在 Qwen3-0.6B 的 FOREVER 调度上，\(\tau\) 的速率主要由优化器矩统计（\(\Sigma\eta\|\hat{m}\|\)）决定，纯学习率调度不能重建 \(\tau\) 的速率（\(R^2=0.67\)，低于预注册的 0.80）；阶段层面的 \(\tau\) 与纯调度在触发 \(d=1,2\) 时几乎无法区分（中位差 −1 步）**。但不能声称：(i) \(\tau\) 携带了超出 Adam 矩统计的信息——因为 \(\Sigma\eta\|\hat{m}\|\) 是 \(\tau\) 的近似；(ii) \(\tau\) 的调度优于步数调度——R8 的有效性失败和回放混淆使任何性能比较无效；(iii) FOREVER 的 benchmark 增益——dossier 自己没有复现 SuperNI 和 >0.6B 模型。R7 的“duration artefact”进一步说明，阶段层面的高 \(R^2\) 来自阶段长度，而非时钟的信息内容。置信度：高。

**让声明不可争议的实验**：在 LM 臂上运行**三个回放调度器**，相同的 Qwen3-0.6B/LoRA/数据/计算预算：(1) FOREVER \(\tau\) 驱动；(2) \(\Sigma\eta\|\hat{m}\|\) 驱动（一个“矩时钟”，与 \(\tau\) 近似但不等同）；(3) 纯调度驱动（\(\Sigma\eta\) 归一化）。预注册的主要终点是**每个任务结束时的旧任务探针准确率**（在 FOREVER 最终回放**之前**读取，以避免 R8 的回放混淆）和**总回放步数**。通过/失败：如果 (1) 与 (2) 的差异在预注册的等价界内（例如 \(\pm 1\%\) 准确率），则 \(\tau\) 的可操作内容与矩统计无法区分；如果 (1) 优于 (3) 且 (1) 与 (2) 不同，则 \(\tau\) 有独特内容。成本：每个调度器 3 seeds × 10 tasks × 15 min ≈ 7.5 小时/调度器，三个调度器 ≈ **22.5 小时**，加上分析。**短描述性说明**：现在**可以**写，但必须标注“descriptive, not confirmatory”，并且**不得**包含任何“FOREVER 时钟优于步数”的因果声明。它不会污染主研究的预注册，只要主研究的预注册明确声明“该说明不影响 G2 或 H1 的判定规则”。

**Q5. Level 2 的 \(c_e\) 是否被削弱？**

**是，被实质性削弱，但不是被完全否定。** Level 2 的原始表述是：累积内部变化 \(c_e\) “carries information beyond logged optimizer statistics ... remains open”。R1–R6 显示，对于**参数距离**候选（D1、D1_rel、D2、\(\tau\)），这个“open”问题现在有了一个清晰的**否定答案**：在 Adam 类优化器下，参数距离的累积在速率层面与矩统计的累积高度共线（\(R^2\ge 0.86\)–0.99），因此不能声称独特信息。对于**函数距离 D3**，F6 留下了一个**窄的、未决的**问题，但 D3 的竞争者 C10c 尚未在同等成本下被强制比较（dossier §6 自己承认）。下一版本应：(i) 明确写出 G2 对参数时钟的失败，并把“参数距离时钟”从 Level 2 的候选列表中**降级**为“一个被重建分析排除的平凡实现”；(ii) 把 Level 2 重新表述为“函数距离在**标签噪声干扰**条件下可能携带超出损失标量的信息，这一假设尚待 F6 上的预注册检验”；(iii) 撤回任何暗示“任何内部变化累积都能提供不可伪造的时间证据”的表述，因为 R1–R6 恰好表明，在标准优化器下，内部变化的主要成分是优化器状态的确定性函数。置信度：中高。

**Q6. 红队：最强反驳与最重要的缺失控制**

**最强反驳**：这些结果之所以看起来“时钟无信息”，是因为**竞争者的设计使 G2 无法失败**。B_strong 包含了 \(\Sigma\eta\|\hat{m}\|\) 和 \(\Sigma\eta\|\hat{g}\|\)，而 D1 和 \(\tau\) 在 Adam 下的定义就是这些量的累积。因此，“G2 失败”不是经验发现，而是**定义上的必然**——只要优化器是 Adam 且学习率非零，参数距离的累积就近似正比于矩统计的累积。这意味着 R1–R6 的负面结论**没有证伪任何有趣的东西**：它只是重新发现了 Adam 的更新规则。置信度：高。这个反驳不适用于 **D3**，因为 D3 是函数空间的距离，不是参数空间的距离；也不完全适用于**纯调度时钟**，因为 \(\Sigma\eta\) 不包含梯度信息。

**最重要的缺失控制**：**一个与 D3 计算成本相同、但不累积时间语义的“函数探针活动”基线**——即 D3_shuffled（打乱 8 步块配对）或“单步函数距离的随机子集”。没有这个控制，F6 中 D3 的任何优势都无法归因于“累积时间”，而只能归因于“使用了函数探针”。这比增加更多种子或更多合成族都更关键，因为它是**唯一能把“时间”与“函数测量”分开的控制**。

**Q7. 方向选择**

**DIRECTION: C** — 关闭参数时钟线（G2 重建的 closure report + 一份描述性的 FOREVER 说明），只保留 D3 对 C10c 在 F6 上的小型预注册确认测试。理由：参数时钟（D1、D1_rel、D2、\(\tau\)）的 G2 失败是**决定性的且可解释的**——它们被 Adam 矩统计近似重建，继续 H1 只会产生无法归因的结果。D3 在 F6 中的残余异常是**唯一**尚未被廉价标量排除的候选，但它需要一个带 D3_shuffled 控制的严格测试，而不是一个完整的 Stage A。FOREVER 说明应作为描述性记录发表，明确“\(\tau\) 的可操作内容与矩统计无法区分，纯调度不能重建 \(\tau\) 的速率”，但不声称调度优越性。这符合决策规则中的“更具可证伪性且更便宜”：总成本约 30–40 小时（F6 的 D3 测试 ~8h + FOREVER 三调度器比较 ~23h + 分析），远低于一个完整的合成 + LM Stage A。

---

**DECISIVE TESTS**（每个测试均需按 run 分组交叉验证，报告 per-run 分布，预注册通过/失败标准）

1. **G2 解析共线性诊断**。假设：D1/D1_rel/D2/\(\tau\) 的速率与 \(\Sigma\eta\|\hat{m}\|\) 的共线性是 G2 失败的主因。通过标准：在留一 run 的线性模型中，\(\Sigma\eta\|\hat{m}\|\) 单独对 D1 速率的 \(R^2\ge 0.85\)，且加入 D1 后对 T1 的增量 \(R^2\) 的 95% 下界 \(\le 0\)。失败标准：D1 在控制 \(\Sigma\eta\|\hat{m}\|\) 后仍有 >0.02 的增量 \(R^2\)。成本：~2 小时（使用已有日志）。
2. **D3 vs C10c vs D3_shuffled（F6）**。假设：D3 的累积函数距离在 F6 中对 T1 的预测优于同成本损失变化和打乱时间的函数距离。通过标准：D3 对 C10c 的增量 \(R^2\) 的 95% bootstrap 下界 >0，**且** D3 对 D3_shuffled 的增量下界 >0。失败标准：任一比较的 bootstrap 区间包含 0。成本：~8 小时（5 seeds × F6，包括 D3 重算）。
3. **FOREVER 三调度器比较**。假设：\(\tau\) 驱动的回放与 \(\Sigma\eta\|\hat{m}\|\) 驱动的回放在旧任务准确率上不可区分，且两者优于纯调度。通过标准：\(\tau\) vs 矩时钟的准确率差在预注册等价界 \(\pm 1\%\) 内；\(\tau\) vs 纯调度的差 >1% 且 bootstrap 下界 >0。失败标准：\(\tau\) 显著优于矩时钟（则 \(\tau\) 有独特内容）或 \(\tau\) 不优于纯调度（则时钟的调度价值被否定）。成本：~23 小时（3 调度器 × 3 seeds × 10 tasks）。
4. **窗口长度与累积值敏感性**（仅当 Test 1 显示 D1 仍有残余信号时运行）。假设：G2 失败不是窗口长度造成的。通过标准：在窗口 \(\{8,16,32,64,128\}\) 上，D1 对 T1 的增量 \(R^2\) 不随窗口增大而单调上升超过 0.02。成本：~3 小时。

**MISSING CONTROL**: D3_shuffled——在相同 128 个探针上计算函数距离，但随机打乱 8 步块的配对，以分离“函数探针测量”与“累积时间”。

**CONFIDENCE**: **medium-high** — 对“参数时钟被 Adam 矩统计重建”的判断是高置信度；对“D3 在 F6 中是否有超出函数探针的独特信息”的判断是中等置信度，因为尚未运行 D3_shuffled。

---

**FINAL ANSWER BLOCK**

DIRECTION: **C** — 关闭参数时钟线（G2 重建 closure report + 描述性 FOREVER 说明），仅保留 D3/F6 的小型预注册确认测试。

DECISIONS: 1: **other: close the parameter-clock line; no full Stage A**; 2: **yes** (only the 0a/0b split for the D3/F6 test); 3: **postpone**; 4: **fully** (embeddings out of weight decay, as provisionally applied); 5: **before final replay**; 6: **bf16** (avoids GradScaler skips); 7: **yes** (C10c mandatory alongside D3); 8: **now** (descriptive note, explicitly non-confirmatory)

DECISIVE TESTS:
1. G2 analytic collinearity diagnostic — hypothesis: \(\Sigma\eta\|\hat{m}\|\) alone reconstructs D1/D2/\(\tau\) rates at \(R^2\ge 0.85\); pass if this holds and D1 adds \(\le 0\) incremental \(R^2\) after control; ~2 laptop-hours.
2. D3 vs C10c vs D3_shuffled on F6 — pass if D3 beats both by a 95% bootstrap lower bound >0 on held-out \(R^2\) for T1; ~8 laptop-hours.
3. FOREVER three-scheduler comparison (\(\tau\) vs \(\Sigma\eta\|\hat{m}\|\) vs schedule-only) — pass if \(\tau\) and moment-clock are within \(\pm 1\%\) pre-replay accuracy and both beat schedule-only; ~23 laptop-hours.
4. Window-length/cumulative-value sensitivity — pass if D1's incremental \(R^2\) does not rise by >0.02 across window sizes 8→128; ~3 laptop-hours.

MISSING CONTROL: **D3_shuffled** — same function probes, same cost, but 8-step block pairings randomized, to separate “function measurement” from “accumulated time”.

CONFIDENCE: **medium-high** — the parameter-clock closure is well supported by the collinearity argument; the residual D3/F6 question requires the D3_shuffled control before any positive claim.