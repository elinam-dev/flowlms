#!/usr/bin/env python3
"""
Script to reset courses and add new Flowitec policy courses with page-based content.
Also sets up Career Beetle data.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / 'backend' / '.env')

mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'flowitec_lms')

client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

# Course content pages - formatted for Alison-style page-by-page navigation
COURSES = [
    {
        "id": str(uuid.uuid4()),
        "title": "Leave Policy - Ghana",
        "description": "The company recognizes the need for employees to rest, recharge and revitalize. This policy outlines the terms and conditions for requesting leave days at Flowitec Group Ltd.",
        "thumbnail": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "LPHR1",
        "pages": [
            {
                "title": "Introduction to Leave Policy",
                "content": """<div class="policy-page">
                    <h2>LEAVE POLICY (LPHR1)</h2>
                    <h3>Introduction</h3>
                    <p>The company recognizes the need for employees to <strong>rest, recharge and revitalize</strong>, hence the leave policy.</p>
                    <p>The leave policy outlines the terms and conditions for requesting leave days here at Flowitec Group Ltd.</p>
                    <div class="highlight-box">
                        <h4>Purpose</h4>
                        <p>To provide employees with time off from work for various reasons, while also ensuring that the organization's operational needs are met.</p>
                    </div>
                    <p class="legal-note">This policy shall be construed in accordance with the laws of Ghana, including but not limited to the <strong>Labour Act, 2003 (Act 651)</strong>.</p>
                </div>"""
            },
            {
                "title": "Eligibility & Leave Request",
                "content": """<div class="policy-page">
                    <h2>Eligibility & Leave Request Process</h2>
                    
                    <div class="policy-section">
                        <h3>1. Eligibility</h3>
                        <p>Notwithstanding any other provision of this policy, all <strong>permanent/full-time employees</strong> of Flowitec shall be eligible for leave.</p>
                        <div class="warning-box">
                            <p><strong>Exclusions:</strong> Persons who are on probation and performance improvement plans are not eligible. However, exemptions may be made considering the gravity of the emergency.</p>
                        </div>
                    </div>
                    
                    <div class="policy-section">
                        <h3>2. Leave Request</h3>
                        <p>An employee seeking to take leave shall submit a <strong>leave request form</strong> to their supervisor at least <strong>10 days prior</strong> to the commencement of the leave, unless in cases of emergency.</p>
                    </div>
                    
                    <div class="policy-section">
                        <h3>3. Approval</h3>
                        <p>The supervisor shall review the leave request and approve or deny it based on the operational needs of the business, in accordance with the Labour Act, 2003 (Act 651), which states that <em>"the employer shall be the administrator of the leave days"</em>.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Leave Duration & Exemptions",
                "content": """<div class="policy-page">
                    <h2>Leave Duration & Emergency Exemptions</h2>
                    
                    <div class="policy-section">
                        <h3>4. Leave Duration</h3>
                        <div class="info-box">
                            <p>Unless otherwise approved by the company, the maximum duration of leave that an employee can take at any time is <strong>five (5) consecutive working days</strong>.</p>
                        </div>
                    </div>
                    
                    <div class="policy-section">
                        <h3>5. Emergency Exemptions</h3>
                        <p>The Company may, in its discretion, grant exemptions to the maximum leave duration in exceptional emergency circumstances:</p>
                        <ul>
                            <li>Serious illness</li>
                            <li>Injury</li>
                            <li>Study leave for exams</li>
                            <li>Family bereavement</li>
                        </ul>
                        <p>Such exemptions shall be subject to approval by the relevant supervisor or HR.</p>
                    </div>
                    
                    <div class="policy-section">
                        <h3>6. Wellness Break</h3>
                        <p>These <strong>2 days leave</strong> shall be in addition to the employee's annual leave entitlement.</p>
                        <div class="highlight-box">
                            <p>The leave shall only be taken in the <strong>month of October</strong>. Employees shall provide their managers with at least 10 days' notice prior to taking this leave.</p>
                        </div>
                    </div>
                </div>"""
            },
            {
                "title": "Leave Administration",
                "content": """<div class="policy-page">
                    <h2>Leave Administration</h2>
                    
                    <div class="policy-section">
                        <h3>7. Leave Payment</h3>
                        <p>Annual leave shall be paid at the employee's <strong>regular rate of pay</strong>, unless otherwise specified in this policy.</p>
                    </div>
                    
                    <div class="policy-section">
                        <h3>8. Leave Carryover</h3>
                        <p>Accrued annual leave shall be carried over from one year to the next, up to a maximum of <strong>10 days</strong>.</p>
                    </div>
                    
                    <div class="policy-section">
                        <h3>9. Leave Record</h3>
                        <p>The HR department shall maintain accurate and confidential records of employee leave.</p>
                    </div>
                    
                    <div class="policy-section">
                        <h3>10. Leave Cancellation</h3>
                        <p>An employee who wishes to cancel a leave request shall notify their supervisor at least <strong>3 days prior</strong> to the commencement of the leave.</p>
                    </div>
                    
                    <div class="policy-section warning-box">
                        <h3>11. Unapproved Leave</h3>
                        <p>Any leave taken without prior approval shall be considered <strong>unauthorized</strong> and may result in disciplinary action, up to and including termination.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Leave Types",
                "content": """<div class="policy-page">
                    <h2>Types of Leave</h2>
                    
                    <div class="leave-type">
                        <h3>1. Annual Leave</h3>
                        <div class="days-badge">21 Days</div>
                        <p>Employees shall be entitled to 21 days of annual leave days per year, which may be used for vacation, personal or family purpose, in accordance with Section 20 of the Labour Act, 2003 (Act 651).</p>
                        <p class="bonus">Plus <strong>2 wellness days</strong> each year, taken in October for World Mental Health Day.</p>
                    </div>
                    
                    <div class="leave-type">
                        <h3>2. Sick Leave</h3>
                        <div class="days-badge">10 Days</div>
                        <p>Employees shall be entitled to 10 days of sick leave per year for illness or injury. This may be extended based on employee's health conditions, in accordance with Section 57 of the Labour Act, 2003 (Act 651).</p>
                    </div>
                    
                    <div class="leave-type">
                        <h3>3. Bereavement Leave</h3>
                        <div class="days-badge">5 Days</div>
                        <p>Employees shall be entitled to 5 days of bereavement leave per year for bereavement or funeral purposes.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Additional Leave Types",
                "content": """<div class="policy-page">
                    <h2>Additional Leave Types</h2>
                    
                    <div class="leave-type">
                        <h3>4. Maternity Leave</h3>
                        <div class="days-badge">12 Weeks</div>
                        <p>Female employees shall be entitled to <strong>12 weeks maternity leave</strong> per year, which may be used for childbirth or adoption purposes in accordance with Section 57 of the Labor Act, 2003 (Act 651).</p>
                    </div>
                    
                    <div class="leave-type highlight">
                        <h3>5. Wellness Break</h3>
                        <div class="days-badge special">2 Days</div>
                        <p>In recognition of the importance of mental health and well-being, the Company shall grant an additional <strong>two (2) days of leave</strong> to all employees.</p>
                        <div class="info-box">
                            <h4>When:</h4>
                            <p>To be taken in the <strong>month of October</strong>, in commemoration of Mental Health Awareness Month.</p>
                            <h4>Purpose:</h4>
                            <p>To provide employees with the opportunity to recharge, relax, and prioritize their mental health and well-being.</p>
                        </div>
                    </div>
                    
                    <div class="summary-box">
                        <h4>Leave Summary</h4>
                        <ul>
                            <li><strong>Annual:</strong> 21 days + 2 wellness days</li>
                            <li><strong>Sick:</strong> 10 days</li>
                            <li><strong>Bereavement:</strong> 5 days</li>
                            <li><strong>Maternity:</strong> 12 weeks</li>
                        </ul>
                    </div>
                </div>"""
            }
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Code of Ethics & Conduct",
        "description": "At Flowitec, we are committed to conducting business with integrity, transparency, and respect for all individuals. This Code provides a framework for making ethical decisions.",
        "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop",
        "category": "Ethics",
        "duration_hours": 1.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "CEPC3",
        "pages": [
            {
                "title": "Introduction",
                "content": """<div class="policy-page">
                    <h2>CODE OF ETHICS & CONDUCT</h2>
                    <p class="document-code">FLGG/232/72/CEPC3</p>
                    
                    <h3>Introduction</h3>
                    <p>At Flowitec, we are committed to conducting business with <strong>integrity, transparency, and respect</strong> for all individuals.</p>
                    
                    <div class="highlight-box">
                        <p>This Code of Ethics & Conduct provides a framework for making ethical decisions and ensures that we maintain a positive and professional environment.</p>
                    </div>
                    
                    <p>All employees, managers, and executives are expected to uphold these standards in every aspect of their work.</p>
                </div>"""
            },
            {
                "title": "Integrity and Honesty",
                "content": """<div class="policy-page">
                    <h2>1. Integrity and Honesty</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We will conduct ourselves with the <strong>highest standards of integrity and honesty</strong> in all business dealings.</li>
                            <li>We will be truthful in communications and business transactions, ensuring that all information shared is <strong>accurate and transparent</strong>.</li>
                            <li>Employees must not engage in any form of <strong>deception, fraud, or misrepresentation</strong>.</li>
                        </ul>
                    </div>
                    
                    <h2>2. Respect for People</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We are committed to creating a <strong>diverse and inclusive workplace</strong> where every individual is treated with respect and dignity.</li>
                            <li>Discrimination, harassment, or any form of mistreatment based on race, gender, age, religion, disability, or any other characteristic <strong>will not be tolerated</strong>.</li>
                            <li>We will foster an environment that values <strong>teamwork, collaboration, and open communication</strong>.</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Fairness & Confidentiality",
                "content": """<div class="policy-page">
                    <h2>3. Fairness and Equal Opportunity</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We will provide <strong>equal opportunity</strong> for employment, promotion, and training, regardless of race, gender, sexual orientation, religion, disability, or other protected characteristics.</li>
                            <li>We will make decisions based on <strong>merit, competence, and performance</strong> rather than personal bias.</li>
                            <li>We will maintain a fair and unbiased approach in all business practices.</li>
                        </ul>
                    </div>
                    
                    <h2>4. Confidentiality and Privacy</h2>
                    
                    <div class="principle-card warning">
                        <ul>
                            <li>Employees must <strong>protect confidential and proprietary information</strong> related to the company, clients, and other stakeholders.</li>
                            <li>Personal data of employees and clients will be handled with the utmost care and in compliance with relevant <strong>privacy laws and regulations</strong>.</li>
                            <li>No employee should use confidential information for <strong>personal gain</strong> or share it with unauthorized individuals.</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Legal Compliance & Conflicts of Interest",
                "content": """<div class="policy-page">
                    <h2>5. Compliance with Laws and Regulations</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We will comply with all <strong>applicable laws, rules, and regulations</strong> in the countries where we operate.</li>
                            <li>Employees must familiarize themselves with the relevant legal requirements and seek guidance from management when in doubt.</li>
                            <li>We will uphold ethical standards and act responsibly, even when local practices may differ from our corporate values.</li>
                        </ul>
                    </div>
                    
                    <h2>6. Conflicts of Interest</h2>
                    
                    <div class="principle-card warning">
                        <ul>
                            <li>Employees must <strong>avoid situations</strong> where personal interests could conflict with the interests of the company.</li>
                            <li>Employees should <strong>disclose any potential conflicts</strong> of interest to their supervisors and avoid participating in decisions where they have a personal stake.</li>
                            <li>Gifts or other forms of compensation from business partners, clients, or suppliers should <strong>not influence decision-making</strong> or compromise the company's integrity.</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Health, Safety & Accountability",
                "content": """<div class="policy-page">
                    <h2>7. Health, Safety, and Environmental Responsibility</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We will provide a <strong>safe and healthy working environment</strong> for all employees, free from hazards or unsafe practices.</li>
                            <li>We are committed to <strong>minimizing our environmental impact</strong> and promoting sustainability in our operations.</li>
                            <li>Employees must adhere to all workplace safety regulations and <strong>immediately report</strong> any unsafe conditions or incidents.</li>
                        </ul>
                    </div>
                    
                    <h2>8. Accountability and Reporting Misconduct</h2>
                    
                    <div class="principle-card highlight">
                        <ul>
                            <li>Employees are responsible for <strong>reporting any unethical behavior</strong>, misconduct, or violations of this Code of Ethics.</li>
                            <li><strong>Whistle-blowers will be protected</strong> from retaliation for reporting in good faith.</li>
                            <li>Employees can report concerns to management or through anonymous channels provided by the company.</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Financial Integrity & Excellence",
                "content": """<div class="policy-page">
                    <h2>9. Financial Integrity and Responsibility</h2>
                    
                    <div class="principle-card">
                        <ul>
                            <li>We will ensure that all financial records are <strong>accurate, transparent</strong>, and comply with applicable accounting standards and regulations.</li>
                            <li>Employees must avoid any actions that could lead to <strong>fraudulent financial reporting</strong> or the misappropriation of company funds.</li>
                            <li>Proper use of company resources is expected, and personal use of company assets must be minimal and approved.</li>
                        </ul>
                    </div>
                    
                    <h2>10. Commitment to Excellence</h2>
                    
                    <div class="principle-card highlight">
                        <ul>
                            <li>We will strive for <strong>excellence</strong> in all aspects of our work and deliver high-quality products and services to our clients.</li>
                            <li><strong>Continuous improvement, innovation</strong>, and a commitment to best practices will guide our actions and decisions.</li>
                            <li>We will hold ourselves accountable for meeting or exceeding the standards set by our company and industry.</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Gifts, Favors & Conclusion",
                "content": """<div class="policy-page">
                    <h2>11. Gifts and Favors</h2>
                    
                    <div class="principle-card warning">
                        <p>Employees <strong>will not solicit</strong>, directly or indirectly, any:</p>
                        <ul>
                            <li>Gifts, bribes, favors</li>
                            <li>Entertainment, loans, commission</li>
                            <li>Any other item of monetary value or promise</li>
                        </ul>
                        <p>...from any of Flowitec's clients or suppliers as a condition to access Flowitec's services or obtain any kind of favor from Flowitec.</p>
                    </div>
                    
                    <h2>Conclusion</h2>
                    
                    <div class="conclusion-box">
                        <p>By adhering to this Code of Ethics & Conduct, we create a <strong>positive work environment</strong> that supports the success and growth of the company, its employees, and its clients.</p>
                        <p class="emphasis">Each employee's commitment to these principles is vital to ensuring the <strong>long-term success and reputation</strong> of Flowitec.</p>
                    </div>
                </div>"""
            }
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Disciplinary Code",
        "description": "This code fosters a culture of care, mutual respect, and teamwork among employees, clients and associated partners while ensuring fair and consistent treatment.",
        "thumbnail": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 0.5,
        "is_published": True,
        "course_type": "compulsory",
        "code": "DCPC/HR1",
        "pages": [
            {
                "title": "Purpose of the Disciplinary Code",
                "content": """<div class="policy-page">
                    <h2>DISCIPLINARY CODE (DCPC/HR1)</h2>
                    
                    <div class="info-box">
                        <p><strong>1.</strong> This document does not form part of any reserved employment contract. All legal rights are reserved, even if not explicitly mentioned herein.</p>
                    </div>
                    
                    <h3>2. Purpose of This Code</h3>
                    <div class="purpose-list">
                        <div class="purpose-item">
                            <span class="number">2.1</span>
                            <p>Foster a culture of <strong>care, mutual respect, and teamwork</strong> among employees, clients and associated partners.</p>
                        </div>
                        <div class="purpose-item">
                            <span class="number">2.2</span>
                            <p>Ensure <strong>fair and consistent treatment</strong> of all employees, within the framework of the law and accepted employment practices.</p>
                        </div>
                        <div class="purpose-item">
                            <span class="number">2.3</span>
                            <p>Provide a framework for <strong>collaboration</strong> between management and employees to maintain acceptable behavior and conduct.</p>
                        </div>
                    </div>
                    
                    <div class="legal-note">
                        <p><strong>3.</strong> The disciplinary code will work hand in hand with The Code of Good Practice: Dismissal (Section 62, Labour Act, 2003). The Code of Good Practice will serve as guideline notwithstanding any provisions in this document.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Management Standards & Procedures",
                "content": """<div class="policy-page">
                    <h2>Management Standards & Procedures</h2>
                    
                    <div class="policy-section">
                        <p><strong>4.</strong> Management sets standards for behavior and performance, and trusts employees to meet these expectations.</p>
                    </div>
                    
                    <div class="policy-section">
                        <p><strong>5.</strong> In instances of minor unacceptable behavior or poor performance, management will attempt to address these issues through:</p>
                        <ul>
                            <li>Counselling</li>
                            <li>PIPs (Performance Improvement Plans)</li>
                            <li>Warnings</li>
                        </ul>
                        <p>...except in exceptional circumstances.</p>
                    </div>
                    
                    <div class="policy-section warning-box">
                        <p><strong>6.</strong> The Company reserves the right to <strong>terminate or end employment</strong> for any unlawful reason, following a fair procedure. This includes termination due to:</p>
                        <ul>
                            <li>Employee conduct</li>
                            <li>Performance issues</li>
                            <li>Capacity issues</li>
                        </ul>
                        <p>...supported by clear and convincing evidence.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Gross Misconduct",
                "content": """<div class="policy-page">
                    <h2>7. Examples of Gross Misconduct</h2>
                    
                    <div class="misconduct-grid">
                        <div class="misconduct-item severe">
                            <span class="number">7.1</span>
                            <p>Gross dishonesty</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.2</span>
                            <p>Willful damage of Company property</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.3</span>
                            <p>Physical assault on the employer, fellow employees, clients or partners</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.4</span>
                            <p>Gross insubordination</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.5</span>
                            <p>Gross negligence</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.6</span>
                            <p>Misuse of drugs, alcohol and other habit-forming substances</p>
                        </div>
                        <div class="misconduct-item severe">
                            <span class="number">7.7</span>
                            <p>Sexual harassment</p>
                        </div>
                    </div>
                    
                    <div class="warning-box">
                        <p><strong>Note:</strong> Gross misconduct may result in immediate dismissal following due process.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Unacceptable Behaviors",
                "content": """<div class="policy-page">
                    <h2>8. Examples of Unacceptable Behaviors</h2>
                    
                    <div class="behavior-section">
                        <h3>8.1 Obscene, immoral, or offensive conduct including:</h3>
                        <ul>
                            <li><strong>8.1.1</strong> Sexual harassment</li>
                            <li><strong>8.1.2</strong> Racism, ethnocentrism, foul/vulgar language</li>
                            <li><strong>8.1.3</strong> Rudeness to colleagues, clients, suppliers or other stakeholders</li>
                        </ul>
                    </div>
                    
                    <div class="behavior-grid">
                        <div class="behavior-item">
                            <span class="number">8.2</span>
                            <p>Disloyalty</p>
                        </div>
                        <div class="behavior-item">
                            <span class="number">8.3</span>
                            <p>Persistent absenteeism without leave</p>
                        </div>
                        <div class="behavior-item">
                            <span class="number">8.4</span>
                            <p>Persistent late coming without prior notice</p>
                        </div>
                        <div class="behavior-item">
                            <span class="number">8.5</span>
                            <p>Insubordination</p>
                        </div>
                        <div class="behavior-item">
                            <span class="number">8.6</span>
                            <p>Neglecting duties</p>
                        </div>
                        <div class="behavior-item">
                            <span class="number">8.7</span>
                            <p>Failing to devote adequate attention to responsibilities</p>
                        </div>
                    </div>
                </div>"""
            }
        ]
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Health & Safety Policy",
        "description": "Flowitec is committed to maintaining a safe and healthy workplace for all employees and visitors. This policy outlines our health and safety procedures.",
        "thumbnail": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=400&h=225&fit=crop",
        "category": "Safety",
        "duration_hours": 1,
        "is_published": True,
        "course_type": "compulsory",
        "code": "H/SP1",
        "pages": [
            {
                "title": "Health & Safety Policy Overview",
                "content": """<div class="policy-page">
                    <h2>HEALTH & SAFETY POLICY & PROCEDURE</h2>
                    <p class="document-code">Policy No: H/SP 1</p>
                    
                    <div class="purpose-box">
                        <h3>Purpose</h3>
                        <ul>
                            <li>Prevent accidents and injuries in the workplace</li>
                            <li>Comply with all statutory health and safety requirements</li>
                            <li>Ensure proper handling, storage and distribution of products</li>
                            <li>Provide a safety-first culture across all company levels</li>
                            <li>Provide adequate training and support for all staff</li>
                        </ul>
                    </div>
                    
                    <div class="policy-statement highlight-box">
                        <h3>POLICY</h3>
                        <p>Flowitec is committed to maintaining a <strong>safe and healthy workplace</strong> for all employees and visitors. We recognize our legal and moral responsibility to prevent work-related injury or illness by ensuring our operations are safe, compliant and continuously improved.</p>
                    </div>
                    
                    <div class="legal-note">
                        <p>This policy is enacted in accordance with the <strong>Labour Act, 2003 (Act 651)</strong>, <strong>Factories, Offices and Shops Act, 1970 (Act 328)</strong> and other applicable health, safety and environmental laws of Ghana.</p>
                    </div>
                </div>"""
            },
            {
                "title": "Warehouse & Office Safety Guidelines",
                "content": """<div class="policy-page">
                    <h2>Policy Guidelines</h2>
                    
                    <div class="guideline-section">
                        <h3>Warehouse Safety</h3>
                        <div class="guideline-item">
                            <span class="number">1.</span>
                            <p>Warehouse access is <strong>restricted to authorized personnel only</strong>.</p>
                        </div>
                        <div class="guideline-item important">
                            <span class="number">2.</span>
                            <p><strong>Required PPE when visiting warehouse or client sites:</strong></p>
                            <ul>
                                <li>High-visibility vests</li>
                                <li>Safety boots</li>
                                <li>Gloves</li>
                                <li>Helmets</li>
                            </ul>
                        </div>
                        <div class="guideline-item">
                            <span class="number">3.</span>
                            <p>All staff must <strong>sign in and out</strong> when entering or exiting the warehouse.</p>
                        </div>
                        <div class="guideline-item">
                            <span class="number">4.</span>
                            <p><strong>Handling and storage of equipment:</strong></p>
                            <ul>
                                <li>Use pallet jacks, forklifts and cranes for heavy lifting</li>
                                <li>Manual lifting should be minimized or avoided</li>
                                <li>Ensure all items are securely stacked to prevent tipping or falling</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="guideline-section">
                        <h3>Office Safety Guidelines</h3>
                        <div class="guideline-item">
                            <span class="number">5.</span>
                            <ul>
                                <li>Ensure all electrical equipment is properly grounded and inspected</li>
                                <li>Fire extinguishers must be mounted and inspected monthly</li>
                                <li>Flammable materials must be stored in designated, ventilated areas</li>
                            </ul>
                        </div>
                    </div>
                </div>"""
            },
            {
                "title": "Emergency Procedures",
                "content": """<div class="policy-page">
                    <h2>Policy Procedure</h2>
                    
                    <div class="procedure-grid">
                        <div class="procedure-item">
                            <span class="number">1.</span>
                            <p><strong>Emergency contact numbers</strong> must be provided by all staff.</p>
                        </div>
                        <div class="procedure-item">
                            <span class="number">2.</span>
                            <p><strong>First aid kits</strong> must be fully stocked and accessible.</p>
                        </div>
                        <div class="procedure-item">
                            <span class="number">3.</span>
                            <p>A minimum of <strong>one senior or trained staff</strong> must be on duty during visits to warehouse or movement of products/equipment.</p>
                        </div>
                        <div class="procedure-item important">
                            <span class="number">4.</span>
                            <p>All injuries, near misses, and dangerous occurrences must be <strong>reported immediately</strong> to the HR Department.</p>
                        </div>
                        <div class="procedure-item">
                            <span class="number">5.</span>
                            <p><strong>Incident reports</strong> must be prepared and shared with supervisor and manager.</p>
                        </div>
                    </div>
                </div>"""
            },
            {
                "title": "Training & Supervision",
                "content": """<div class="policy-page">
                    <h2>6. Training and Supervision</h2>
                    
                    <div class="training-section">
                        <div class="training-item">
                            <span class="number">6.1</span>
                            <p>All new employees must undergo <strong>safety induction training</strong>.</p>
                        </div>
                        <div class="training-item">
                            <span class="number">6.2</span>
                            <p><strong>Regular refresher training</strong> must be conducted for staff.</p>
                        </div>
                        <div class="training-item">
                            <span class="number">6.3</span>
                            <p><strong>Risk meetings</strong> must be held weekly to discuss risk and safety practices.</p>
                        </div>
                        <div class="training-item">
                            <span class="number">6.4</span>
                            <p>Supervisors must <strong>ensure compliance</strong> with all safety procedures.</p>
                        </div>
                    </div>
                    
                    <h2>7. Monitoring and Review</h2>
                    
                    <div class="monitoring-section">
                        <div class="monitoring-item">
                            <span class="number">7.1</span>
                            <p><strong>Risk assessment</strong> must be reviewed annually or after any incident.</p>
                        </div>
                        <div class="monitoring-item">
                            <span class="number">7.2</span>
                            <p>The policy will be <strong>reviewed and updated annually</strong> to reflect changes in law, operations, or risks.</p>
                        </div>
                    </div>
                </div>"""
            },
            {
                "title": "Penalties for Non-Compliance",
                "content": """<div class="policy-page">
                    <h2>8. Penalties for Non-Compliance</h2>
                    
                    <div class="legal-reference">
                        <p>In accordance with <strong>Section 118(2) of the Labour Act, 2003 (Act 651)</strong>, which requires employees to use safety appliances provided by the employer and follow safety instructions, Flowitec shall impose disciplinary actions for violations.</p>
                    </div>
                    
                    <div class="penalty-section">
                        <h3>8.1 Minor Infractions (First-time or low-risk violations)</h3>
                        <p class="examples">Examples: Not wearing PPE, unauthorized movement in restricted zones</p>
                        <ul>
                            <li>Verbal warning with documentation</li>
                            <li>Mandatory retraining on safety procedures</li>
                        </ul>
                    </div>
                    
                    <div class="penalty-section moderate">
                        <h3>8.2 Moderate Infractions (Repeated or moderately risky behavior)</h3>
                        <p class="examples">Examples: Repeated neglect of safety protocols, improper use of equipment</p>
                        <ul>
                            <li>Written warning placed in personnel file</li>
                            <li>Temporary suspension from hazardous duties</li>
                        </ul>
                    </div>
                    
                    <div class="penalty-section severe">
                        <h3>8.3 Major Infractions (High-risk or willful misconduct)</h3>
                        <p class="examples">Examples: Tampering with safety equipment, failure to report serious incidents</p>
                        <ul>
                            <li>Final written warning</li>
                            <li>Suspension without pay (not more than 10 days)</li>
                            <li>Termination of employment (subject to due process)</li>
                        </ul>
                    </div>
                </div>"""
            },
            {
                "title": "Roles & Responsibilities",
                "content": """<div class="policy-page">
                    <h2>Roles And Responsibilities</h2>
                    
                    <div class="role-section">
                        <h3>1. Management Must:</h3>
                        <ul>
                            <li>Conduct regular risk assessment and safety audits</li>
                            <li>Ensure appropriate PPE is provided and worn</li>
                            <li>Implement and enforce safe work procedures</li>
                            <li>Offer safety training and respond quickly to hazards and incident reports</li>
                        </ul>
                    </div>
                    
                    <div class="role-section">
                        <h3>2. Employees Must:</h3>
                        <ul>
                            <li>Follow safety procedures and wear PPE</li>
                            <li>Report hazards, near misses, and incidents immediately</li>
                            <li>Attend mandatory training and talks</li>
                            <li>Operate equipment only if trained and authorized</li>
                        </ul>
                    </div>
                    
                    <div class="role-section">
                        <h3>3. Visitors Must:</h3>
                        <ul>
                            <li>Follow all safety rules and signs</li>
                            <li>Be accompanied or supervised in operational areas</li>
                            <li>Report any unsafe conditions observed</li>
                        </ul>
                    </div>
                    
                    <div class="declaration-box">
                        <h3>11. Declaration</h3>
                        <p>Flowitec is committed to creating a culture where <strong>safety is a shared responsibility</strong>. All staff must actively contribute to identifying hazards, maintaining safety standards, and protecting the well-being of themselves and others.</p>
                    </div>
                </div>"""
            }
        ]
    }
]

