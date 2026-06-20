import os
import time
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":
    raise ValueError("Valid GEMINI_API_KEY required for bulk generation.")

genai.configure(api_key=API_KEY)

PROMPTS = {
    # 1. Sample Cases
    "knowledge_base/sample_cases/tea_export_uk.md": """
Act as the Sri Lanka Tea Board. Write a formal compliance roadmap for exporting Ceylon Tea (HS Code 0902) to the United Kingdom.
Cover mandatory registrations, the Tea Board export permit, phytosanitary requirements, standard customs duties, and an estimated timeline. 
Format as a detailed markdown document.
    """,
    "knowledge_base/sample_cases/medical_device_import.md": """
Act as the National Medicines Regulatory Authority (NMRA) of Sri Lanka. 
Write a formal import guideline for Medical Devices (HS Code 9018).
Explain the NMRA registration process, necessary ISO 13485 certifications, import licensing, and import tax exemptions. Format as markdown.
    """,
    "knowledge_base/sample_cases/gemstone_export_usa.md": """
Act as the National Gem and Jewellery Authority of Sri Lanka.
Write the official procedure for exporting cut and polished gemstones (HS Code 7103) to the USA.
Detail the examination process by the Gem Authority, the export permit, the role of Sri Lanka Customs Gem Unit, and required documentation. Format as markdown.
    """,
    "knowledge_base/sample_cases/textile_import_china.md": """
Act as Sri Lanka Customs. Write a guideline for importing woven fabrics of cotton (HS Code 5208) from China.
Focus on the calculation of applicable tariffs (CID, VAT, PAL, CESS) and the documentation required to clear the shipment. Format as markdown.
    """,
    
    # 2. Import/Export Control
    "knowledge_base/import_export_control/prohibited_restricted_list.md": """
Act as the Department of Import and Export Control. Write the "2026 Restricted and Prohibited Items Guide".
List at least 5 strictly prohibited items (e.g., narcotics, specific hazardous chemicals) and 5 restricted items requiring special licenses (e.g., drones, specific agricultural goods). Format as markdown with clear headers.
    """,
    "knowledge_base/import_export_control/specialized_permits_guide.md": """
Act as a Trade Compliance Authority. Write a comprehensive "Specialized Permits Cross-Reference Guide".
Explain which specific authority handles which product categories: TRCSL (electronics), NMRA (pharmaceuticals), NPQS (plants/agriculture), Ministry of Defence (drones/security). Format as markdown.
    """,
    
    # 3. Customs Rules & Risks
    "knowledge_base/customs/common_risks_and_holds.md": """
Act as the Risk Management Directorate of Sri Lanka Customs.
Write a document titled "Common Causes for Customs Holds and Rejections".
Detail the top 5 reasons a shipment might be delayed: Valuation disputes (under-invoicing), HS Code misclassification, missing mandatory permits, incomplete documentation, and physical inspection triggers. Provide risk mitigation advice for SMEs. Format as markdown.
    """,
    "knowledge_base/customs/timeline_estimation_guide.md": """
Act as Sri Lanka Customs. Write a "Standard Clearance Timeline Estimation Guide".
Provide expected processing times for:
1. Green Channel clearance.
2. Yellow Channel (document check).
3. Red Channel (physical inspection).
4. Obtaining a TRCSL or NMRA permit prior to import.
Format as markdown.
    """,
    "knowledge_base/customs/comprehensive_tariff_schedule.md": """
Act as Sri Lanka Customs. Write a summary of the 2026 Tariff Schedule.
Provide the standard Customs Import Duty (CID) and PAL percentage bands for:
- Essential medical supplies
- Raw materials for manufacturing
- Consumer electronics
- Luxury vehicles
Explain how the total tax is compounded. Format as markdown.
    """
}

def run_bulk_generation():
    # Use gemini-2.5-flash as it's highly capable and fast
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    base_dir = Path(__file__).parent.parent
    
    for relative_path, prompt in PROMPTS.items():
        file_path = base_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Generating: {relative_path}")
        try:
            response = model.generate_content(prompt)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"  -> Success: {file_path}")
            time.sleep(3) # Rate limit protection
        except Exception as e:
            print(f"  -> Failed: {e}")

if __name__ == "__main__":
    print("Starting bulk synthetic data generation...")
    run_bulk_generation()
    print("Generation complete!")
