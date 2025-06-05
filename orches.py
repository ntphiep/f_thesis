import multiprocessing
import subprocess

# Hàm để chạy script với một tham số cụ thể
def run_script(suffix):
    subprocess.run(["python", "clm.py", suffix])


suffixes = [f"{i:04d}" for i in range(34, 55)]  # tạo danh sách từ "0000" đến "2762"

# Sử dụng multiprocessing để chạy 10 process song song
with multiprocessing.Pool(20) as pool:
    pool.map(run_script, suffixes)
 