# Career Beetle Data
CAREER_BEETLE = {
    "departments": [
        {
            "id": "sales",
            "name": "SALES",
            "roles": [
                {"id": "vp_sales", "title": "VP - Sales", "level": "Senior Mgt.", "key_skills": "Leadership, strategic sales planning, executive stakeholder management", "qualifications": "MBA/Masters, 10+ years sales leadership", "timeline": "N/A"},
                {"id": "country_sales_mgr", "title": "Country Sales Manager", "level": "First Level", "key_skills": "Leadership, sales strategy, business development, key account mgt", "qualifications": "Bachelor's/MBA, 7+ years", "timeline": "3-5 years"},
                {"id": "tech_sales_mgr", "title": "Technical Sales Manager", "level": "First Level", "key_skills": "Solutions sharing, competitor unseating strategies, technical advisory, leadership", "qualifications": "Engineering degree, 5+ years", "timeline": "3-4 years"},
                {"id": "sr_mech_sales_eng", "title": "Senior Mechanical Sales Engineer", "level": "Mid level", "key_skills": "Technical expertise, client relationship management, complex solutions", "qualifications": "Engineering degree, 4+ years", "timeline": "2-3 years"},
                {"id": "mech_sales_eng_assoc", "title": "Mechanical Sales Engineer Associate", "level": "Intermediate", "key_skills": "Product knowledge, customer service, basic technical support", "qualifications": "Engineering degree, 1-2 years", "timeline": "1-2 years"},
                {"id": "mech_sales_eng_trainee", "title": "Mechanical Sales Engineer Trainee", "level": "Entry level", "key_skills": "Learn products, shadow sales calls, understand client needs", "qualifications": "Engineering degree, Fresh graduate", "timeline": "6-12 months"},
                {"id": "biz_dev_mgr", "title": "Business Development Manager", "level": "Mid level", "key_skills": "Market analysis, partnership development, strategic planning", "qualifications": "Bachelor's degree, 3+ years", "timeline": "2-3 years"},
                {"id": "sales_admin", "title": "Sales Administrator", "level": "Entry level", "key_skills": "CRM basics, communication, administrative support", "qualifications": "Diploma/Bachelor's", "timeline": "1-2 years"}
            ]
        },
        {
            "id": "supply_chain",
            "name": "SUPPLY CHAIN",
            "roles": [
                {"id": "coo_supply", "title": "COO - Supply Chain", "level": "Senior Level", "key_skills": "Executive decision making, group logistics, digital transformation", "qualifications": "MBA, 15+ years", "timeline": "N/A"},
                {"id": "sr_procurement_mgr", "title": "Senior Procurement Manager", "level": "Senior Mgt.", "key_skills": "Leadership, strategic sourcing, risk management, contract negotiations", "qualifications": "MBA/Masters, 8+ years", "timeline": "4-5 years"},
                {"id": "procurement_mgr", "title": "Procurement Manager", "level": "First Level", "key_skills": "Advance excel, project management, good communication", "qualifications": "Bachelor's, 5+ years", "timeline": "3-4 years"},
                {"id": "sr_procurement_off", "title": "Senior Procurement Officer", "level": "Mid level", "key_skills": "Inventory controls, procurement basics, reporting and forecasting", "qualifications": "Bachelor's, 3+ years", "timeline": "2-3 years"},
                {"id": "procurement_off", "title": "Procurement Officer", "level": "Intermediate", "key_skills": "Basic sales and procurement knowledge", "qualifications": "Bachelor's, 1-2 years", "timeline": "1-2 years"},
                {"id": "procurement_trainee", "title": "Procurement Trainee", "level": "Entry level", "key_skills": "Learn procurement processes, documentation", "qualifications": "Bachelor's, Fresh graduate", "timeline": "6-12 months"}
            ]
        },
        {
            "id": "finance",
            "name": "FINANCE",
            "roles": [
                {"id": "cfo", "title": "CFO", "level": "Senior Level", "key_skills": "Strategic planning, Risk & compliance leadership, Executive decision making", "qualifications": "MBA/CPA/ACCA, 15+ years", "timeline": "N/A"},
                {"id": "finance_mgr", "title": "Finance Manager", "level": "Senior Mgt.", "key_skills": "Financial modeling, team coordination, regulatory and compliance", "qualifications": "CPA/ACCA, 8+ years", "timeline": "4-5 years"},
                {"id": "sr_accountant", "title": "Senior Accountant", "level": "First Level", "key_skills": "Financial reporting, budgeting & forecasting, cross-functional collaboration", "qualifications": "Bachelor's/CPA, 5+ years", "timeline": "3-4 years"},
                {"id": "accountant", "title": "Accountant", "level": "Mid level", "key_skills": "Advanced accounting, financial analysis, audit support", "qualifications": "Bachelor's, 3+ years", "timeline": "2-3 years"},
                {"id": "accounts_clerk", "title": "Accounts Clerk", "level": "Entry level", "key_skills": "Basic accounting principles, Excel proficiency, attention to detail", "qualifications": "Diploma/Bachelor's", "timeline": "1-2 years"}
            ]
        },
        {
            "id": "hr",
            "name": "HUMAN RESOURCE",
            "roles": [
                {"id": "hr_director", "title": "HR Director", "level": "Senior Level", "key_skills": "Strategic workforce planning, leadership coaching, change management and succession planning", "qualifications": "MBA/MHRM, 12+ years", "timeline": "N/A"},
                {"id": "hr_mgr", "title": "HR Manager", "level": "Senior Mgt.", "key_skills": "Talent Management, policy development, HR analytics & Compliance", "qualifications": "Bachelor's/Masters, 7+ years", "timeline": "4-5 years"},
                {"id": "sr_hr_off", "title": "Senior HR Officer", "level": "First Level", "key_skills": "Recruitment & onboarding, benefits administration, employee relations", "qualifications": "Bachelor's, 4+ years", "timeline": "2-3 years"},
                {"id": "hr_off", "title": "HR Officer", "level": "Mid level", "key_skills": "HRIS, record keeping, understanding of HR policies and procedures", "qualifications": "Bachelor's, 2+ years", "timeline": "1-2 years"},
                {"id": "hr_assistant", "title": "HR Assistant", "level": "Entry level", "key_skills": "Administrative support, documentation, basic HR knowledge", "qualifications": "Diploma/Bachelor's", "timeline": "1 year"}
            ]
        },
        {
            "id": "facilities",
            "name": "FACILITIES",
            "roles": [
                {"id": "facilities_mgr", "title": "Facilities Manager", "level": "Senior Mgt.", "key_skills": "Facilities strategy, health and safety compliance, office space planning", "qualifications": "Bachelor's, 7+ years", "timeline": "N/A"},
                {"id": "facilities_super", "title": "Facilities Supervisor", "level": "First Level", "key_skills": "Team leadership, General maintenance coordination", "qualifications": "Diploma, 4+ years", "timeline": "3-4 years"},
                {"id": "facilities_off", "title": "Facilities Officer", "level": "Mid level", "key_skills": "Basic office supplies stocking, maintaining functioning devices", "qualifications": "Diploma, 2+ years", "timeline": "2 years"},
                {"id": "chief_driver", "title": "Chief Driver", "level": "First Level", "key_skills": "Team supervisor, route planning, fleet compliance", "qualifications": "Valid license, 5+ years", "timeline": "3-4 years"},
                {"id": "driver", "title": "Driver", "level": "Entry level", "key_skills": "Vehicle maintenance, road safety and company policies, route optimization", "qualifications": "Valid license", "timeline": "2-3 years"}
            ]
        }
    ]
}

