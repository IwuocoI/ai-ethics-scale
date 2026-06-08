import streamlit as st, json, random, requests

st.set_page_config(page_title="ValueAlign", layout="centered")

VALUES = [
    {"id":"fairness","emoji":"⚖️","title":"公平与反歧视","desc":"算法不因种族、性别等因素歧视特定群体，需全生命周期偏差检测"},
    {"id":"privacy","emoji":"🔒","title":"隐私","desc":"个人对其数据拥有控制权，防止未经授权的访问或重识别"},
    {"id":"accountability","emoji":"📋","title":"可问责性","desc":"AI出事了有人负责，决策链路可追溯，受损时可申诉"},
    {"id":"transparency","emoji":"🔍","title":"透明与可解释性","desc":"利益相关者能理解AI决策逻辑，包括原理、数据和局限性"},
    {"id":"safety","emoji":"🛡️","title":"安全与网络安全","desc":"确保AI系统免受攻击、操纵和意外故障，贯穿全流程"},
    {"id":"human_control","emoji":"🤝","title":"人类控制技术","desc":"高风险场景保持自主监督，保留否决AI决策的最终权限"},
    {"id":"responsibility","emoji":"🎓","title":"专业责任","desc":"开发者恪守伦理义务，对职业标准与社会影响负责"},
    {"id":"human_values","emoji":"🌍","title":"促进人类价值","desc":"AI应增进人类福祉、创造力与公平，服务于人文繁荣"},
]
CONSENSUS = {"fairness":100,"privacy":97,"accountability":97,"transparency":94,"safety":81,"human_control":69,"responsibility":78,"human_values":69}
IMPLEMENTATION = {"fairness":2.5,"privacy":5.0,"accountability":4.0,"transparency":3.5,"safety":4.5,"human_control":2.0,"responsibility":2.5,"human_values":1.0}

# 落地程度详细原因
IMPL_REASON = {
    "fairness":"落地低（巨大反差）：虽有100%的口头政治正确，但斯坦福报告指出AI歧视事件激增，且技术上公平与性能存在冲突，企业普遍超配口号低配行动。",
    "privacy":"落地极高：有GDPR等法律强制力，企业有动力和成熟技术（如联邦学习）去保护数据。",
    "accountability":"落地高：EU AI Act强制规定了高风险AI必须有明确的法律责任主体承担代价。",
    "transparency":"落地中：法律有要求，但主流大模型在技术上很难做到真正的可解释性。",
    "safety":"落地高：企业最怕AI系统被黑客投毒或产生安全漏洞，技术上最容易被Benchmark量化测试。",
    "human_control":"落地极低：2026年是AI Agent大爆发的年份，技术正疯狂追求全自主免人工干预，与人类控制背道而驰。",
    "responsibility":"落地低：多依赖于工程师个人职业道德和企业自律，缺乏跨行业硬性审计标准。",
    "human_values":"完全悬空：纯粹的哲学和道德愿景，既无法律惩罚，技术上也无法通过代码进行任何量化测试。"
}

if "step" not in st.session_state: st.session_state.step = "welcome"
if "sorted_list" not in st.session_state: st.session_state.sorted_list = []
if "to_insert" not in st.session_state: st.session_state.to_insert = []
if "cur_new" not in st.session_state: st.session_state.cur_new = None
if "bin_lo" not in st.session_state: st.session_state.bin_lo = 0
if "bin_hi" not in st.session_state: st.session_state.bin_hi = 0
if "choices" not in st.session_state: st.session_state.choices = []
if "total_comparisons" not in st.session_state: st.session_state.total_comparisons = 0
if "dragged_ranking" not in st.session_state: st.session_state.dragged_ranking = None
if "active_card" not in st.session_state: st.session_state.active_card = None
if "analysis_cache" not in st.session_state: st.session_state.analysis_cache = {}

