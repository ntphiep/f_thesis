import multiprocessing
import subprocess
import time

# Hàm để chạy script với một tham số cụ thể
def run_script(suffix):
    subprocess.run(["python", "gen.py", suffix])  

start = 210
end = start + 10
pools = 100

suffixes = [f"{i:04d}" for i in range(start, end)]  

# Sử dụng multiprocessing để chạy 10 process song songl
with multiprocessing.Pool(pools) as pool:
    pool.map(run_script, suffixes)
 