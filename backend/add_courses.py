from pymongo import MongoClient
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

course = {
    "id": str(uuid.uuid4()),
    "title": "Health & Safety Policy & Procedure",
    "code": "H/SP1",
    "description": "Flowitec is committed to maintaining a safe and healthy workplace for all employees and visitors. This course covers our health and safety policy to prevent accidents and injuries, comply with statutory requirements, and provide a safety-first culture across all company levels.",
    "category": "Compliance",
    "type": "compulsory",
    "duration": "2 hours",
    "thumbnail": "",
    "modules": [
        {
            "title": "Introduction to Health & Safety Policy",
            "order": 1,
            "lessons": [
                {
                    "title": "Policy Purpose and Commitment",
                    "type": "text",
                    "order": 1,
                    "content": "**Purpose:**\nTo prevent accidents and injuries in the workplace, comply with all statutory health and safety requirements, ensure handling, storage and distribution of products and to provide a safety-first culture across all company levels and also provide adequate training and support for all staff.\n\n**Policy Statement:**\nFlowitec is committed to maintaining a safe and healthy workplace for all employees and visitors. We recognize our legal and moral responsibility to prevent work-related injury or illness by ensuring our operations are safe, compliant and continuously improved.\n\nThis policy is enacted in accordance with:\n• Labour Act, 2003 (Act 651)\n• Factories, Offices and Shops Act, 1970 (Act 328)\n• Other applicable health, safety and environmental laws of Ghana"
                }
            ]
        },
        {
            "title": "Policy Guidelines",
            "order": 2,
            "lessons": [
                {
                    "title": "Warehouse Safety Requirements",
                    "type": "text",
                    "order": 1,
                    "content": "**Warehouse Access:**\nWarehouse access is restricted to authorized personnel only.\n\n**Personal Protective Equipment (PPE):**\nHigh-visibility vests, safety boots, gloves and helmets must be worn when:\n• Visiting the warehouse\n• Visiting clients on site\n\n**Sign-In Procedures:**\nAll staff must sign in and out when entering or exiting the warehouse.\n\n**Handling and Storage of Equipment:**\n• Use pallet jacks, forklifts and cranes for heavy lifting\n• Manual lifting (lifting with bare hands) should be minimized or avoided at all cost\n• Ensure all items are securely stacked to prevent tipping or falling"
                },
                {
                    "title": "Office Safety Guidelines",
                    "type": "text",
                    "order": 2,
                    "content": "**Electrical Safety:**\nEnsure all electrical equipment is properly grounded and inspected.\n\n**Fire Safety:**\nFire extinguishers must be mounted and inspected monthly.\n\n**Hazardous Materials:**\nFlammable materials must be stored in designated, ventilated areas."
                }
            ]
        },
        {
            "title": "Policy Procedures",
            "order": 3,
            "lessons": [
                {
                    "title": "Emergency Preparedness",
                    "type": "text",
                    "order": 1,
                    "content": "**Emergency Contacts:**\nEmergency contact numbers must be provided by all staff.\n\n**First Aid:**\nFirst aid kits must be fully stocked and accessible.\n\n**Supervision Requirements:**\nA minimum of one senior or trained staff must be on duty during:\n• Visits to warehouse\n• Movement of products or equipment\n• Offloading or onloading for delivery\n• Regular warehouse inspection"
                },
                {
                    "title": "Incident Reporting",
                    "type": "text",
                    "order": 2,
                    "content": "**Immediate Reporting:**\nAll injuries, near misses, and dangerous occurrences must be reported immediately to the HR Department.\n\n**Documentation:**\nIncident reports must be prepared and shared with supervisor and manager.\n\n**What to Report:**\n• All injuries (no matter how minor)\n• Near misses (incidents that could have caused injury)\n• Dangerous occurrences\n• Unsafe conditions\n• Equipment malfunctions"
                },
                {
                    "title": "Training and Supervision",
                    "type": "text",
                    "order": 3,
                    "content": "**New Employee Training:**\nAll new employees must undergo safety induction training.\n\n**Ongoing Training:**\nRegular refresher training must be conducted for staff.\n\n**Risk Meetings:**\nRisk meetings must be held weekly to discuss risk and safety practices.\n\n**Supervisor Responsibilities:**\nSupervisors must ensure compliance with all safety procedures."
                },
                {
                    "title": "Monitoring and Review",
                    "type": "text",
                    "order": 4,
                    "content": "**Risk Assessment:**\nRisk assessment must be reviewed annually or after any incident.\n\n**Policy Review:**\nThe policy will be reviewed and updated annually to reflect changes in law, operations, or risks.\n\n**Continuous Improvement:**\nFlowitec is committed to continuously improving health and safety standards based on feedback, incidents, and best practices."
                }
            ]
        },
        {
            "title": "Penalties for Non-Compliance",
            "order": 4,
            "lessons": [
                {
                    "title": "Understanding Penalties",
                    "type": "text",
                    "order": 1,
                    "content": "In accordance with Section 118(2) of the Labour Act, 2003 (Act 651), which requires employees to use safety appliances provided by the employer and follow safety instructions, Flowitec shall impose disciplinary actions for violations of health and safety regulations.\n\nFailure to comply with the health and safety provisions of this policy may result in penalties, depending on the severity and frequency of the offense.\n\nAll disciplinary actions will follow due process as provided in the company's internal HR policy and in compliance with the Labour Act. Employees will be given the opportunity to explain or appeal any disciplinary decisions."
                },
                {
                    "title": "Minor Infractions",
                    "type": "text",
                    "order": 2,
                    "content": "**Examples of Minor Infractions (First-time or low-risk violations):**\n• Not wearing PPE (e.g., gloves, helmet) in designated areas\n• Unauthorized movement in restricted warehouse zones\n\n**Penalties:**\n• Verbal warning with documentation\n• Mandatory retraining on safety procedures"
                },
                {
                    "title": "Moderate Infractions",
                    "type": "text",
                    "order": 3,
                    "content": "**Examples of Moderate Infractions (Repeated or moderately risky behavior):**\n• Repeated neglect of warehouse safety protocols\n• Improper use of equipment or machinery despite training\n\n**Penalties:**\n• Written warning placed in personnel file\n• Temporary suspension from hazardous duties"
                },
                {
                    "title": "Major Infractions",
                    "type": "text",
                    "order": 4,
                    "content": "**Examples of Major Infractions (High-risk or willful misconduct):**\n• Tampering with safety equipment (e.g., fire extinguishers, pallets)\n• Failure to report a serious incident or injury\n\n**Penalties:**\n• Final written warning\n• Suspension without pay (not more than 10 days)\n• Termination of employment (subject to due process)"
                },
                {
                    "title": "Contractors and Visitors",
                    "type": "text",
                    "order": 5,
                    "content": "Any contractor or visitor found violating health and safety rules may be immediately removed from the premises and barred from future access.\n\nThe company may also terminate contracts with vendors or suppliers who consistently disregard safety protocols."
                }
            ]
        },
        {
            "title": "Roles and Responsibilities",
            "order": 5,
            "lessons": [
                {
                    "title": "Management Responsibilities",
                    "type": "text",
                    "order": 1,
                    "content": "**Management must:**\n\n• Conduct regular risk assessment and safety audits\n• Ensure appropriate personal protective equipment (PPE) is provided and worn\n• Implement and enforce safe work procedures\n• Offer safety training and respond quickly to hazards and incident reports"
                },
                {
                    "title": "Employee Responsibilities",
                    "type": "text",
                    "order": 2,
                    "content": "**Employees must:**\n\n• Follow safety procedures and wear PPE\n• Report hazards, near misses, and incidents immediately\n• Attend mandatory training and talks\n• Operate, offload and onload equipment only if trained and authorized"
                },
                {
                    "title": "Visitor Responsibilities",
                    "type": "text",
                    "order": 3,
                    "content": "**Visitors must:**\n\n• Follow all safety rules and signs\n• Be accompanied or supervised in operational areas\n• Report any unsafe conditions observed"
                }
            ]
        },
        {
            "title": "Declaration and Commitment",
            "order": 6,
            "lessons": [
                {
                    "title": "Our Safety Culture",
                    "type": "text",
                    "order": 1,
                    "content": "Flowitec is committed to creating a culture where safety is a shared responsibility or duty.\n\nAll staff must actively contribute to:\n• Identifying hazards\n• Maintaining safety standards\n• Protecting the well-being of themselves and others\n\n**Remember:** Safety is everyone's responsibility. By completing this course, you acknowledge your understanding of and commitment to Flowitec's Health & Safety Policy and Procedures.\n\n**Your safety matters. Work safe, stay safe.**"
                }
            ]
        }
    ],
    "createdAt": datetime.now(timezone.utc),
    "updatedAt": datetime.now(timezone.utc)
}

result = db.courses.insert_one(course)
print(f"Course added successfully with ID: {result.inserted_id}")

client.close()