if st.session_state.step == "welcome":
    st.markdown("<div style='text-align:center;padding:80px 0 30px 0'><h1 style='font-size:24px;margin-bottom:8px'>个人价值偏好与全球共识碰撞</h1><p style='font-size:16px;color:#555'>——AI伦理个人报告 · 课程作业</p></div>", unsafe_allow_html=True)
    if st.button("📖 项目介绍", use_container_width=True):
        st.session_state.step = "intro"; st.rerun()
    st.markdown("<div style='text-align:center;font-size:11px;color:#aaa;margin-top:60px'>参考：Fjeld et al. 2020 · 哈佛伯克曼克莱因中心</div>", unsafe_allow_html=True)

elif st.session_state.step == "intro":
    ci1, ci2 = st.columns([3, 1])
    with ci1:
        st.markdown("<h2 style='font-size:20px;margin-bottom:12px'>📋 项目介绍</h2>", unsafe_allow_html=True)
    with ci2:
        if st.button("🚀 开始价值比较", use_container_width=True):
            order = list(range(8)); random.shuffle(order)
            st.session_state.sorted_list = [order[0]]; st.session_state.to_insert = order[1:]
            st.session_state.cur_new = None; st.session_state.bin_lo = 0; st.session_state.bin_hi = 1
            st.session_state.choices = []; st.session_state.total_comparisons = 0
            st.session_state.dragged_ranking = None; st.session_state.step = "pairwise"; st.rerun()
    st.markdown("**本项目做什么？**\n\n通过 8 项核心 AI 伦理原则的逐对比较，探索你的个人价值偏好与全球共识之间的差距。")
    st.markdown("**参考基准**\n- **全球共识数据**：Fjeld et al. (2020) 哈佛伯克曼克莱因中心，分析 36 份国际 AI 伦理准则\n- **落地程度数据**：基于 EU AI Act、斯坦福 AI Index Report、麦肯锡全球 AI 调研")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown("**① 价值比较**\n自适应逐对比较")
    with c2: st.markdown("**② 排序确认**\n调整最终优先级")
    with c3: st.markdown("**③ 生成报告**\n对比共识与落地")
    st.markdown("<h3 style='font-size:16px;margin:0 0 8px 0'>📚 核心数据来源</h3>", unsafe_allow_html=True)
    st.markdown("本项目关于 AI 治理与伦理框架的核心数据，源自哈佛大学伯克曼·克莱恩中心发布的里程碑式白皮书《Principled Artificial Intelligence: Mapping Consensus in Ethical and Rights-based Approaches to Principles for AI》。作为全球 AI 治理领域的奠基性与地缘性文献，该研究通过对全球五大主体（政府、企业、公民社会等）的 36 份权威 AI 原则文件进行全景式深度分析，首次以量化和可视化方式确立了全球在隐私、问责及“公平与非歧视”等 8 大核心伦理主题上的顶层规范共识，其研究结论被联合国、欧盟、OECD 等多方广泛引用，具有极高的国际公信力，为本项目提供了坚实的合规理论支撑与国际标准参照。")
    st.markdown("【官方文献主页】<a href='https://dash.harvard.edu/entities/story/e7033f70-5e9b-484f-af0f-0d8b2fb2cd75' target='_blank'>Harvard DASH - Principled Artificial Intelligence</a>", unsafe_allow_html=True)
    st.markdown("---")

