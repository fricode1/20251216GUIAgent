```mermaid
sequenceDiagram
    autonumber
    participant Index as index.ts (Entry)
    participant Exec as executor.ts (Executor)
    participant Nav as NavigatorAgent
    participant Plan as planner.ts (PlannerAgent)
    participant Base as base.ts (BaseAgent)

    Index->>Index: setupExecutor()
    
    Index->>Exec: new Executor()
    activate Exec
    
    Note over Exec: 构造函数开始执行
    
    Exec->>Nav: new NavigatorAgent()
    activate Nav
    Nav-->>Exec: 返回 Navigator 实例
    deactivate Nav

    Exec->>Plan: new PlannerAgent()
    activate Plan
    
    Note over Plan: 构造函数开始执行
    
    Plan->>Base: super() (调用父类构造函数)
    activate Base
    
    Base->>Base: getModelName()
    Note right of Base: 返回 "qwen-plus"
    
    Note over Base: 初始化 chatLLM 和 modelName
    
    Base-->>Plan: 父类初始化完成
    deactivate Base
    
    Plan-->>Exec: 返回 Planner 实例
    deactivate Plan
    
    Exec-->>Index: 返回 Executor 实例 (currentExecutor)
    deactivate Exec
```

```typescript
index.ts
    currentExecutor = setupExecutor()  // 调用 index.js/setupExecutor()

index.ts
    setupExecutor()
        executor = new Executor()  // 调用 executor.ts/Executor/constructor()

executor.ts
    class Executor
        constructor()
            this.navigator = new NavigatorAgent()
            this.planner = new PlannerAgent()  // 调用 planner.ts/PlannerAgent/constructor

planner.ts
    class PlannerAgent extends BaseAgent
        constructor()
            super()  // 调用 base.ts/BaseAgent/constructor()

base.ts
    class BaseAgent
        constructor()
            this.chatLLM = options.chatLLM
            this.modelName = this.getModelName()  // "qwen-plus"
```