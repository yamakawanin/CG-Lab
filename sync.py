import subprocess
import sys
import datetime
import os

def run(cmd):
    # 这里的 capture_output=True 是为了抓取错误信息
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return result.returncode == 0, result.stdout, result.stderr

def sync():
    # 1. 更新表格
    # 💡 已经将这里的 updata 改为了 update
    table_script = "update_table.py"
    
    if os.path.exists(table_script):
        print(f"正在运行 {table_script}...")
        # 使用 sys.executable 确保在虚拟环境下运行正确
        success, out, err = run(f'"{sys.executable}" {table_script}')
        if not success:
            print(f"表格更新失败: {err}")
    else:
        print(f"未找到 {table_script}，跳过此步。")

    # 2. Git 操作
    print("检查文件变动...")
    run("git add .")
    
    msg = sys.argv[1] if len(sys.argv) > 1 else f"auto sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    print(f"正在提交: {msg}")
    success, out, _ = run(f'git commit -m "{msg}"')
    
    if "nothing to commit" in out:
        print("无需提交（文件没有变动）。")
        return

    print(f"正在推送到 GitHub...")
    push_ok, _, err = run("git push")
    if push_ok:
        print("\n" + "="*20)
        print("同步成功！")
        print("="*20)
    else:
        print(f"推送失败: {err}")

if __name__ == "__main__":
    sync()