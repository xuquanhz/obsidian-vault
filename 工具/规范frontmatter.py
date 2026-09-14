# -*- coding: utf-8 -*-
"""
frontmatter 规范化（幂等，可重复运行）
用法：python 工具/规范frontmatter.py            # 预演，只打印将要改动的文件
      python 工具/规范frontmatter.py --apply    # 实际写入

原则：
  1. 只补缺失字段，绝不改写已有字段的值
  2. updated 取该文件的 git 最近提交日期（取不到才用文件修改时间），不虚构
  3. tags 缺失时按所在目录层级生成（目录名即分类），不臆造语义标签
  4. 完全不碰 .obsidian / copilot / PD2405 / .stversions 等目录
"""
import os
import re
import sys
import subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".obsidian", ".stversions", ".trash", ".git", ".claudian",
             "copilot", "PD2405", ".smart-env"}
# 不纳入自动规范的路径片段（原文类文档 / 敏感文件 / 临时文件 / 自动生成文件）
EXCLUDE = {"AI各种PAIKEY重要-1.md", "Windows同步测试.md", "体检报告.md"}

# 根目录笔记的标签修正（目录推断对根目录失效）
TAG_OVERRIDES = {
    "我的任务.md": ["任务"],
    "知识库首页.md": ["导航"],
    "学习个人知识库.md": ["导航"],
    "工作台.md": ["工作台"],
    "知识库体检.md": ["体检"],
    "白水知识库管理规范.md": ["规范"],
}

today = datetime.now().strftime("%Y-%m-%d")


def git_date(rel):
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", rel],
                           cwd=ROOT, capture_output=True, text=True, timeout=15)
        s = r.stdout.strip()
        if s:
            return s
    except Exception:
        pass
    return None


def guess_tags(rel):
    if rel in TAG_OVERRIDES:
        return TAG_OVERRIDES[rel]
    parts = rel.replace("\\", "/").split("/")[:-1]
    parts = [p for p in parts if p and p not in ("工作文件", "合同模板")]
    if not parts:
        return []
    return parts[-2:] if len(parts) >= 2 else parts


def yaml_tags(tags):
    if not tags:
        return "[]"
    clean = [t.replace("[", "").replace("]", "").replace(",", "").strip() for t in tags]
    return "[" + ", ".join(clean) + "]"


def process(path, apply_):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    if os.path.basename(rel) in EXCLUDE:
        return None
    raw = open(path, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig", errors="replace")

    if not text.lstrip().startswith("---"):
        # 完全没有 frontmatter
        mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
        upd = git_date(rel) or mtime
        title = os.path.basename(rel)[:-3]
        tags = guess_tags(rel)
        block = (f"---\ntitle: {title}\nupdated: {upd}\n"
                 f"tags: {yaml_tags(tags)}\nstatus: active\n---\n\n")
        new = block + text.lstrip("\n")
        if apply_:
            open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="").write(new)
        return ("新建", rel, f"title/updated({upd})/tags{tags}/status")

    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = parts[1]
    body = parts[2]

    add = []
    if not re.search(r"^title\s*:", fm, re.M):
        add.append(f"title: {os.path.basename(rel)[:-3]}")
    if not re.search(r"^updated\s*:", fm, re.M):
        mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d")
        upd = git_date(rel) or mtime
        add.append(f"updated: {upd}")
    if not re.search(r"^tags\s*:", fm, re.M):
        add.append(f"tags: {yaml_tags(guess_tags(rel))}")
    if not re.search(r"^status\s*:", fm, re.M):
        add.append("status: active")

    if not add:
        return None

    new_fm = fm.rstrip("\n") + "\n" + "\n".join(add) + "\n"
    new = "---" + new_fm + "---" + body
    if apply_:
        open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="").write(new)
    return ("补齐", rel, " / ".join(a.split(":")[0] for a in add))


def main():
    apply_ = "--apply" in sys.argv
    results = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fns:
            if not f.lower().endswith(".md"):
                continue
            r = process(os.path.join(dp, f), apply_)
            if r:
                results.append(r)

    a = [r for r in results if r[0] == "新建"]
    b = [r for r in results if r[0] == "补齐"]
    print(f"{'已写入' if apply_ else '预演'}：共 {len(results)} 篇")
    print(f"  · 新建完整 frontmatter：{len(a)} 篇")
    for _, rel, keys in a:
        print(f"      {rel}  ← {keys}")
    print(f"  · 补齐缺失字段：{len(b)} 篇")

    keep = []
    for _, rel, keys in b:
        if "title" in keys:
            keep.append((rel, keys))
    if keep:
        print(f"    （其中补 title 的 {len(keep)} 篇）")
        for rel, keys in keep:
            print(f"      {rel}  ← {keys}")
    if not apply_:
        print("\n加 --apply 才会实际写入。")


if __name__ == "__main__":
    main()