elif st.session_state.step == "pairwise":
    st.markdown("<style>.stButton>button{height:320px!important;padding:30px 10px!important}.stButton>button p{font-size:14px!important;line-height:1.4!important;text-align:center!important;white-space:pre-wrap!important}.stButton>button{max-width:300px!important;margin:0 auto}@media(min-width:641px){.stButton{display:flex;justify-content:center}div[data-testid='stHorizontalBlock']{justify-content:center!important;gap:24px!important}div[data-testid='stColumn']{flex:0 1 auto!important;width:300px!important;min-width:0!important;padding:0!important}}@media(max-width:640px){div[data-testid='stHorizontalBlock']{flex-wrap:nowrap!important;column-gap:0!important;justify-content:center!important}div[data-testid='stColumn']{flex:0 0 auto!important;max-width:50%!important;min-width:0!important;padding:0!important}.stButton>button{width:150px!important;min-width:150px!important;max-width:150px!important;height:240px!important;padding:14px 4px!important}.stButton>button p{font-size:13px!important}}</style>", unsafe_allow_html=True)
    s = st.session_state
    if s.cur_new is None and s.to_insert:
        s.cur_new = s.to_insert.pop(0); s.bin_lo = 0; s.bin_hi = len(s.sorted_list)
    if s.cur_new is None and not s.to_insert:
        st.session_state.ranking = list(reversed(s.sorted_list)); st.session_state.step = "drag"; st.rerun()
    if s.cur_new is not None:
        mid = (s.bin_lo + s.bin_hi) // 2
        a, b = VALUES[s.cur_new], VALUES[s.sorted_list[mid]]
        st.markdown("<div style='text-align:center;margin-bottom:12px'><h2 style='font-size:20px;margin-bottom:4px'>⚖️ 价值比较</h2><p style='font-size:14px;color:#666'>选一个你认为更重要的原则。</p></div>", unsafe_allow_html=True)
        st.progress((len(s.sorted_list)-1)/7, text=f"已排 {len(s.sorted_list)}/8 项")
        c1,c2 = st.columns(2)
        with c1:
            if st.button(f"{a['emoji']}\n\n**{a['title']}**\n\n{a['desc']}", key=f"c_{s.total_comparisons}_a"):
                s.choices.append({"winner":s.cur_new,"loser":s.sorted_list[mid]}); s.total_comparisons += 1
                s.bin_lo = mid+1
                if s.bin_lo >= s.bin_hi: s.sorted_list.insert(s.bin_lo,s.cur_new); s.cur_new = None
                st.rerun()
        with c2:
            if st.button(f"{b['emoji']}\n\n**{b['title']}**\n\n{b['desc']}", key=f"c_{s.total_comparisons}_b"):
                s.choices.append({"winner":s.sorted_list[mid],"loser":s.cur_new}); s.total_comparisons += 1
                s.bin_hi = mid
                if s.bin_lo >= s.bin_hi: s.sorted_list.insert(s.bin_lo,s.cur_new); s.cur_new = None
                st.rerun()

