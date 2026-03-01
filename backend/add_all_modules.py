#!/usr/bin/env python3
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

MODULES = [
    {
        "title": "Module 1: Global Supply Chain Architecture",
        "description": "The structural design of networks and the physics of flow",
        "duration": "2 Hours",
        "lessons": [
            {"title": "1.1 The SCOR Model Framework", "content": """<h3>The SCOR Model Framework</h3>
<p>The Supply Chain Operations Reference (SCOR) model is the world's leading supply chain framework. It breaks down every process into six primary pillars:</p>
<ul>
<li><strong>Plan:</strong> Demand and supply planning and management.</li>
<li><strong>Source:</strong> Sourcing infrastructure and material acquisition.</li>
<li><strong>Make:</strong> Manufacturing and production execution.</li>
<li><strong>Deliver:</strong> Order management, warehousing, and transportation.</li>
<li><strong>Return:</strong> Managing the reverse flow of goods (defective or surplus).</li>
<li><strong>Enable:</strong> Managing business rules, performance, and data.</li>
</ul>"""},
            {"title": "1.2 The Bullwhip Effect: Mathematics of Distortion", "content": """<h3>The Bullwhip Effect</h3>
<p>The Bullwhip Effect explains how a small fluctuation in consumer demand (e.g., 5%) results in massive fluctuations at the raw material level (e.g., 40%).</p>
<h4>Causes:</h4>
<ul>
<li>Demand forecast updating</li>
<li>Order batching</li>
<li>Price fluctuations</li>
<li>Rationing/shortage gaming</li>
</ul>
<p><strong>Key Insight:</strong> If the variance ratio is > 1, the bullwhip effect is present.</p>"""}
        ]
    },
    {
        "title": "Module 2: Strategic Procurement & Vendor Intelligence",
        "description": "Moving from transactional buying to value creation",
        "duration": "2.5 Hours",
        "lessons": [
            {"title": "2.1 The Kraljic Matrix", "content": """<h3>The Kraljic Matrix</h3>
<p>This 2x2 matrix is the gold standard for procurement strategy, categorizing items by Supply Risk and Profit Impact:</p>
<ul>
<li><strong>Strategic Items:</strong> High risk, high impact (e.g., engines for an aircraft). Strategy: Partnerships.</li>
<li><strong>Leverage Items:</strong> Low risk, high impact (e.g., bulk raw materials). Strategy: Competitive bidding.</li>
<li><strong>Bottleneck Items:</strong> High risk, low impact (e.g., specialized spare parts). Strategy: Secure continuity.</li>
<li><strong>Non-Critical Items:</strong> Low risk, low impact (e.g., office supplies). Strategy: Process efficiency.</li>
</ul>"""},
            {"title": "2.2 Total Cost of Ownership (TCO)", "content": """<h3>Total Cost of Ownership (TCO)</h3>
<p>The purchase price is only "the tip of the iceberg." TCO accounts for:</p>
<ul>
<li><strong>Acquisition Costs:</strong> Price, taxes, duties, and transport.</li>
<li><strong>Ownership Costs:</strong> Storage, insurance, and maintenance.</li>
<li><strong>Post-Ownership Costs:</strong> Disposal, environmental impact, and warranty claims.</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 3: Advanced Inventory & Warehouse Dynamics",
        "description": "The science of 'buffer' and the optimization of physical space",
        "duration": "3 Hours",
        "lessons": [
            {"title": "3.1 The Economic Order Quantity (EOQ)", "content": """<h3>The Economic Order Quantity (EOQ)</h3>
<p>The goal is to find the "Sweet Spot" where total costs are minimized.</p>
<ul>
<li><strong>Holding Cost (H):</strong> The cost of "dead money" and storage space.</li>
<li><strong>Setup Cost (K):</strong> The administrative cost of placing an order.</li>
</ul>
<p>EOQ helps balance ordering costs against holding costs to minimize total inventory costs.</p>"""},
            {"title": "3.2 Warehouse Design: The Honeycombing Effect", "content": """<h3>Warehouse Design: The Honeycombing Effect</h3>
<p>Inefficient warehouse slotting leads to "honeycombing"—empty spaces in racks that cannot be filled because of SKU isolation.</p>
<h4>Key Strategies:</h4>
<ul>
<li><strong>Cross-Docking:</strong> Unloading goods from an incoming semi-trailer and loading them directly into outbound trucks with little to no storage in between.</li>
<li><strong>ABC Analysis:</strong> Using Pareto's Law (80/20 rule) to place "A" items (high velocity) closest to the shipping docks to reduce travel time.</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 4: Logistics, Distribution, and Cold Chain",
        "description": "Physical transit and legal accountability",
        "duration": "2.5 Hours",
        "lessons": [
            {"title": "4.1 Incoterms 2020: The Rules of the Game", "content": """<h3>Incoterms 2020</h3>
<p>Understanding where the "Risk" and "Cost" transfer from seller to buyer is critical for insurance and pricing.</p>
<ul>
<li><strong>EXW (Ex Works):</strong> Maximum liability for the buyer.</li>
<li><strong>DDP (Delivered Duty Paid):</strong> Maximum liability for the seller.</li>
<li><strong>FOB (Free On Board):</strong> Risk transfers the moment the goods cross the ship's rail.</li>
</ul>"""},
            {"title": "4.2 The Last Mile & Cold Chain", "content": """<h3>The Last Mile & Cold Chain</h3>
<ul>
<li><strong>The Last Mile:</strong> Often represents 53% of total shipping costs. Route optimization algorithms are critical.</li>
<li><strong>Cold Chain:</strong> Deep dive into "Active" vs. "Passive" cooling systems for biologics (vaccines) and the impact of temperature excursions on shelf-life.</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 5: Digital Transformation & Risk Management",
        "description": "Industry 4.0 and the 'Antifragile' supply chain",
        "duration": "3 Hours",
        "lessons": [
            {"title": "5.1 Industry 4.0 Technologies", "content": """<h3>Industry 4.0 Technologies</h3>
<ul>
<li><strong>Blockchain:</strong> Creating an immutable ledger for food safety (Farm-to-Table) or diamond sourcing.</li>
<li><strong>Digital Twins:</strong> Using real-time IoT data to simulate how a port strike in Long Beach will affect inventory in Chicago three weeks from now.</li>
</ul>"""},
            {"title": "5.2 Risk Management: The FMEA Framework", "content": """<h3>Risk Management: The FMEA Framework</h3>
<p>Failure Mode and Effects Analysis (FMEA) calculates a Risk Priority Number (RPN):</p>
<p><strong>RPN = Severity × Occurrence × Detection</strong></p>
<p>This framework helps prioritize which risks to address first based on their potential impact and likelihood.</p>"""}
        ]
    },
    {
        "title": "Module 6: Supply Chain Finance & Working Capital",
        "description": "The flow of cash as much as the flow of boxes",
        "duration": "2 Hours",
        "lessons": [
            {"title": "6.1 The Cash-to-Cash (C2C) Conversion Cycle", "content": """<h3>The Cash-to-Cash (C2C) Conversion Cycle</h3>
<p>This is the ultimate metric for supply chain efficiency. It measures how long a company's cash is tied up in inventory before it is recovered through sales.</p>
<h4>The Formula:</h4>
<p><strong>C2C = DIO + DSO - DPO</strong></p>
<ul>
<li><strong>DIO:</strong> Days Inventory Outstanding (How long it sits in the warehouse).</li>
<li><strong>DSO:</strong> Days Sales Outstanding (How long customers take to pay you).</li>
<li><strong>DPO:</strong> Days Payables Outstanding (How long you take to pay suppliers).</li>
</ul>
<p><strong>Negative C2C:</strong> How companies like Dell and Amazon use customer money to fund their growth.</p>"""},
            {"title": "6.2 Supply Chain Financing (SCF)", "content": """<h3>Supply Chain Financing (SCF)</h3>
<ul>
<li><strong>Reverse Factoring:</strong> Using the buyer's high credit rating to help suppliers get lower-interest loans.</li>
<li><strong>Letter of Credit (L/C):</strong> Deep dive into bank-guaranteed international trade payments.</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 7: Global Trade Compliance & Customs",
        "description": "The 'Invisible Walls' of the supply chain",
        "duration": "1.5 Hours",
        "lessons": [
            {"title": "7.1 Harmonized System (HS) Codes", "content": """<h3>Harmonized System (HS) Codes</h3>
<ul>
<li>How a 6-to-10 digit code determines your import duty.</li>
<li><strong>Case Study:</strong> The "Chicken Tax"—how a 25% tariff on light trucks changed the global automotive manufacturing landscape.</li>
</ul>"""},
            {"title": "7.2 Trade Agreements & Rules of Origin", "content": """<h3>Trade Agreements & Rules of Origin</h3>
<ul>
<li><strong>USMCA, EU-UK TCA, and AfCFTA:</strong> Understanding regional value content (RVC) to qualify for zero-duty shipments.</li>
<li><strong>Anti-Dumping Duties:</strong> Identifying when "predatory pricing" from foreign competitors triggers government intervention.</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 8: Sustainable Operations & Circular Economy",
        "description": "Moving from 'Linear' (Take-Make-Waste) to 'Circular' (Recover-Redesign)",
        "duration": "1.5 Hours",
        "lessons": [
            {"title": "8.1 The Triple Bottom Line (TBL)", "content": """<h3>The Triple Bottom Line (TBL)</h3>
<p>Evaluating performance based on Profit, People, and Planet.</p>
<ul>
<li><strong>Carbon Footprinting:</strong> Calculating CO2e per ton-mile for different transport modes (Sea vs. Air).</li>
<li><strong>Reverse Logistics Strategy:</strong> Designing for "Remanufacturing" rather than just "Recycling."</li>
</ul>"""},
            {"title": "8.2 Ethical Sourcing & Human Rights", "content": """<h3>Ethical Sourcing & Human Rights</h3>
<ul>
<li>The UK Modern Slavery Act and the Uyghur Forced Labor Prevention Act (UFLPA).</li>
<li><strong>Conflict Minerals:</strong> Monitoring the supply chain for Tantalum, Tin, Tungsten, and Gold (3TG).</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 9: Demand Forecasting & Statistical Models",
        "description": "The 'Brain' of the supply chain",
        "duration": "2 Hours",
        "lessons": [
            {"title": "9.1 Quantitative Forecasting Methods", "content": """<h3>Quantitative Forecasting Methods</h3>
<ul>
<li><strong>Simple Moving Average (SMA):</strong> For stable demand.</li>
<li><strong>Exponential Smoothing:</strong> Weighting recent data more heavily (where α is the smoothing constant, A is actual demand, and F is the forecast).</li>
<li><strong>Regression Analysis:</strong> Predicting demand based on external variables (e.g., weather or interest rates).</li>
</ul>"""},
            {"title": "9.2 Measuring Forecast Accuracy", "content": """<h3>Measuring Forecast Accuracy</h3>
<ul>
<li><strong>MAPE (Mean Absolute Percentage Error):</strong> The standard "Executive" metric.</li>
<li><strong>Tracking Signal:</strong> A calculation used to detect if a forecast model is "Biased" (consistently over or under-predicting).</li>
</ul>"""}
        ]
    },
    {
        "title": "Module 10: Lean Six Sigma in Supply Chain",
        "description": "Eliminating waste (Muda) and reducing variability",
        "duration": "1.5 Hours",
        "lessons": [
            {"title": "10.1 The 8 Wastes of Lean (DOWNTIME)", "content": """<h3>The 8 Wastes of Lean (DOWNTIME)</h3>
<ul>
<li><strong>D</strong>efects</li>
<li><strong>O</strong>verproduction</li>
<li><strong>W</strong>aiting</li>
<li><strong>N</strong>on-utilized Talent</li>
<li><strong>T</strong>ransportation</li>
<li><strong>I</strong>nventory</li>
<li><strong>M</strong>otion</li>
<li><strong>E</strong>xtra-processing</li>
</ul>"""},
            {"title": "10.2 DMAIC Framework for Process Improvement", "content": """<h3>DMAIC Framework</h3>
<p>Define, Measure, Analyze, Improve, Control.</p>
<p><strong>Kaizen Events:</strong> Rapid, 5-day improvement workshops on the warehouse floor.</p>"""}
        ]
    },
    {
        "title": "Module 11: Crisis Management & Global Resilience",
        "description": "Navigating high-impact, low-probability disruptions and 'Black Swan' events",
        "duration": "2 Hours",
        "lessons": [
            {"title": "11.1 The Era of Constant Disruption", "content": """<h3>The Era of Constant Disruption</h3>
<p>The mid-2020s have redefined supply chain risk. The shift from Efficiency (Lean) to Antifragility (Agility).</p>
<ul>
<li><strong>Black Swan:</strong> Unpredictable, high-impact events (e.g., COVID-19 pandemic).</li>
<li><strong>Grey Swan:</strong> Known risks with high impact but uncertain timing (e.g., a major cyberattack on the Suez Canal or regional wars).</li>
<li><strong>Chokepoint Geopolitics:</strong> Deep dive into the Suez Canal, Panama Canal, and Strait of Hormuz. Analysis of the 2024-2026 Red Sea volatility and its impact on transit times (adding +10-15 days via the Cape of Good Hope).</li>
</ul>"""},
            {"title": "11.2 Business Continuity Planning (BCP)", "content": """<h3>Business Continuity Planning (BCP)</h3>
<p>Building a "Resilience Playbook" using two key metrics:</p>
<ul>
<li><strong>Time to Recover (TTR):</strong> The time required for a node (factory/port) to return to full capacity after a shock.</li>
<li><strong>Time to Survive (TTS):</strong> The maximum duration the supply chain can meet demand while a node is down, based on existing inventory and alternative sourcing.</li>
</ul>"""},
            {"title": "11.3 Nearshoring and Friend-shoring", "content": """<h3>Nearshoring and Friend-shoring</h3>
<p>Analysis of the "De-globalization" trend:</p>
<ul>
<li><strong>Nearshoring:</strong> Moving production closer to the end consumer (e.g., US companies moving from China to Mexico).</li>
<li><strong>Friend-shoring:</strong> Sourcing from countries with shared values/treaties to avoid sudden sanctions or trade wars.</li>
</ul>"""}
        ]
    }
]

async def add_modules():
    course = await db.courses.find_one({
        "title": {"$regex": "diploma.*supply.*chain", "$options": "i"}
    })
    
    if not course:
        print("Course not found!")
        return
    
    print(f"Adding modules to: {course['title']}\n")
    
    for idx, module_data in enumerate(MODULES, start=2):
        module_id = str(uuid.uuid4())
        module_doc = {
            "id": module_id,
            "course_id": course["id"],
            "title": module_data["title"],
            "description": module_data["description"],
            "order": idx
        }
        
        await db.modules.insert_one(module_doc)
        print(f"Created: {module_data['title']}")
        
        for lesson_idx, lesson_data in enumerate(module_data["lessons"]):
            lesson_doc = {
                "id": str(uuid.uuid4()),
                "module_id": module_id,
                "title": lesson_data["title"],
                "content_type": "text",
                "content": lesson_data["content"],
                "duration_minutes": 30,
                "order": lesson_idx
            }
            
            await db.lessons.insert_one(lesson_doc)
            print(f"  - {lesson_data['title']}")
    
    print(f"\nAdded {len(MODULES)} modules with lessons")

if __name__ == "__main__":
    asyncio.run(add_modules())
