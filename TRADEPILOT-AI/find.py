import os

directory = r"c:\Users\LENOVO\Desktop\Agentrix\TRADEPILOT-AI"
out = []
for root, dirs, files in os.walk(directory):
    if "App.jsx" in files:
        out.append(os.path.join(root, "App.jsx"))
    if "vite.config.js" in files:
        out.append(os.path.join(root, "vite.config.js"))
    if "index.html" in files:
        out.append(os.path.join(root, "index.html"))

with open(r"c:\Users\LENOVO\Desktop\Agentrix\TRADEPILOT-AI\found.txt", "w") as f:
    f.write("\n".join(out))
