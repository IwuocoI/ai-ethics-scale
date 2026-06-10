# AI 伦理天平 (AI Ethics Scale)

一个轻量级的个人 AI 伦理偏好测量工具。通过迫选法两两比较，量化用户对八项核心 AI 伦理原则的偏好排序，并与全球共识及产业落地数据进行对比分析。

## 功能

- **自适应两两比较** — 将八项原则随机配对，用户逐一选择更看重的一项，基于二分插入排序算法逐步收敛至完整排序，仅需 13–17 次比较
- **动态排序微调** — 生成初步优先级列表后，支持手动上移/下移微调
- **多维共识对比** — 利用 Spearman 秩相关系数计算用户排序与哈佛全球共识提及率（基准 A）、欧盟 AI 法案及斯坦福 AI 指数评分（基准 B）的相似度，并识别最大分歧项
- **智能诊断报告** — 调用大语言模型 API，根据用户排序与分歧项生成个性化分析文本

## 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开 http://localhost:8501

## 项目结构

```
app.py                  # 主程序（Streamlit）
requirements.txt        # 依赖
.streamlit/secrets.toml # API Key（本地，不提交）
```

## 部署

在线体验：[https://ai-ethics-scale.streamlit.app/](https://ai-ethics-scale.streamlit.app/)

推送到 GitHub 后可在 Streamlit Cloud 直接部署，需在 Secrets 中配置：

```toml
api_key = "你的 DeepSeek API Key"
```

## 参考基准

- **Fjeld et al. (2020)** — Principled Artificial Intelligence: Mapping Consensus in Ethical and Rights-Based Approaches to Principles for AI. Harvard Berkman Klein Center.
  - 分析 36 份国际 AI 伦理准则，提炼 8 项核心原则及各原则出现频率
- **EU AI Act、斯坦福 AI Index Report、麦肯锡全球 AI 调研**

## 许可

MIT
