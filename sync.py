import subprocess
import sys
import datetime
import os

def run(cmd):
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.returncode == 0, result.stdout, result.stderr

def sync():
    # 1. 更新表格 (使用当前解释器运行)
    if os.path.exists("updata_table.py"):
        print("正在同步 README 表格...")
        run(f'"{sys.executable}" updata_table.py')

    # 2. Git 操作
    print("检查文件变动...")
    run("git add .")
    
    msg = sys.argv[1] if len(sys.argv) > 1 else f"auto sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    success, out, _ = run(f'git commit -m "{msg}"')
    if "nothing to commit" in out:
        print("无需提交。")
        return

    print(f"推送到 GitHub: {msg}")
    push_ok, _, err = run("git push")
    if push_ok:
        print("同步成功！")
    else:
        print(f"推送失败: {err}")

if __name__ == "__main__":
    sync()