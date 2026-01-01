```typescript
webpack://Agent/src/background/handlers/ExecutionHandler.ts
    handleExecuteTeachModeWorkflow
        workflow = teachModeService.getWorkflow(workflowId)  // 调用 webpack://Agent/src/lib/services/TeachModeService.ts/getWorkflow()
        this.execution.updateOptions({
            mode: 'teach',
            workflow: workflow
        })
        this.execution.run()

webpack://Agent/src/lib/services/TeachModeService.ts
    getWorkflow()
        storage = RecordingStorage.getInstance()
        return storage.getWorkflow(recordingId)

webpack://Agent/src/lib/teach-mode/storage/RecordingStorage.ts
    getWorkflow()
        chrome.storage.local.get(workflowKey)  // 从扩展程序的本地存储（local storage）中读取已保存的数据。chrome.storage.local 存储的数据物理上存在你的电脑硬盘中，逻辑上存储在 Chrome 浏览器用户配置文件的特定数据库里。使用了 Google 开发的 LevelDB（一种高性能键值对数据库）。数据存储在以下目录：%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Extension Settings\[你的插件ID]\
```