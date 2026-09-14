# -*- coding: utf-8 -*-
"""
白水知识库体检脚本
用法：在库根目录执行  python 工具/知识库体检.py
输出：重写 工具/体检报告.md

体检项（对应《白水知识库管理规范》§6）：
  1. 断链（[[ ]] 指向不存在的文件）
  2. frontmatter 覆盖率（title / updated / tags / status）
  3. 空笔记
  4. 孤儿笔记（无入链也无出链）
  5. 超期未更新
  6. 织网率（有互链的笔记占比）
"""
import os
import re
import sys
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = (".md", ".canvas", ".excalidraw", ".pdf", ".xlsx", ".docx", ".doc",
           ".jpg", ".jpeg", ".png", ".txt", ".pptx", ".xls", ".dwg")
SKIP_DIRS = {".obsidian", ".stversions", ".trash", ".git", ".claudian",
             "copilot", "PD2405", ".smart-env", ".space"}
STALE_DAYS = 180


def walk_notes():
    out = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fns:
            if f.lower().endswith(".md"):
                out.append(os.path.join(dp, f))
    return out


def build_index():
    """vault 内所有文件的多种写法（全路径 / 去扩展名 / 文件名）"""
    idx = set()
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fns:
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
            idx.add(rel.lower())
            idx.add(os.path.basename(rel).lower())
            if rel.lower().endswith(".md"):
                idx.add(rel[:-3].lower())
                idx.add(os.path.basename(rel)[:-3].lower())
    return idx


def strip_code(text):
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def split_frontmatter(text):
    if not text.lstrip().startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    return parts[1], parts[2]


def git_date(path):
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", path],
                           cwd=ROOT, capture_output=True, text=True, timeout=15)
        s = r.stdout.strip()
        return s if s else None
    except Exception:
        return None


def main():
    notes = walk_notes()
    idx = build_index()

    missing_fm, missing_keys, empty, no_link = [], [], [], []
    out_links, in_links = {}, {}
    broken = {}
    stale = []

    for p in notes:
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        try:
            text = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            try:
                text = open(p, encoding="gbk", errors="ignore").read()
            except Exception:
                continue

        if len(text.strip()) < 60:
            empty.append(rel)

        fm, body = split_frontmatter(text)
        if fm is None:
            missing_fm.append(rel)
        else:
            lack = [k for k in ("title", "updated", "tags", "status")
                    if not re.search(rf"^{k}\s*:", fm, re.M)]
            if lack:
                missing_keys.append((rel, lack, fm))

        clean = strip_code(body)
        links = []
        for raw in re.findall(r"\[\[(.+?)\]\]", clean):
            target = raw.split("|")[0].split("#")[0].strip().rstrip("\\").strip()
            if not target:
                continue
            links.append(target)
            if not target.lower().endswith(TARGETS):
                continue
            t = target.lower()
            if t in idx or os.path.basename(t) in idx:
                continue
            broken.setdefault(rel, []).append(target)

        out_links[rel] = set(links)
        if not links:
            no_link.append(rel)

        m = re.search(r"^updated\s*:\s*(\d{4}-\d{2}-\d{2})", fm or "", re.M)
        if m:
            try:
                d = datetime.strptime(m.group(1), "%Y-%m-%d")
                if (datetime.now() - d).days > STALE_DAYS:
                    stale.append((rel, m.group(1)))
            except ValueError:
                pass

    for rel, tgts in out_links.items():
        for t in tgts:
            b = os.path.basename(t)
            for other in notes:
                orel = os.path.relpath(other, ROOT).replace("\\", "/")
                oname = os.path.basename(orel)[:-3]
                if orel != rel and (t == oname or t == orel or b == oname or b == orel):
                    in_links.setdefault(orel, set()).add(rel)

    orphans = [r for r in out_links if r not in in_links and len(out_links.get(r, ())) == 0]
    wired = [r for r in notes
             if os.path.relpath(r, ROOT).replace("\\", "/") in in_links]
    wired_rate = len(wired) / max(1, len(notes)) * 100
    fm_rate = (len(notes) - len(missing_fm)) / max(1, len(notes)) * 100
    broken_total = sum(len(v) for v in broken.values())

    L = []
    A = L.append
    A("---")
    A("title: 体检报告")
    A(f"updated: {datetime.now().strftime('%Y-%m-%d')}")
    A("tags: [体检, 自动生成]")
    A("status: active")
    A("---")
    A("")
    A("# 🩺 知识库体检报告\n")
    A(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 扫描笔记：{len(notes)} 篇\n")
    A("## 总览\n")
    A("| 指标 | 数值 | 达标线 | 状态 |")
    A("|:--|--:|:--|:--|")
    A(f"| 断链 | {broken_total} 条 | 0 | {'✅' if broken_total == 0 else '❌'} |")
    A(f"| frontmatter 完整率 | {fm_rate:.1f}%（缺 {len(missing_fm)} 篇 / 字段不全 {len(missing_keys)} 篇） | ≥95% | {'✅' if fm_rate >= 95 else '⚠️'} |")
    A(f"| 空笔记 | {len(empty)} 篇 | 0 | {'✅' if not empty else '❌'} |")
    A(f"| 孤儿笔记 | {len(orphans)} 篇 | 持续下降 | {'✅' if not orphans else '⚠️'} |")
    A(f"| 织网率 | {wired_rate:.1f}% | ≥20% | {'✅' if wired_rate >= 20 else '⚠️'} |")
    A(f"| 超 {STALE_DAYS} 天未更新 | {len(stale)} 篇 | 季度复核 | ℹ️ |")

    A("\n## ① 断链\n")
    if not broken:
        A("无断链。✅")
    else:
        for k in sorted(broken):
            A(f"**{k}**")
            for t in dict.fromkeys(broken[k]):
                A(f"- `{t}`")
            A("")

    A("\n## ② 缺 frontmatter\n")
    A(f"完全缺失（{len(missing_fm)} 篇）：")
    for r in sorted(missing_fm):
        A(f"- {r}")
    A(f"\n字段不全（{len(missing_keys)} 篇）：")
    for r, lack, _ in sorted(missing_keys):
        A(f"- {r} —— 缺 {'/'.join(lack)}")

    A("\n## ③ 空笔记\n")
    for r in sorted(empty) or ["（无）"]:
        A(f"- {r}")

    A("\n## ④ 孤儿笔记（无入链亦无出链）\n")
    for r in sorted(orphans) or ["（无）"]:
        A(f"- {r}")

    A(f"\n## ⑤ 超 {STALE_DAYS} 天未更新\n")
    for r, d in sorted(stale, key=lambda x: x[1]) or [("（无）", "")]:
        A(f"- {d}　{r}")

    A("\n---\n")
    A("*由 `工具/知识库体检.py` 自动生成，请勿手工编辑。*")

    report = os.path.join(ROOT, "工具", "体检报告.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"体检完成：笔记 {len(notes)} 篇 ｜ 断链 {broken_total} 条 ｜ 缺 frontmatter {len(missing_fm)} 篇 ｜ 织网率 {wired_rate:.1f}%")
    print(f"报告已写入：{report}")


if __name__ == "__main__":
    sys.exit(main())