async def reset_and_seed():
    print("Starting database reset and seed...")
    
    # Delete all existing courses, modules, lessons, progress, quizzes
    print("Deleting existing course data...")
    await db.courses.delete_many({})
    await db.modules.delete_many({})
    await db.lessons.delete_many({})
    await db.quizzes.delete_many({})
    # Don't delete progress - users might want to keep their history
    
    # Reset user enrollments
    await db.users.update_many({}, {"$set": {"enrolled_courses": [], "completed_courses": []}})
    await db.progress.delete_many({})
    await db.certificates.delete_many({})
    
    print("Creating new courses with page-based content...")
    
    for course_data in COURSES:
        pages = course_data.pop("pages")
        course_data["enrolled_users"] = []
        course_data["created_at"] = datetime.now(timezone.utc).isoformat()
        
        # Insert course
        await db.courses.insert_one(course_data)
        print(f"  Created course: {course_data['title']}")
        
        # Create a single module for each course
        module_id = str(uuid.uuid4())
        module = {
            "id": module_id,
            "course_id": course_data["id"],
            "title": "Course Content",
            "description": f"Complete content for {course_data['title']}",
            "order": 0,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.modules.insert_one(module)
        
        # Create lessons from pages
        for i, page in enumerate(pages):
            lesson_id = str(uuid.uuid4())
            lesson = {
                "id": lesson_id,
                "module_id": module_id,
                "title": page["title"],
                "content_type": "text",  # HTML content rendered as text/rich content
                "content": page["content"],
                "duration_minutes": 5,
                "order": i,
                "page_number": i + 1,
                "total_pages": len(pages),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await db.lessons.insert_one(lesson)
        
        print(f"    Created {len(pages)} pages for {course_data['title']}")
    
    # Save Career Beetle data
    print("Setting up Career Beetle data...")
    await db.career_beetle.delete_many({})
    await db.career_beetle.insert_one(CAREER_BEETLE)
    print("  Career Beetle data saved")
    
    print("\nDatabase reset and seed complete!")
    print(f"Created {len(COURSES)} courses with page-based content")
    print("Career Beetle succession plan configured")

if __name__ == "__main__":
    asyncio.run(reset_and_seed())
