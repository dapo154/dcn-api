
import os

app_dir = '/mnt/agents/output/dcn-app'
os.makedirs(app_dir, exist_ok=True)
os.makedirs(f'{app_dir}/src', exist_ok=True)
os.makedirs(f'{app_dir}/src/components', exist_ok=True)
os.makedirs(f'{app_dir}/src/screens', exist_ok=True)
os.makedirs(f'{app_dir}/src/navigation', exist_ok=True)
os.makedirs(f'{app_dir}/src/services', exist_ok=True)
os.makedirs(f'{app_dir}/src/store', exist_ok=True)
os.makedirs(f'{app_dir}/src/utils', exist_ok=True)
os.makedirs(f'{app_dir}/src/hooks', exist_ok=True)
os.makedirs(f'{app_dir}/assets', exist_ok=True)

print("DCN app directory structure created")
