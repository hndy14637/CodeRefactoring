# 环境配置指令
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

pip install autogen-core autogen-ext
pip install langchain-core
pip install langchain-openai

# 论文核心信息
## 标题
Automating Best-Practice Refactoring in Java via Multi-Agent Planning and Verification

## 摘要
Best-practice rules capture widely accepted coding conventions that improve software maintainability, safety, and extensibility. Modern static analysis tools, such as PMD and SonarQube, can accurately detect best-practice violations, yet repairing these issues remains largely manual, time-consuming, and error-prone. Although large language models show promise in code generation, directly applying them to refactoring often yields unsafe or incomplete transformations, especially for semantically subtle best-practice rules.
In this paper, we propose BestRefactor, the first automated approach that explicitly targets Java best-practice violations at scale. BestRefactor adopts a multi-agent, recipe-guided framework that decomposes refactoring into three coordinated stages: (i) a Planning Agent that determines applicability and safety, (ii) a Refactoring Agent that applies rule-specific transformation recipes, and (iii) a Verification Agent that validates correctness and rule compliance. This design enables reliable, behavior-preserving refactoring beyond naïve single-step LLM rewriting. We implement BestRefactor as a practical tool integrated with PMD and evaluate it on 10 real-world Java libraries spanning five application domains, comprising 844 detected best-practice violations. Experimental results show that BestRefactor successfully produces verified repairs for 72.6% of all detected violations end to end, outperforming a direct LLM baseline by over 11 percentage points in verified repair rate. An ablation study confirms that planning, recipe guidance, and verification each play a critical role in achieving reliable refactoring. Finally, our performance analysis demonstrates that BestRefactor is practical in terms of runtime and cost.

# BestRefactor方法流程图
## 1. 纯文本版流程图（直观展示逻辑）
开始
  ├─ 输入：Java代码 + PMD检测到的最佳实践违规
  └─ 进入 Planning Agent（规划代理）
       ├─ 执行：1. 校验违规规则适用性 2. 评估重构安全性 3. 生成重构规划方案
       ├─ 分支1：规划不通过（不适用/不安全）→ 终止重构，返回原因 → 结束
       └─ 分支2：规划通过 → 进入 Refactoring Agent（重构代理）
            ├─ 执行：根据规则专属转换模板（Recipe）执行Java代码重构
            ├─ 生成：重构后的Java代码
            └─ 进入 Verification Agent（验证代理）
                 ├─ 执行：1. 验证语法正确性 2. 验证规则合规性 3. 验证行为一致性（无功能变更）
                 ├─ 分支1：验证不通过 → 反馈问题至Refactoring Agent → 重新执行重构
                 └─ 分支2：验证通过 → 输出最终重构代码 → 结束

## 2. Mermaid流程图代码（可渲染为可视化图片）
### 渲染方式：复制以下代码到 https://mermaid.live/，可下载PNG/SVG格式流程图
flowchart TD
    A["开始：输入Java代码 + PMD检测违规"] --> B["Planning Agent（规划代理）"]
    B --> C{"1. 校验规则适用性<br/>2. 评估重构安全性<br/>3. 生成重构方案"}
    C -- 规划不通过 --> D["终止重构，返回原因"] --> Z["结束"]
    C -- 规划通过 --> E["Refactoring Agent（重构代理）"]
    E --> F["执行规则专属Recipe重构代码"]
    F --> G["生成重构后Java代码"]
    G --> H["Verification Agent（验证代理）"]
    H --> I{"1. 验证语法正确性<br/>2. 验证规则合规性<br/>3. 验证行为一致性"}
    I -- 验证不通过 --> J["反馈问题→重构代理重试"] --> E
    I -- 验证通过 --> K["输出最终重构代码"] --> Z["结束"]
# 环境配置指令
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

pip install autogen-core autogen-ext
pip install langchain-core
pip install langchain-openai

# 论文核心信息
## 标题
Automating Best-Practice Refactoring in Java via Multi-Agent Planning and Verification

## 摘要
Best-practice rules capture widely accepted coding conventions that improve software maintainability, safety, and extensibility. Modern static analysis tools, such as PMD and SonarQube, can accurately detect best-practice violations, yet repairing these issues remains largely manual, time-consuming, and error-prone. Although large language models show promise in code generation, directly applying them to refactoring often yields unsafe or incomplete transformations, especially for semantically subtle best-practice rules.
In this paper, we propose BestRefactor, the first automated approach that explicitly targets Java best-practice violations at scale. BestRefactor adopts a multi-agent, recipe-guided framework that decomposes refactoring into three coordinated stages: (i) a Planning Agent that determines applicability and safety, (ii) a Refactoring Agent that applies rule-specific transformation recipes, and (iii) a Verification Agent that validates correctness and rule compliance. This design enables reliable, behavior-preserving refactoring beyond naïve single-step LLM rewriting. We implement BestRefactor as a practical tool integrated with PMD and evaluate it on 10 real-world Java libraries spanning five application domains, comprising 844 detected best-practice violations. Experimental results show that BestRefactor successfully produces verified repairs for 72.6% of all detected violations end to end, outperforming a direct LLM baseline by over 11 percentage points in verified repair rate. An ablation study confirms that planning, recipe guidance, and verification each play a critical role in achieving reliable refactoring. Finally, our performance analysis demonstrates that BestRefactor is practical in terms of runtime and cost.

# BestRefactor方法流程图
## 1. 纯文本版流程图（直观展示逻辑）
开始
  ├─ 输入：Java代码 + PMD检测到的最佳实践违规
  └─ 进入 Planning Agent（规划代理）
       ├─ 执行：1. 校验违规规则适用性 2. 评估重构安全性 3. 生成重构规划方案
       ├─ 分支1：规划不通过（不适用/不安全）→ 终止重构，返回原因 → 结束
       └─ 分支2：规划通过 → 进入 Refactoring Agent（重构代理）
            ├─ 执行：根据规则专属转换模板（Recipe）执行Java代码重构
            ├─ 生成：重构后的Java代码
            └─ 进入 Verification Agent（验证代理）
                 ├─ 执行：1. 验证语法正确性 2. 验证规则合规性 3. 验证行为一致性（无功能变更）
                 ├─ 分支1：验证不通过 → 反馈问题至Refactoring Agent → 重新执行重构
                 └─ 分支2：验证通过 → 输出最终重构代码 → 结束

## 2. Mermaid流程图代码（可渲染为可视化图片）
### 渲染方式：复制以下代码到 https://mermaid.live/，可下载PNG/SVG格式流程图
flowchart TD
    A["开始：输入Java代码 + PMD检测违规"] --> B["Planning Agent（规划代理）"]
    B --> C{"1. 校验规则适用性<br/>2. 评估重构安全性<br/>3. 生成重构方案"}
    C -- 规划不通过 --> D["终止重构，返回原因"] --> Z["结束"]
    C -- 规划通过 --> E["Refactoring Agent（重构代理）"]
    E --> F["执行规则专属Recipe重构代码"]
    F --> G["生成重构后Java代码"]
    G --> H["Verification Agent（验证代理）"]
    H --> I{"1. 验证语法正确性<br/>2. 验证规则合规性<br/>3. 验证行为一致性"}
    I -- 验证不通过 --> J["反馈问题→重构代理重试"] --> E
    I -- 验证通过 --> K["输出最终重构代码"] --> Z["结束"]

### 可视化流程图文件：./BestRefactor_flowchart.png