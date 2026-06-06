# ValueAlign · 价值对齐

个人价值偏好与全球共识碰撞——AI伦理个人报告

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

## 参考基准

- **Fjeld et al. (2020)** — Principled Artificial Intelligence: Mapping Consensus in Ethical and Rights-Based Approaches to Principles for AI. Harvard Berkman Klein Center.
  - 分析 36 份国际 AI 伦理准则，提炼 8 项核心原则及各原则出现频率
- **落地数据** — 基于 EU AI Act、斯坦福 AI Index Report、麦肯锡全球 AI 调研

## 部署到 Streamlit Cloud

1. 推送到 GitHub
2. 在 [Streamlit Cloud](https://streamlit.io/cloud) 新建 app
3. 在 Settings → Secrets 添加：
   ```toml
   api_key = "你的 DeepSeek API Key"
   ```

## 许可

MIT
