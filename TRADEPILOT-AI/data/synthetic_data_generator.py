import os
import time
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":
    print("Warning: GEMINI_API_KEY is not set correctly in .env. The generation might fail.")

genai.configure(api_key=API_KEY)

# Define the prompts for different knowledge base documents
PROMPTS = {
    "knowledge_base/sample_cases/cinnamon_export.md": """
Act as the Sri Lanka Department of Import and Export Control. 
Write a formal circular detailing the export licensing requirements, mandatory phytosanitary certificates, 
and relevant authorities for exporting Cinnamon (HS Code 0906) to Dubai. 
Format it as a structured markdown document with sections for 'Applicable Goods', 'Required Permits', 'Procedures', and 'Authorities Involved'.
Make it look like an official Sri Lankan government document.
    """,
    "knowledge_base/sample_cases/electronics_import.md": """
Act as the Sri Lanka Customs Authority.
Write a formal customs guideline document detailing the import procedures, required approvals, 
and documentation for importing consumer electronic devices (HS Code 8543) into Sri Lanka.
Include details on Telecommunications Regulatory Commission (TRCSL) approval, standard customs duties, PAL (Ports and Airports Development Levy), and VAT.
Format it as a structured markdown document.
    """,
    "knowledge_base/import_export_control/general_licensing_rules.md": """
Act as the Sri Lanka Department of Import and Export Control.
Write a comprehensive guide on the General Import and Export Licensing Rules for SMEs in Sri Lanka.
Cover the process of obtaining an Import/Export License, the documents required (Business Registration, TIN certificate, Bank references), 
and the standard timeline for processing. Use markdown format.
    """,
    "knowledge_base/customs/duties_and_taxes_overview.md": """
Act as the Sri Lanka Customs Authority.
Write an overview document explaining the common duties and taxes applied to imports in Sri Lanka.
Explain Customs Import Duty (CID), Value Added Tax (VAT), Ports and Airports Development Levy (PAL), 
and CESS. Provide a brief explanation of how each is calculated. Format as markdown.
    """
}

def generate_synthetic_data():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    base_dir = Path(__file__).parent.parent
    
    for relative_path, prompt in PROMPTS.items():
        file_path = base_dir / relative_path
        
        # Ensure the parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating content for {relative_path}...")
        try:
            response = model.generate_content(prompt)
            content = response.text
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully wrote {file_path}")
            
            # Sleep to avoid rate limits
            time.sleep(2)
        except Exception as e:
            print(f"Failed to generate {relative_path}: {e}")

if __name__ == "__main__":
    generate_synthetic_data()
