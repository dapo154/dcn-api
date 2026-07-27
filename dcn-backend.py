
import shutil

# Create ZIP of dcn-app
app_dir = '/mnt/agents/output/dcn-app'
zip_output = '/mnt/agents/output/dcn-app.zip'

shutil.make_archive(zip_output.replace('.zip', ''), 'zip', app_dir)

# Also create ZIP of the backend
backend_dir = '/mnt/agents/output/dcn-ai-video-backend'
backend_zip = '/mnt/agents/output/dcn-backend.zip'

if os.path.exists(backend_dir):
    shutil.make_archive(backend_zip.replace('.zip', ''), 'zip', backend_dir)
    print("Backend ZIP created")

print(f"App ZIP size: {os.path.getsize(zip_output) / 1024:.1f} KB")
print("ZIP files ready for download!")