elif st.session_state.step == "drag":
    st.markdown("<style>.stButton>button{height:60px!important;padding:4px 8px!important}.stButton>button p{font-size:13px!important;text-align:center!important}.btns-row{display:flex;gap:8px}@media(max-width:640px){div[data-testid='stHorizontalBlock']{flex-wrap:nowrap!important;column-gap:0!important}div[data-testid='stColumn']{padding:0 2px!important;margin:0!important;min-width:0!important;word-break:break-word!important}div[data-testid='stColumn']:nth-child(3) .stButton>button,div[data-testid='stColumn']:nth-child(4) .stButton>button{height:30px!important;width:36px!important;min-width:36px!important;max-width:36px!important;padding:0!important}.btns-row{flex-direction:column;align-items:center}.btns-row .stButton{width:100%!important}}</style>", unsafe_allow_html=True)
    cd1, cd2 = st.columns([2, 1])
    with cd1:
        st.markdown("<h2 style='font-size:20px;margin-bottom:4px'>📋 确认你的排序</h2><p style='font-size:14px;color:#666'>调整优先级，越靠上越重要。</p>", unsafe_allow_html=True)
    with cd2:
        st.markdown("<div class='btns-row'>", unsafe_allow_html=True)
        if st.button("← 重新比较", use_container_width=True):
            order = list(range(8)); random.shuffle(order)
            st.session_state.sorted_list=[order[0]]; st.session_state.to_insert=order[1:]
            st.session_state.cur_new=None; st.session_state.bin_lo=0; st.session_state.bin_hi=1
            st.session_state.choices=[]; st.session_state.total_comparisons=0
            st.session_state.step="pairwise"; st.rerun()
        if st.button("📊 生成报告", use_container_width=True):
            st.session_state.final_ranking=st.session_state.dragged_ranking; st.session_state.step="report"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    if st.session_state.dragged_ranking is None: st.session_state.dragged_ranking = list(st.session_state.ranking)
    rk = st.session_state.dragged_ranking
    for i, vi in enumerate(rk):
        v = VALUES[vi]
        ce,ct,cu,cd = st.columns([1,4,1,1])
        with ce: st.markdown(f"<div style='font-size:28px;line-height:1;padding-top:8px;text-align:center'>{v['emoji']}</div>", unsafe_allow_html=True)
        with ct: st.markdown(f"<div style='font-weight:600;font-size:15px;padding-top:8px'>{v['title']}</div><div style='font-size:11px;color:#888'>{v['desc'][:40]}…</div>", unsafe_allow_html=True)
        with cu:
            if i > 0 and st.button("↑", key=f"u_{i}"):
                rk[i-1],rk[i]=rk[i],rk[i-1]; st.session_state.dragged_ranking=rk; st.rerun()
        with cd:
            if i < len(rk)-1 and st.button("↓", key=f"d_{i}"):
                rk[i],rk[i+1]=rk[i+1],rk[i]; st.session_state.dragged_ranking=rk; st.rerun()

