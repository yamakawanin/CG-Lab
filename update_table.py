import os
import re

def get_experiment_title(work_dir):
    """提取子目录 README.md 的一级标题并清洗前缀"""
    readme_path = os.path.join(work_dir, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# "):
                        title = line.replace("# ", "").strip()
                        # 清洗前缀：Work0:, 实验一:, Exp 1. 等
                        clean_title = re.sub(
                            r'^(Work|实验|Exp|Project|Task|作业)\s*[\d一二三四五六七八九十]+\s*[:：.\- ]\s*', 
                            '', title, flags=re.IGNORECASE
                        ).strip()
                        return clean_title if clean_title else title
        except Exception as e:
            return f"读取失败({e})"
    return "未知实验"

def generate_table():
    """生成 Markdown 表格"""
    src_dir = "src"
    if not os.path.exists(src_dir):
        return "| 错误 | src 目录不存在 |"

    # 获取 WorkX 文件夹并按数值排序
    works = [d for d in os.listdir(src_dir) if d.startswith("Work") and os.path.isdir(os.path.join(src_dir, d))]
    works.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)

    table_lines = [
        "| 实验阶段 | 目录编号 | 实验名称 | 源码文档链接 |",
        "| :--- | :--- | :--- | :--- |"
    ]

    cn_nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", 
               "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]

    for i, work in enumerate(works):
        title = get_experiment_title(os.path.join(src_dir, work))
        rel_path = f"./src/{work}/README.md"
        # i=0 对应 实验一
        label = cn_nums[i] if i < len(cn_nums) else str(i + 1)
        table_lines.append(f"| **实验{label}** | `{work}` | {title} | [查看源码]({rel_path}) |")

    # 自动生成的待开发占位
    next_idx = len(works)
    next_label = cn_nums[next_idx] if next_idx < len(cn_nums) else str(next_idx + 1)
    table_lines.append(f"| **实验{next_label}** | `Work{next_idx}` | 待开发项目 | `即将开启...` |")
    
    return "\n".join(table_lines)

def update_root_readme(new_table):
    """更新根目录 README.md"""
    readme_file = "README.md"
    if not os.path.exists(readme_file):
        print("未找到 README.md")
        return

    with open(readme_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配标记位之间的内容
    pattern = r"(## 实验进度表\s*\n+)([\s\S]*?)(\n---|\n##|$)"
    if re.search(pattern, content):
        new_content = re.sub(pattern, r"\1" + new_table + r"\n\3", content)
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README 进度表已更新。")
    else:
        print("未找到 '## 实验进度表' 标记位。")

if __name__ == "__main__":
    update_root_readme(generate_table())