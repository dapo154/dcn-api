
import shutil
import os

# Create ZIP of the dcn-app
app_dir = '/mnt/agents/output/dcn-app'
zip_path = '/mnt/agents/output/dcn-app'

# Check if directory exists and has files
if os.path.exists(app_dir):
    files = []
    for root, dirs, filenames in os.walk(app_dir):
        for f in filenames:
            files.append(os.path.join(root, f))
    print(f"Found {len(files)} files in dcn-app:")
    for f in files[:20]:
        print(f"  {f.replace(app_dir, '')}")
    if len(files) > 20:
        print(f"  ... and {len(files)-20} more")
else:
    print("dcn-app directory not found")
