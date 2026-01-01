```mermaid
sequenceDiagram
    autonumber
    participant MR as MessageRouter.ts
    participant EH as ExecutionHandler.ts
    participant E as Execution.ts
    participant L as Logging.ts
    participant BOA as BrowserOSAdapter.ts

    Note over MR: routeMessage()
    MR->>EH: handleExecuteQuery(message)
    
    Note over EH: this.execution.run(query)
    EH->>E: run(query)
    
    Note over E: Logging.logMetric()
    E->>L: logMetric()
    
    Note over L: getBrowserOSAdapter().logMetric()
    L->>BOA: logMetric()

    rect rgb(255, 235, 235)
        Note right of BOA: 逻辑检查点
        alt chrome.browserOS 存在
            BOA->>BOA: 继续执行逻辑
        else chrome.browserOS 为 undefined
            BOA-->>BOA: ❌ 抛出 TypeError: Cannot use 'in' operator to search for 'logMetric' in undefined
        end
    end
```


```TypeScript
webpack://Agent/src/background/router/MessageRouter.ts
    routeMessage()
        handler(message)  // 调用 webpack://Agent/src/background/handlers/ExecutionHandler.ts/handleExecuteQuery()

webpack://Agent/src/background/handlers/ExecutionHandler.ts
    handleExecuteQuery()
        this.execution.run(query)  // 调用 webpack://Agent/src/lib/execution/Execution.ts/run()

webpack://Agent/src/lib/execution/Execution.ts
    run()
        Logging.logMetric()  // 调用 webpack://Agent/src/lib/utils/Logging.ts/logMetric()

webpack://Agent/src/lib/utils/Logging.ts
    logMetric()
        getBrowserOSAdapter().logMetric()  // 调用 webpack://Agent/src/lib/browser/BrowserOSAdapter.ts/BrowserOSAdapter/logMetric()
        
webpack://Agent/src/lib/browser/BrowserOSAdapter.ts
    class BrowserOSAdapter
        logMetric()
            if ("logMetric" in chrome.browserOS)  // 若使用通用浏览器，则 chrome.browserOS 为 undefined，xxx in undefined 是语法错误。
                ...
```