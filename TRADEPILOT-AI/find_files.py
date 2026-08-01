import os
import glob

directory = r"c:\Users\LENOVO\Desktop\Agentrix\TRADEPILOT-AI\frontend"
out = []
out.append("Searching for files...")
for root, dirs, files in os.walk(directory):
    if "index.html" in files:
        out.append(f"Found: {os.path.join(root, 'index.html')}")
    if "App.jsx" in files:
        out.append(f"Found: {os.path.join(root, 'App.jsx')}")
    if "main.jsx" in files:
        out.append(f"Found: {os.path.join(root, 'main.jsx')}")
    if "vite.config.js" in files:
        out.append(f"Found: {os.path.join(root, 'vite.config.js')}")
    if "index.css" in files:
        out.append(f"Found: {os.path.join(root, 'index.css')}")

with open(r"c:\Users\LENOVO\Desktop\Agentrix\TRADEPILOT-AI\search_results.txt", "w") as f:
    f.write("\n".join(out))
