# NextChat · Cloudflare Workers

独立部署 NextChat 到 `https://aiweb.cheapapi.com.cn`，Worker 名称为 `nextchat-aiweb`。

流程使用固定的 NextChat 源码提交，应用本目录中的兼容补丁，并通过 OpenNext 构建为 Cloudflare Workers 应用。

## 手机完成发布

1. 在 Cloudflare 创建专用于此次部署的 API Token，限定到目标账户和 `cheapapi.com.cn` 域名。需要创建/管理 Workers 的权限、该域名 Workers Routes 写权限，以及读取账户与域名信息的权限。可以从官方 Edit Cloudflare Workers 模板开始，核对资源范围和有效期。
2. 在本仓库的 Settings → Secrets and variables → Actions 添加两个 repository secrets：`CLOUDFLARE_API_TOKEN` 和 `CLOUDFLARE_ACCOUNT_ID`。不要把 Token 写进源码、Issue、聊天或日志。
3. 在 Actions 页面重新运行 **Deploy NextChat to Cloudflare Workers** 工作流。后续该部署分支的配置更新也会自动触发发布。

`cheapapi.com.cn` 必须已在相同 Cloudflare 账户中生效。首次绑定前检查 `aiweb` 是否已有 CNAME 或已有站点；工作流不会主动删除现有 DNS 记录。

## 首次使用

默认使用 Google 原生 Gemini API 调用 Gemma，默认模型为 `gemma-4-31b-it`，同时提供 `gemma-4-26b-a4b-it`。Google 接口地址为 `https://generativelanguage.googleapis.com/`。默认不配置公共模型密钥；打开网站后在设置中启用自定义接口、选择 Google，并填写自己的 Google AI Studio API Key。网页端接口地址保持 `/api/google`，请求经过本站 Worker 转发。

如希望 Google API Key 只保存在 Worker 端，先在 Worker 的 Settings → Variables and Secrets 中设置 `CODE` 访问码，再添加 `GOOGLE_API_KEY`。两者使用 Secret 类型，不放入构建变量或提交到仓库。Google API Key 用于模型调用，`CLOUDFLARE_API_TOKEN` 用于发布网站；这两种凭据不能互相替代。

不会自动启用 R2、KV、Workers AI 或付费套餐。Artifacts 的云端分享功能需要另行配置 KV；未配置时不提供该功能。对话记录默认保存在当前浏览器。

## 实现

- NextChat upstream: `1d3dc331512929a4b1d3e82354e72acce33b5c7a`
- Next.js: `15.5.29`
- OpenNext Cloudflare: `1.20.17`
- Wrangler: `4.163.0`
- 使用 Workers Custom Domain 自动配置域名及证书。
- 适配 Next.js 异步路由参数及 Workers 的 Node.js 兼容运行时。
- 移除上游 API Key 和访问码的明文日志。
- 依赖使用 `package-lock.json` 固定，构建阶段不接收 Cloudflare 部署 Token。

## 已完成的本地验证

- OpenNext 生产构建通过，未跳过类型检查或 lint。
- Wrangler 部署 dry run 通过：压缩后约 1 MB（1013.36 KiB），符合免费 Workers 的 3 MB 脚本限制。
- Workers 本地运行时检查通过：首页、静态资源缓存、公开配置接口及不合法代理/WebDAV/Upstash 请求的拒绝处理。
- 尚未连接真实模型 API，尚未部署到 Cloudflare 生产账户；生产发布需要上述两个 GitHub Secrets。

## 官方文档

- https://opennext.js.org/cloudflare/get-started
- https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/

Google Gemma 官方接口说明：https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api
