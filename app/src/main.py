from datetime import datetime
import psutil
import os

# Function to get the current memory usage of the process
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # in bytes


start=datetime.now()
start_memory = get_memory_usage()
print("Hello, World!")
end=datetime.now()
end_memory = get_memory_usage()

print(round((end-start).total_seconds() * 1000))

memory_usage_mb = (end_memory - start_memory) / (1024 * 1024)  # in megabytes
print(f"Memory usage: {memory_usage_mb:.2f} MB")

print(f"{os.path.dirname(__file__)}")