elif st.session_state.step == "report":
    ranking = st.session_state.ranking
    user_order = {VALUES[i]["id"]: p for p,i in enumerate(ranking)}
    sorted_by_con = sorted(VALUES, key=lambda v: -CONSENSUS[v["id"]])
    con_order = {v["id"]: i for i,v in enumerate(sorted_by_con)}
    d2 = sum((user_order[v["id"]]-con_order[v["id"]])**2 for v in VALUES)
    sim = max(0,min(100,round((1-6*d2/(8*(64-1))+1)/2*100)))

    st.markdown("<div style='text-align:center;margin-bottom:20px'><h2 style='font-size:20px;margin-bottom:4px'>📋 你的 AI 伦理报告</h2></div>", unsafe_allow_html=True)
    cl,cr = st.columns(2)
    with cl:
        st.markdown("**🧑 你的排序**")
        for i,idx in enumerate(ranking):
            v=VALUES[idx]
            st.markdown(f"<div style='display:flex;align-items:center;gap:8px;padding:8px 10px;margin-bottom:5px;background:{['#1a1a2e','#2d2d4e','#40406e','#53538e','#6666ae','#7979ce','#8c8cee','#9f9fff'][i]};border-radius:8px;color:#fff;height:36px'><span style='font-size:13px;font-weight:700;opacity:0.7;width:18px'>{i+1}</span><span style='font-size:18px;width:28px;text-align:center'>{v['emoji']}</span><span style='font-size:13px;font-weight:500'>{v['title']}</span></div>", unsafe_allow_html=True)
    with cr:
        st.markdown("**📊 全球共识**")
        for v in sorted_by_con:
            con,imp=CONSENSUS[v["id"]],IMPLEMENTATION[v["id"]]
            cc="#22c55e" if con>=90 else "#eab308" if con>=70 else "#ef4444"
            ic="#22c55e" if imp>=4 else "#eab308" if imp>=2.5 else "#ef4444"
            st.markdown(f"<div style='display:flex;align-items:center;gap:6px;padding:8px 10px;margin-bottom:5px;background:#f5f5f5;border-radius:8px;height:36px'><span style='font-size:16px;width:28px;text-align:center'>{v['emoji']}</span><span style='flex:1;font-size:13px'>{v['title']}</span><span style='color:{cc};font-weight:600;font-size:13px;width:40px;text-align:right'>{con}%</span><span style='color:{ic};font-weight:600;font-size:12px;width:55px;text-align:right'>落地{imp}/5</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    gaps=sorted([(v,user_order[v["id"]]+1-con_order[v["id"]]) for v in VALUES],key=lambda x:-abs(x[1]))
    bg_v,bg_gap=gaps[0]
    bg_ur,bg_cr=user_order[bg_v["id"]]+1,con_order[bg_v["id"]]+1
    sim_c="#22c55e" if sim>=60 else "#eab308" if sim>=40 else "#ef4444"
    st.markdown(f"<div style='display:flex;align-items:center;background:{'#f0fdf4' if sim>=60 else '#fefce8' if sim>=40 else '#fef2f2'};border-radius:12px;padding:16px 20px'><div style='flex:1;text-align:center'><div style='font-size:14px;color:#888;margin-bottom:4px'>排序相似度</div><div style='font-size:42px;font-weight:700;color:{sim_c}'>{sim}%</div></div><div style='width:1px;height:60px;background:#ddd'></div><div style='flex:1;text-align:center'><div style='font-size:13px;color:#555'>最大分歧：<b>{bg_v['title']}</b></div><div style='font-size:12px;color:#888;margin-top:4px'>你第{bg_ur}名 · 共识第{bg_cr}名 · 差{abs(bg_gap)}位</div></div></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Three cards as st.button
    top_v,last_v=VALUES[ranking[0]],VALUES[ranking[-1]]
    st.markdown("<div style='text-align:center;font-size:16px;font-weight:700;margin:12px 0 8px 0'>点击下面三张卡片可展开具体分析</div>", unsafe_allow_html=True)
    st.markdown("<style>.cb{height:140px!important;border:2px solid #e0e0e0!important;border-radius:12px!important;background:#fff!important;padding:12px 8px!important;text-align:center!important;box-shadow:0 1px 3px rgba(0,0,0,.06)!important}.cb:hover{border-color:#6c63ff!important;background:#f8f7ff!important}.cb p{font-size:12px!important;text-align:center!important;white-space:pre-wrap!important;line-height:1.3!important}</style>", unsafe_allow_html=True)
    ca,cb,cc = st.columns(3)
    with ca:
        if st.button(f"🥇 首位价值\n\n{top_v['emoji']}\n\n**{top_v['title']}**\n\n共识{CONSENSUS[top_v['id']]}% 落地{IMPLEMENTATION[top_v['id']]}/5", key="bt_top", use_container_width=True):
            st.session_state.active_card = "top" if st.session_state.active_card!="top" else None; st.rerun()
    with cb:
        if st.button(f"🔻 末位价值\n\n{last_v['emoji']}\n\n**{last_v['title']}**\n\n共识{CONSENSUS[last_v['id']]}% 落地{IMPLEMENTATION[last_v['id']]}/5", key="bt_last", use_container_width=True):
            st.session_state.active_card = "last" if st.session_state.active_card!="last" else None; st.rerun()
    with cc:
        if st.button(f"⚡ 显著差异\n\n📊\n\n**{bg_v['title']}**\n\n差{abs(bg_gap)}位", key="bt_gap", use_container_width=True):
            st.session_state.active_card = "gap" if st.session_state.active_card!="gap" else None; st.rerun()

    if st.session_state.active_card:
        st.markdown("---")
        ck = st.session_state.active_card
        rank_t = "\n".join(f"{i+1}. {VALUES[idx]['title']}" for i,idx in enumerate(ranking))

        if ck in st.session_state.analysis_cache:
            st.markdown(f"<div style='background:#f9f9f9;border-radius:12px;padding:20px;line-height:1.7;font-size:14px'>{st.session_state.analysis_cache[ck]}</div>", unsafe_allow_html=True)
        else:
            st.info("🤖 正在生成分析…")
            if ck == "top":
                sp = f"""你是一位AI伦理分析师，为用户的个人AI伦理价值报告生成分析文本。

背景：用户完成了8项AI伦理原则的价值排序测试。Fjeld et al.(2020)哈佛研究分析了36份国际AI伦理准则，统计了每项原则的出现频率（全球共识百分比）。落地程度（1-5分）基于EU AI Act、斯坦福AI Index Report、麦肯锡全球AI调研，反映该原则在实际法律和技术层面的执行情况。

用户完整排序：
{rank_t}

请分析第一项「{top_v['title']}」。
1. 解释这项原则的含义：{top_v['desc']}
2. 用户将其排在第一，可能反映了用户什么样的伦理偏好或价值取向？
3. 引用数据：Fjeld(2020)研究显示{CONSENSUS[top_v['id']]}%的伦理框架将其列为必要项。
4. 目前落地程度为{IMPLEMENTATION[top_v['id']]}/5分。{IMPL_REASON[top_v['id']]}

语言简洁流畅，100字左右，直接输出。"""
            elif ck == "last":
                sp = f"""你是一位AI伦理分析师，为用户的个人AI伦理价值报告生成分析文本。

背景：用户完成了8项AI伦理原则的价值排序测试。Fjeld et al.(2020)哈佛研究分析了36份国际AI伦理准则，统计了每项原则的出现频率（全球共识百分比）。落地程度（1-5分）基于EU AI Act、斯坦福AI Index Report、麦肯锡全球AI调研。

用户完整排序：
{rank_t}

请分析末位项「{last_v['title']}」。
1. 解释这项原则的含义
2. 用户将其排在最后，可能反映了用户什么样的伦理偏好或权衡？
3. 引用数据：Fjeld(2020)显示{CONSENSUS[last_v['id']]}%的伦理框架将其列为必要项。
4. 目前落地程度为{IMPLEMENTATION[last_v['id']]}/5分。{IMPL_REASON[last_v['id']]}

语言简洁流畅，100字左右，直接输出。"""
            else:
                sp = f"""你是一位AI伦理分析师，为用户的个人AI伦理价值报告生成分析文本。

背景：用户完成了8项AI伦理原则的价值排序测试。Fjeld et al.(2020)哈佛研究分析了36份国际AI伦理准则，统计了每项原则的出现频率（全球共识百分比）。落地程度（1-5分）基于EU AI Act、斯坦福AI Index Report、麦肯锡全球AI调研。

用户完整排序：
{rank_t}

用户排序与全球共识的相似度为{sim}%。最大差异出现在「{bg_v['title']}」：用户将其排在第{bg_ur}名，而全球共识排在第{bg_cr}名，差距{abs(bg_gap)}位。

{IMPL_REASON[bg_v['id']]}

分析这一差异的可能原因及含义。100字左右，直接输出。"""
            try:
                ak=st.secrets["api_key"]
                r=requests.post("https://api.deepseek.com/v1/chat/completions",
                    headers={"Content-Type":"application/json","Authorization":f"Bearer {ak}"},
                    json={"model":"deepseek-v4-flash","messages":[{"role":"user","content":sp}],"max_tokens":300,"temperature":0.4},
                    timeout=30)
                if r.status_code==200:
                    txt=r.json()["choices"][0]["message"]["content"]
                    st.session_state.analysis_cache[ck]=txt
                    st.markdown(f"<div style='background:#f9f9f9;border-radius:12px;padding:20px;line-height:1.7;font-size:14px'>{txt}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"API错误: {r.status_code}")
            except Exception as e:
                st.error(f"出错了: {e}")

    st.markdown("---")
    _,c2,_=st.columns(3)
    with c2:
        if st.button("🔄 重新测试", use_container_width=True):
            for k in ["step","sorted_list","to_insert","cur_new","bin_lo","bin_hi","choices","total_comparisons","dragged_ranking","active_card","analysis_cache"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()