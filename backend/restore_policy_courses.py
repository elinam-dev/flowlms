"""
Restore the 4 policy courses
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def restore_policy_courses():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Restoring 4 policy courses...")
    
    # Course 1: Leave Policy - Ghana
    leave_policy_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": leave_policy_id,
        "title": "Leave Policy - Ghana",
        "description": "The company recognizes the need for employees to rest, recharge and revitalize. This policy outlines the terms and conditions for requesting leave days at Flowitec Group Ltd.",
        "thumbnail": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "LPHR1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    leave_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": leave_module_id,
        "course_id": leave_policy_id,
        "title": "Course Content",
        "description": "Complete content for Leave Policy - Ghana",
        "order": 0
    })
    
    leave_pages = [
        {"title": "Introduction to Leave Policy", "content": '''<div class="policy-page"><h2>LEAVE POLICY (LPHR1)</h2><h3>Introduction</h3><p>The company recognizes the need for employees to <strong>rest, recharge and revitalize</strong>, hence the leave policy.</p><p>The leave policy outlines the terms and conditions for requesting leave days here at Flowitec Group Ltd.</p><div class="highlight-box"><h4>Purpose</h4><p>To provide employees with time off from work for various reasons, while also ensuring that the organization's operational needs are met.</p></div><p class="legal-note">This policy shall be construed in accordance with the laws of Ghana, including but not limited to the <strong>Labour Act, 2003 (Act 651)</strong>.</p></div>'''},
        {"title": "Eligibility & Leave Request", "content": '''<div class="policy-page"><h2>Eligibility & Leave Request Process</h2><div class="policy-section"><h3>1. Eligibility</h3><p>Notwithstanding any other provision of this policy, all <strong>permanent/full-time employees</strong> of Flowitec shall be eligible for leave.</p><div class="warning-box"><p><strong>Exclusions:</strong> Persons who are on probation and performance improvement plans are not eligible. However, exemptions may be made considering the gravity of the emergency.</p></div></div><div class="policy-section"><h3>2. Leave Request</h3><p>An employee seeking to take leave shall submit a <strong>leave request form</strong> to their supervisor at least <strong>10 days prior</strong> to the commencement of the leave, unless in cases of emergency.</p></div><div class="policy-section"><h3>3. Approval</h3><p>The supervisor shall review the leave request and approve or deny it based on the operational needs of the business, in accordance with the Labour Act, 2003 (Act 651).</p></div></div>'''},
        {"title": "Leave Duration & Exemptions", "content": '''<div class="policy-page"><h2>Leave Duration & Emergency Exemptions</h2><div class="policy-section"><h3>4. Leave Duration</h3><div class="info-box"><p>Unless otherwise approved by the company, the maximum duration of leave that an employee can take at any time is <strong>five (5) consecutive working days</strong>.</p></div></div><div class="policy-section"><h3>5. Emergency Exemptions</h3><p>The Company may grant exemptions in exceptional emergency circumstances:</p><ul><li>Serious illness</li><li>Injury</li><li>Study leave for exams</li><li>Family bereavement</li></ul></div><div class="policy-section"><h3>6. Wellness Break</h3><p>These <strong>2 days leave</strong> shall be in addition to the employee's annual leave entitlement, taken in <strong>October</strong>.</p></div></div>'''},
        {"title": "Leave Administration", "content": '''<div class="policy-page"><h2>Leave Administration</h2><div class="policy-section"><h3>7. Leave Payment</h3><p>Annual leave shall be paid at the employee's <strong>regular rate of pay</strong>.</p></div><div class="policy-section"><h3>8. Leave Carryover</h3><p>Accrued annual leave shall be carried over up to a maximum of <strong>10 days</strong>.</p></div><div class="policy-section"><h3>9. Leave Record</h3><p>The HR department shall maintain accurate and confidential records.</p></div><div class="policy-section"><h3>10. Leave Cancellation</h3><p>Notify supervisor at least <strong>3 days prior</strong> to cancel a leave request.</p></div><div class="policy-section warning-box"><h3>11. Unapproved Leave</h3><p>Unauthorized leave may result in disciplinary action, up to and including termination.</p></div></div>'''},
        {"title": "Leave Types", "content": '''<div class="policy-page"><h2>Types of Leave</h2><div class="leave-type"><h3>1. Annual Leave</h3><div class="days-badge">21 Days</div><p>For vacation, personal or family purpose. Plus <strong>2 wellness days</strong> in October.</p></div><div class="leave-type"><h3>2. Sick Leave</h3><div class="days-badge">10 Days</div><p>For illness or injury. May be extended based on health conditions.</p></div><div class="leave-type"><h3>3. Bereavement Leave</h3><div class="days-badge">5 Days</div><p>For bereavement or funeral purposes.</p></div></div>'''},
        {"title": "Additional Leave Types", "content": '''<div class="policy-page"><h2>Additional Leave Types</h2><div class="leave-type"><h3>4. Maternity Leave</h3><div class="days-badge">12 Weeks</div><p>For childbirth or adoption purposes per Section 57 of the Labor Act, 2003.</p></div><div class="leave-type highlight"><h3>5. Wellness Break</h3><div class="days-badge special">2 Days</div><p>In recognition of mental health and well-being, taken in <strong>October</strong> for Mental Health Awareness Month.</p></div><div class="summary-box"><h4>Leave Summary</h4><ul><li><strong>Annual:</strong> 21 days + 2 wellness days</li><li><strong>Sick:</strong> 10 days</li><li><strong>Bereavement:</strong> 5 days</li><li><strong>Maternity:</strong> 12 weeks</li></ul></div></div>'''}
    ]
    
    for i, page in enumerate(leave_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": leave_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 2: Code of Ethics & Conduct
    ethics_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": ethics_id,
        "title": "Code of Ethics & Conduct",
        "description": "At Flowitec, we are committed to conducting business with integrity, transparency, and respect for all individuals.",
        "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop",
        "category": "Ethics",
        "duration_hours": 1.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "CEPC3",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    ethics_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": ethics_module_id,
        "course_id": ethics_id,
        "title": "Course Content",
        "order": 0
    })
    
    ethics_pages = [
        {"title": "Introduction", "content": '''<div class="policy-page"><h2>CODE OF ETHICS & CONDUCT</h2><p class="document-code">FLGG/232/72/CEPC3</p><h3>Introduction</h3><p>At Flowitec, we are committed to conducting business with <strong>integrity, transparency, and respect</strong> for all individuals.</p><div class="highlight-box"><p>This Code provides a framework for making ethical decisions and ensures we maintain a positive and professional environment.</p></div></div>'''},
        {"title": "Integrity and Honesty", "content": '''<div class="policy-page"><h2>1. Integrity and Honesty</h2><div class="principle-card"><ul><li>Conduct ourselves with the <strong>highest standards of integrity</strong></li><li>Be truthful in all communications</li><li>No deception, fraud, or misrepresentation</li></ul></div><h2>2. Respect for People</h2><div class="principle-card"><ul><li>Create a <strong>diverse and inclusive workplace</strong></li><li>No discrimination or harassment tolerated</li><li>Foster teamwork and open communication</li></ul></div></div>'''},
        {"title": "Fairness & Confidentiality", "content": '''<div class="policy-page"><h2>3. Fairness and Equal Opportunity</h2><div class="principle-card"><ul><li>Provide <strong>equal opportunity</strong> regardless of background</li><li>Decisions based on <strong>merit and performance</strong></li><li>Fair approach in all business practices</li></ul></div><h2>4. Confidentiality and Privacy</h2><div class="principle-card warning"><ul><li><strong>Protect confidential information</strong></li><li>Handle personal data with care</li><li>No use of information for personal gain</li></ul></div></div>'''},
        {"title": "Legal Compliance & Conflicts", "content": '''<div class="policy-page"><h2>5. Compliance with Laws</h2><div class="principle-card"><ul><li>Comply with all <strong>applicable laws and regulations</strong></li><li>Seek guidance from management when in doubt</li><li>Uphold ethical standards always</li></ul></div><h2>6. Conflicts of Interest</h2><div class="principle-card warning"><ul><li><strong>Avoid conflicts</strong> between personal and company interests</li><li>Disclose potential conflicts to supervisors</li><li>Gifts should not influence decisions</li></ul></div></div>'''},
        {"title": "Health, Safety & Accountability", "content": '''<div class="policy-page"><h2>7. Health, Safety, and Environment</h2><div class="principle-card"><ul><li>Provide <strong>safe and healthy workplace</strong></li><li>Minimize environmental impact</li><li>Report unsafe conditions immediately</li></ul></div><h2>8. Accountability</h2><div class="principle-card highlight"><ul><li><strong>Report unethical behavior</strong></li><li>Whistle-blowers protected from retaliation</li><li>Report through management or anonymous channels</li></ul></div></div>'''},
        {"title": "Financial Integrity & Excellence", "content": '''<div class="policy-page"><h2>9. Financial Integrity</h2><div class="principle-card"><ul><li>Financial records must be <strong>accurate and transparent</strong></li><li>No fraudulent reporting</li><li>Proper use of company resources</li></ul></div><h2>10. Commitment to Excellence</h2><div class="principle-card highlight"><ul><li>Strive for <strong>excellence</strong> in all work</li><li>Continuous improvement and innovation</li><li>Meet or exceed industry standards</li></ul></div></div>'''},
        {"title": "Gifts & Conclusion", "content": '''<div class="policy-page"><h2>11. Gifts and Favors</h2><div class="principle-card warning"><p>Employees <strong>will not solicit</strong> any gifts, bribes, favors, entertainment, loans, or items of monetary value from clients or suppliers.</p></div><h2>Conclusion</h2><div class="conclusion-box"><p>By adhering to this Code, we create a <strong>positive work environment</strong> supporting the success of the company, employees, and clients.</p><p class="emphasis">Each employee's commitment is vital to ensuring the <strong>long-term success and reputation</strong> of Flowitec.</p></div></div>'''}
    ]
    
    for i, page in enumerate(ethics_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": ethics_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 3: Disciplinary Code
    disciplinary_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": disciplinary_id,
        "title": "Disciplinary Code",
        "description": "This code fosters a culture of care, mutual respect, and teamwork while ensuring fair and consistent treatment.",
        "thumbnail": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 0.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "DCPC/HR1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    disciplinary_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": disciplinary_module_id,
        "course_id": disciplinary_id,
        "title": "Course Content",
        "order": 0
    })
    
    disciplinary_pages = [
        {"title": "Purpose of the Code", "content": '''<div class="policy-page"><h2>DISCIPLINARY CODE (DCPC/HR1)</h2><div class="info-box"><p>This document does not form part of any employment contract. All legal rights are reserved.</p></div><h3>Purpose of This Code</h3><div class="purpose-list"><div class="purpose-item"><span class="number">2.1</span><p>Foster a culture of <strong>care, mutual respect, and teamwork</strong></p></div><div class="purpose-item"><span class="number">2.2</span><p>Ensure <strong>fair and consistent treatment</strong> of all employees</p></div><div class="purpose-item"><span class="number">2.3</span><p>Provide a framework for <strong>collaboration</strong> between management and employees</p></div></div><div class="legal-note"><p>Works with The Code of Good Practice: Dismissal (Section 62, Labour Act, 2003).</p></div></div>'''},
        {"title": "Management Standards", "content": '''<div class="policy-page"><h2>Management Standards & Procedures</h2><div class="policy-section"><p><strong>4.</strong> Management sets standards for behavior and performance.</p></div><div class="policy-section"><p><strong>5.</strong> Minor issues addressed through:</p><ul><li>Counselling</li><li>PIPs (Performance Improvement Plans)</li><li>Warnings</li></ul></div><div class="policy-section warning-box"><p><strong>6.</strong> The Company reserves the right to <strong>terminate employment</strong> following fair procedure for conduct, performance, or capacity issues supported by clear evidence.</p></div></div>'''},
        {"title": "Gross Misconduct", "content": '''<div class="policy-page"><h2>7. Examples of Gross Misconduct</h2><div class="misconduct-grid"><div class="misconduct-item severe"><span class="number">7.1</span><p>Gross dishonesty</p></div><div class="misconduct-item severe"><span class="number">7.2</span><p>Willful damage of Company property</p></div><div class="misconduct-item severe"><span class="number">7.3</span><p>Physical assault on employer, employees, clients</p></div><div class="misconduct-item severe"><span class="number">7.4</span><p>Gross insubordination</p></div><div class="misconduct-item severe"><span class="number">7.5</span><p>Gross negligence</p></div><div class="misconduct-item severe"><span class="number">7.6</span><p>Misuse of drugs, alcohol</p></div><div class="misconduct-item severe"><span class="number">7.7</span><p>Sexual harassment</p></div></div><div class="warning-box"><p><strong>Note:</strong> May result in immediate dismissal following due process.</p></div></div>'''},
        {"title": "Unacceptable Behaviors", "content": '''<div class="policy-page"><h2>8. Unacceptable Behaviors</h2><div class="behavior-section"><h3>8.1 Obscene, immoral, or offensive conduct:</h3><ul><li>Sexual harassment</li><li>Racism, ethnocentrism, foul language</li><li>Rudeness to colleagues, clients, stakeholders</li></ul></div><div class="behavior-grid"><div class="behavior-item"><span class="number">8.2</span><p>Disloyalty</p></div><div class="behavior-item"><span class="number">8.3</span><p>Persistent absenteeism without leave</p></div><div class="behavior-item"><span class="number">8.4</span><p>Persistent late coming</p></div><div class="behavior-item"><span class="number">8.5</span><p>Insubordination</p></div><div class="behavior-item"><span class="number">8.6</span><p>Neglecting duties</p></div><div class="behavior-item"><span class="number">8.7</span><p>Failing to devote adequate attention</p></div></div></div>'''}
    ]
    
    for i, page in enumerate(disciplinary_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": disciplinary_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    # Course 4: Health & Safety Policy
    safety_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": safety_id,
        "title": "Health & Safety Policy",
        "description": "Flowitec is committed to maintaining a safe and healthy workplace for all employees and visitors.",
        "thumbnail": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=400&h=225&fit=crop",
        "category": "Safety",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "H/SP1",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    safety_module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": safety_module_id,
        "course_id": safety_id,
        "title": "Course Content",
        "order": 0
    })
    
    safety_pages = [
        {"title": "Policy Overview", "content": '''<div class="policy-page"><h2>HEALTH & SAFETY POLICY</h2><p class="document-code">Policy No: H/SP 1</p><div class="purpose-box"><h3>Purpose</h3><ul><li>Prevent accidents and injuries</li><li>Comply with statutory requirements</li><li>Ensure proper handling and storage</li><li>Provide safety-first culture</li><li>Provide adequate training</li></ul></div><div class="policy-statement highlight-box"><h3>POLICY</h3><p>Flowitec is committed to maintaining a <strong>safe and healthy workplace</strong> for all employees and visitors.</p></div><div class="legal-note"><p>Enacted per <strong>Labour Act, 2003 (Act 651)</strong> and <strong>Factories, Offices and Shops Act, 1970</strong>.</p></div></div>'''},
        {"title": "Safety Guidelines", "content": '''<div class="policy-page"><h2>Policy Guidelines</h2><h3>Warehouse Safety</h3><div class="guideline-item"><span class="number">1.</span><p>Warehouse access <strong>restricted to authorized personnel</strong></p></div><div class="guideline-item important"><span class="number">2.</span><p><strong>Required PPE:</strong> High-visibility vests, safety boots, gloves, helmets</p></div><div class="guideline-item"><span class="number">3.</span><p>All staff must <strong>sign in and out</strong></p></div><div class="guideline-item"><span class="number">4.</span><p>Use pallet jacks, forklifts for heavy lifting. Manual lifting should be minimized.</p></div><h3>Office Safety</h3><div class="guideline-item"><span class="number">5.</span><p>Electrical equipment grounded. Fire extinguishers mounted. Flammable materials in ventilated areas.</p></div></div>'''},
        {"title": "Emergency Procedures", "content": '''<div class="policy-page"><h2>Policy Procedures</h2><div class="procedure-grid"><div class="procedure-item"><span class="number">1.</span><p><strong>Emergency contacts</strong> must be provided by all staff</p></div><div class="procedure-item"><span class="number">2.</span><p><strong>First aid kits</strong> must be stocked and accessible</p></div><div class="procedure-item"><span class="number">3.</span><p><strong>One senior staff</strong> on duty during warehouse activities</p></div><div class="procedure-item important"><span class="number">4.</span><p>All injuries and near misses <strong>reported immediately</strong> to HR</p></div><div class="procedure-item"><span class="number">5.</span><p><strong>Incident reports</strong> shared with supervisor and manager</p></div></div></div>'''},
        {"title": "Training & Supervision", "content": '''<div class="policy-page"><h2>6. Training and Supervision</h2><div class="training-section"><div class="training-item"><span class="number">6.1</span><p>New employees undergo <strong>safety induction training</strong></p></div><div class="training-item"><span class="number">6.2</span><p><strong>Regular refresher training</strong> for all staff</p></div><div class="training-item"><span class="number">6.3</span><p><strong>Weekly risk meetings</strong></p></div><div class="training-item"><span class="number">6.4</span><p>Supervisors ensure compliance</p></div></div><h2>7. Monitoring and Review</h2><div class="monitoring-section"><div class="monitoring-item"><span class="number">7.1</span><p>Risk assessment reviewed <strong>annually</strong> or after incidents</p></div><div class="monitoring-item"><span class="number">7.2</span><p>Policy updated annually</p></div></div></div>'''},
        {"title": "Penalties", "content": '''<div class="policy-page"><h2>8. Penalties for Non-Compliance</h2><div class="legal-reference"><p>Per <strong>Section 118(2) of the Labour Act, 2003</strong></p></div><div class="penalty-section"><h3>8.1 Minor Infractions</h3><p class="examples">Not wearing PPE, unauthorized movement</p><ul><li>Verbal warning</li><li>Mandatory retraining</li></ul></div><div class="penalty-section moderate"><h3>8.2 Moderate Infractions</h3><p class="examples">Repeated neglect, improper equipment use</p><ul><li>Written warning</li><li>Temporary suspension</li></ul></div><div class="penalty-section severe"><h3>8.3 Major Infractions</h3><p class="examples">Tampering with safety equipment, failure to report</p><ul><li>Final warning</li><li>Suspension without pay</li><li>Termination</li></ul></div></div>'''},
        {"title": "Roles & Responsibilities", "content": '''<div class="policy-page"><h2>Roles And Responsibilities</h2><div class="role-section"><h3>1. Management Must:</h3><ul><li>Conduct risk assessments and safety audits</li><li>Ensure PPE is provided and worn</li><li>Implement safe work procedures</li><li>Offer safety training</li></ul></div><div class="role-section"><h3>2. Employees Must:</h3><ul><li>Follow safety procedures and wear PPE</li><li>Report hazards immediately</li><li>Attend mandatory training</li><li>Operate equipment only if trained</li></ul></div><div class="role-section"><h3>3. Visitors Must:</h3><ul><li>Follow all safety rules</li><li>Be accompanied in operational areas</li><li>Report unsafe conditions</li></ul></div><div class="declaration-box"><h3>Declaration</h3><p>Flowitec is committed to creating a culture where <strong>safety is a shared responsibility</strong>.</p></div></div>'''}
    ]
    
    for i, page in enumerate(safety_pages):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": safety_module_id,
            "title": page["title"],
            "content_type": "text",
            "content": page["content"],
            "duration_minutes": 5,
            "order": i
        })
    
    print("✓ Restored all 4 policy courses successfully!")
    client.close()

if __name__ == "__main__":
    asyncio.run(restore_policy_courses())
