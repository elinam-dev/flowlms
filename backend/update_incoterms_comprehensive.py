import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.getenv('DB_NAME', 'flowitec_lms')]

def update_incoterms_comprehensive():
    # Find and update the Incoterms course
    incoterms_course = db.courses.find_one({"title": "Introduction to International and Commercial Terms (Incoterms)"})
    if incoterms_course:
        module = db.modules.find_one({"course_id": incoterms_course["id"]})
        if module:
            # Delete existing lessons
            db.lessons.delete_many({"module_id": module["id"]})
            
            # Create comprehensive lessons
            lessons = [
                {
                    "title": "Course Overview & Objectives",
                    "content": '''<div class="lesson-content">
<h1>📘 MASTER COURSE</h1>
<h2>International Commercial Terms (Incoterms® 2020) & Sea Freight Law</h2>
<h3>With Legal Frameworks: Ghana, Nigeria & Kenya</h3>

<div class="course-info">
<h3>COURSE OVERVIEW</h3>
<p><strong>Course Level:</strong> Advanced Professional / Executive</p>

<h4>Target Audience:</h4>
<ul>
<li>Import & Export Managers</li>
<li>Freight Forwarders</li>
<li>Supply Chain Professionals</li>
<li>Legal & Compliance Officers</li>
<li>Procurement Managers</li>
<li>Trade Finance Officers</li>
<li>Maritime & Port Professionals</li>
</ul>

<p><strong>Duration:</strong> 8–10 Hours (Self-paced LMS format)</p>

<h4>Course Objectives</h4>
<p>By the end of this course, learners will be able to:</p>
<ol>
<li>Explain the purpose and structure of Incoterms® 2020</li>
<li>Correctly apply each Incoterm in commercial contracts</li>
<li>Distinguish between risk transfer and cost allocation</li>
<li>Apply Incoterms in sea freight operations</li>
<li>Identify required shipping documents and compliance procedures</li>
<li>Understand maritime and shipping law frameworks in Ghana, Nigeria, and Kenya</li>
<li>Mitigate legal and commercial risk in international trade</li>
</ol>
</div>
</div>'''
                },
                {
                    "title": "What Are Incoterms?",
                    "content": '''<div class="lesson-content">
<h2>MODULE 1: Foundations of International Trade & Incoterms</h2>

<h3>1.1 What Are Incoterms?</h3>
<p>Incoterms (International Commercial Terms) are standardized trade terms published by the International Chamber of Commerce (ICC). They define:</p>
<ul>
<li>Who pays for what</li>
<li>When risk transfers from seller to buyer</li>
<li>Who arranges transport</li>
<li>Who arranges insurance</li>
<li>Who clears goods for export/import</li>
</ul>

<div class="important-note">
<h4>Important:</h4>
<p>Incoterms DO NOT govern:</p>
<ul>
<li>Transfer of ownership/title</li>
<li>Payment terms</li>
<li>Contract validity</li>
<li>Dispute resolution</li>
<li>Product quality</li>
</ul>
<p><strong>They strictly regulate delivery obligations.</strong></p>
</div>
</div>'''
                },
                {
                    "title": "Why Incoterms Matter in Africa",
                    "content": '''<div class="lesson-content">
<h3>1.2 Why Incoterms Matter in Africa</h3>
<p>In African trade corridors (e.g., Tema, Lagos, Mombasa), poor use of Incoterms results in:</p>
<ul>
<li>Port demurrage charges</li>
<li>Customs penalties</li>
<li>Delayed cargo clearance</li>
<li>Insurance disputes</li>
<li>Double freight payments</li>
<li>Cargo abandonment</li>
</ul>
<p><strong>Understanding Incoterms reduces commercial exposure and strengthens negotiation power.</strong></p>

<h3>1.3 Structure of Incoterms 2020</h3>
<p>There are 11 Incoterms divided into:</p>

<div class="terms-section">
<h4>A. Terms for Any Mode of Transport</h4>
<ul>
<li>EXW</li>
<li>FCA</li>
<li>CPT</li>
<li>CIP</li>
<li>DAP</li>
<li>DPU</li>
<li>DDP</li>
</ul>

<h4>B. Sea & Inland Waterway Only</h4>
<ul>
<li>FAS</li>
<li>FOB</li>
<li>CFR</li>
<li>CIF</li>
</ul>
</div>

<div class="warning">
<p><strong>Warning:</strong> Sea-specific terms should NOT be used for containerized shipments where the seller hands goods to a terminal before loading.</p>
</div>
</div>'''
                },
                {
                    "title": "EXW & FCA Terms",
                    "content": '''<div class="lesson-content">
<h2>MODULE 2: Detailed Breakdown of Each Incoterm</h2>

<h3>2.1 EXW – Ex Works</h3>
<div class="term-breakdown">
<h4>Seller Responsibility:</h4>
<ul><li>Make goods available at their premises</li></ul>

<h4>Buyer Responsibility:</h4>
<ul>
<li>Loading</li>
<li>Export clearance</li>
<li>Freight</li>
<li>Insurance</li>
<li>Import clearance</li>
<li>All risks from seller's premises</li>
</ul>

<h4>Risk Transfers:</h4>
<p>At seller's warehouse.</p>

<div class="african-risk">
<h4>Practical African Risk:</h4>
<p>In Ghana or Nigeria, export clearance often requires local tax IDs and regulatory approvals. Foreign buyers cannot easily handle export clearance — making EXW risky.</p>
<p><strong>Best Practice:</strong> Avoid EXW in African exports. Prefer FCA.</p>
</div>
</div>

<h3>2.2 FCA – Free Carrier</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Delivers goods to carrier</li>
<li>Handles export clearance</li>
</ul>

<h4>Risk Transfers:</h4>
<p>When goods handed to carrier.</p>

<p><strong>Recommended for:</strong> Containerized shipments.</p>

<div class="common-misuse">
<p><strong>Common Misuse:</strong> Many exporters wrongly use FOB for container cargo.</p>
</div>
</div>
</div>'''
                },
                {
                    "title": "Sea Freight Terms: FAS & FOB",
                    "content": '''<div class="lesson-content">
<h3>2.3 FAS – Free Alongside Ship</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Places goods alongside vessel</li>
<li>Handles export clearance</li>
</ul>

<h4>Risk Transfers:</h4>
<p>When goods placed next to vessel.</p>

<p><strong>Used for:</strong> Bulk cargo (grain, oil, minerals).</p>
</div>

<h3>2.4 FOB – Free on Board</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Loads goods on vessel</li>
<li>Handles export clearance</li>
</ul>

<h4>Risk Transfers:</h4>
<p>Once goods are onboard vessel.</p>

<p><strong>Used for:</strong> Non-containerized sea freight.</p>

<div class="risk-warning">
<p><strong>Risk:</strong> If goods damaged before loading, seller liable.</p>
</div>
</div>
</div>'''
                },
                {
                    "title": "CFR & CIF Terms",
                    "content": '''<div class="lesson-content">
<h3>2.5 CFR – Cost and Freight</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Pays freight to destination</li>
<li>Loads goods on vessel</li>
</ul>

<h4>Risk Transfers:</h4>
<p>When goods loaded onboard (not when they arrive).</p>

<div class="major-misunderstanding">
<p><strong>Major Misunderstanding:</strong> Seller pays freight but buyer bears risk after loading.</p>
</div>
</div>

<h3>2.6 CIF – Cost, Insurance & Freight</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Pays freight</li>
<li>Provides minimum marine insurance</li>
<li>Loads goods onboard</li>
</ul>

<h4>Risk Transfers:</h4>
<p>When loaded onboard.</p>

<h4>Insurance Requirement:</h4>
<p>Minimum ICC (C) coverage unless otherwise agreed.</p>

<div class="important-note">
<p><strong>Important:</strong> Insurance under CIF may not cover inland risk.</p>
</div>
</div>
</div>'''
                },
                {
                    "title": "CPT, CIP & Delivery Terms",
                    "content": '''<div class="lesson-content">
<h3>2.7 CPT – Carriage Paid To</h3>
<p>Seller pays transport. Risk transfers when goods handed to carrier.</p>

<h3>2.8 CIP – Carriage & Insurance Paid To</h3>
<p>Similar to CPT but includes insurance. Insurance must be ICC (A) — higher coverage than CIF.</p>

<h3>2.9 DAP – Delivered at Place</h3>
<p>Seller delivers ready for unloading. Buyer handles import clearance. Risk transfers at delivery point.</p>

<h3>2.10 DPU – Delivered at Place Unloaded</h3>
<p>Seller delivers AND unloads goods. Only term requiring seller to unload.</p>

<h3>2.11 DDP – Delivered Duty Paid</h3>
<div class="term-breakdown">
<h4>Seller:</h4>
<ul>
<li>Handles everything</li>
<li>Pays import duties</li>
</ul>

<div class="risk-warning">
<p><strong>Very risky in Ghana, Nigeria, Kenya due to complex tax laws.</strong></p>
<p>Not recommended unless seller has legal entity locally.</p>
</div>
</div>
</div>'''
                },
                {
                    "title": "Sea Freight Documentation",
                    "content": '''<div class="lesson-content">
<h2>MODULE 3: Sea Freight Operations & Documentation</h2>

<h3>3.1 Key Shipping Documents</h3>

<h4>Bill of Lading (B/L)</h4>
<p><strong>Functions:</strong></p>
<ul>
<li>Contract of carriage</li>
<li>Receipt of goods</li>
<li>Document of title</li>
</ul>

<p><strong>Types:</strong></p>
<ul>
<li>Straight B/L</li>
<li>Order B/L</li>
<li>Sea Waybill</li>
</ul>

<h4>Commercial Invoice</h4>
<p>Basis for customs valuation.</p>

<h4>Packing List</h4>
<p>Details packaging, weight, dimensions.</p>

<h4>Certificate of Origin</h4>
<p>Used for preferential tariffs.</p>

<h4>Marine Insurance Certificate</h4>
<p>Required under CIF and CIP.</p>

<h4>Cargo Tracking Note (CTN / ECTN)</h4>
<p><strong>Mandatory in:</strong></p>
<ul>
<li>Ghana</li>
<li>Nigeria</li>
<li>Some East African shipments</li>
</ul>
<p><strong>Failure results in heavy penalties.</strong></p>
</div>'''
                },
                {
                    "title": "Sea Freight Charges & Ghana Maritime Law",
                    "content": '''<div class="lesson-content">
<h3>3.2 Sea Freight Charges</h3>
<ul>
<li>Freight cost</li>
<li>Terminal handling charges (THC)</li>
<li>Documentation fees</li>
<li>Port charges</li>
<li>Demurrage</li>
<li>Detention</li>
</ul>
<p><strong>Incorrect Incoterm choice can shift these costs unintentionally.</strong></p>

<h2>MODULE 4: Maritime Law – Ghana</h2>

<h3>4.1 Key Legal Instruments</h3>

<h4>Ghana Shipping Act 2003</h4>
<p><strong>Regulates:</strong></p>
<ul>
<li>Vessel registration</li>
<li>Carriage of goods</li>
<li>Maritime liens</li>
<li>Safety requirements</li>
</ul>

<h4>Ghana Maritime Authority Act</h4>
<p>Establishes regulatory oversight.</p>

<h4>Customs Act (Ghana)</h4>
<p>Governs import/export clearance procedures.</p>

<h3>4.2 Sea Freight Compliance in Ghana</h3>
<ul>
<li>Mandatory Cargo Tracking Note</li>
<li>Advance shipment notification</li>
<li>Port handling at Tema and Takoradi</li>
<li>Customs valuation rules (CIF-based valuation)</li>
</ul>

<div class="important-note">
<p><strong>Important:</strong> Ghana customs typically calculate duties based on CIF value — even if shipment is FOB.</p>
</div>
</div>'''
                },
                {
                    "title": "Nigeria & Kenya Maritime Law",
                    "content": '''<div class="lesson-content">
<h2>MODULE 5: Maritime Law – Nigeria</h2>

<h3>5.1 Merchant Shipping Act (Nigeria)</h3>
<p><strong>Covers:</strong></p>
<ul>
<li>Vessel safety</li>
<li>Carrier liability</li>
<li>Carriage obligations</li>
<li>Maritime claims</li>
</ul>

<h3>5.2 Coastal and Inland Shipping (Cabotage) Act</h3>
<p>Restricts domestic shipping to Nigerian-owned vessels.</p>

<h3>5.3 Nigerian Ports Authority Regulations</h3>
<p><strong>Regulates:</strong></p>
<ul>
<li>Port access</li>
<li>Terminal operations</li>
<li>Freight handling</li>
</ul>

<h3>5.4 Nigeria Customs Service Act</h3>
<p><strong>Defines:</strong></p>
<ul>
<li>Import duty structure</li>
<li>Documentation requirements</li>
<li>Pre-arrival assessment reports</li>
</ul>

<h3>5.5 Cargo Tracking Note Requirement</h3>
<p>Nigeria requires electronic cargo tracking for imports.</p>
<p><strong>Non-compliance leads to:</strong></p>
<ul>
<li>Fines</li>
<li>Delayed clearance</li>
<li>Cargo seizure risk</li>
</ul>

<h2>MODULE 6: Maritime Law – Kenya</h2>

<h3>6.1 Kenya Merchant Shipping Act</h3>
<p><strong>Regulates:</strong></p>
<ul>
<li>Vessel registration</li>
<li>Marine pollution</li>
<li>Maritime safety</li>
<li>Carrier liability</li>
</ul>

<h3>6.2 Kenya Ports Authority Act</h3>
<p>Oversees Mombasa port operations.</p>

<h3>6.3 Kenya Revenue Authority (Customs)</h3>
<p><strong>Duties calculated based on:</strong></p>
<ul>
<li>CIF valuation method</li>
<li>East African Community Customs Management Act</li>
</ul>

<h3>6.4 Regional Considerations</h3>
<p><strong>Kenya operates within:</strong></p>
<ul>
<li>East African Community customs framework</li>
<li>Harmonized tariff system</li>
</ul>
</div>'''
                },
                {
                    "title": "Risk Management & Case Studies",
                    "content": '''<div class="lesson-content">
<h2>MODULE 7: Risk Management & Insurance in Sea Freight</h2>

<h3>7.1 Marine Insurance Types</h3>
<ul>
<li>ICC (A) – All Risks</li>
<li>ICC (B)</li>
<li>ICC (C) – Minimum coverage</li>
</ul>

<h3>7.2 Risk Scenarios</h3>
<p><strong>Example:</strong> CIF Tema shipment damaged at sea. Risk transfers at loading port. Buyer must claim under seller-provided insurance.</p>

<h3>7.3 Common Disputes</h3>
<ul>
<li>Wrong Incoterm used for container cargo</li>
<li>No insurance under CFR</li>
<li>DDP without tax registration</li>
<li>Misdeclared customs value</li>
</ul>

<h2>MODULE 8: Practical Case Studies</h2>

<h3>Case Study 1 – Ghana</h3>
<p>A Nigerian exporter ships machinery CIF Tema.</p>
<p><strong>Issues:</strong></p>
<ul>
<li>Insurance only ICC (C)</li>
<li>Damage during inland transport</li>
<li>Customs recalculates value</li>
</ul>
<p><strong>Discussion:</strong> Who bears inland damage risk?</p>

<h3>Case Study 2 – Nigeria</h3>
<p>Chinese supplier ships FOB Lagos. Container damaged before loading. Liability?</p>

<h3>Case Study 3 – Kenya</h3>
<p>German seller agrees DDP Mombasa. Seller lacks Kenyan tax registration. Customs delays shipment. Who bears cost?</p>
</div>'''
                },
                {
                    "title": "Final Assessment & Course Completion",
                    "content": '''<div class="lesson-content">
<h2>FINAL ASSESSMENT</h2>

<h3>Section A – Multiple Choice (Sample)</h3>
<p><strong>1. Under FOB, risk transfers:</strong></p>
<ul>
<li>A. At seller's warehouse</li>
<li>B. When goods loaded onboard vessel</li>
<li>C. At destination port</li>
<li>D. After customs clearance</li>
</ul>
<p><strong>Correct Answer: B</strong></p>

<h3>Section B – Scenario Question</h3>
<p>Draft correct Incoterm for: Exporter in Accra shipping containerized goods to Mombasa where buyer arranges freight.</p>
<p><strong>Correct answer:</strong> FCA Accra (Incoterms 2020)</p>

<h2>COURSE COMPLETION OUTCOME</h2>
<p>Learners completing this course will:</p>
<ul>
<li>Confidently draft Incoterms clauses</li>
<li>Avoid costly shipping errors</li>
<li>Understand maritime compliance in Ghana, Nigeria, Kenya</li>
<li>Reduce legal exposure in sea freight contracts</li>
<li>Improve negotiation strategy in international trade</li>
</ul>

<div class="completion-badge">
<h3>🎓 Congratulations!</h3>
<p>You have successfully completed the Master Course on International Commercial Terms (Incoterms® 2020) & Sea Freight Law.</p>
</div>
</div>'''
                }
            ]
            
            # Insert new lessons
            for i, lesson_data in enumerate(lessons):
                lesson_doc = {
                    "id": f"{module['id']}_lesson_{i+1}",
                    "module_id": module["id"],
                    "title": lesson_data["title"],
                    "content_type": "text",
                    "content": lesson_data["content"],
                    "duration_minutes": 15,
                    "order": i
                }
                db.lessons.insert_one(lesson_doc)
            
            # Update course details
            db.courses.update_one(
                {"_id": incoterms_course["_id"]},
                {
                    "$set": {
                        "description": "Master Course: International Commercial Terms (Incoterms® 2020) & Sea Freight Law with Legal Frameworks for Ghana, Nigeria & Kenya",
                        "duration_hours": 10,
                        "level": "Advanced Professional"
                    }
                }
            )
            
            print(f"Updated Incoterms course with {len(lessons)} comprehensive lessons")

if __name__ == "__main__":
    update_incoterms_comprehensive()