"""
Flowitec Go & Grow LMS - Policy Courses Restoration
Restores the 4 required policy courses with 20+ pages each
"""

import uuid
from datetime import datetime, timezone

async def restore_policy_courses(db):
    """Restore the 4 required policy courses with comprehensive content (20+ pages each)"""
    
    print("Restoring 4 required policy courses...")
    
    # Course 1: Leave Policy - Ghana (20+ pages)
    leave_course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": leave_course_id,
        "title": "Leave Policy - Ghana",
        "description": "Comprehensive guide to Flowitec's leave policies in Ghana, covering annual leave, sick leave, maternity/paternity leave, and all other types of employee leave entitlements.",
        "thumbnail": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 8,
        "is_published": True,
        "course_type": "required",
        "code": "POL-LV-001",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    leave_modules = [
        {
            "title": "Module 1: Introduction to Leave Policy",
            "lessons": [
                ("Introduction to Flowitec Leave Policy", """<div class="lesson-content">
<h2>Welcome to Flowitec Leave Policy Training</h2>
<p>This course provides a comprehensive overview of Flowitec Ghana's leave policies. Understanding these policies ensures you can plan your time off effectively while maintaining operational efficiency.</p>

<div class="highlight-box">
<h3>Why Leave Policies Matter</h3>
<p>Leave policies serve multiple important purposes:</p>
<ul>
<li><strong>Employee Well-being:</strong> Regular time off is essential for physical and mental health</li>
<li><strong>Work-Life Balance:</strong> Enables employees to attend to personal and family needs</li>
<li><strong>Legal Compliance:</strong> Ensures Flowitec meets Ghana Labour Act requirements</li>
<li><strong>Operational Planning:</strong> Helps managers plan workload and coverage</li>
</ul>
</div>

<h3>Scope of This Policy</h3>
<p>This leave policy applies to all Flowitec Ghana employees, including:</p>
<ul>
<li>Permanent full-time employees</li>
<li>Permanent part-time employees</li>
<li>Contract employees (where specified)</li>
<li>Probationary employees (with certain limitations)</li>
</ul>

<div class="info-box">
<h4>Key Principle</h4>
<p>Flowitec believes that well-rested employees are more productive, creative, and engaged. We encourage all employees to take their entitled leave.</p>
</div>
</div>"""),
                ("Legal Framework - Ghana Labour Act", """<div class="lesson-content">
<h2>Legal Framework: Ghana Labour Act 2003 (Act 651)</h2>
<p>Flowitec's leave policies are designed to meet or exceed the requirements of the Ghana Labour Act 2003 (Act 651) and subsequent amendments.</p>

<h3>Key Legal Requirements</h3>
<table class="info-table">
<tr><th>Leave Type</th><th>Legal Minimum</th><th>Flowitec Provision</th></tr>
<tr><td>Annual Leave</td><td>15 working days</td><td>21 working days</td></tr>
<tr><td>Sick Leave</td><td>As certified by medical practitioner</td><td>Up to 30 days paid</td></tr>
<tr><td>Maternity Leave</td><td>12 weeks</td><td>14 weeks fully paid</td></tr>
<tr><td>Public Holidays</td><td>13 days</td><td>13 days + additional company days</td></tr>
</table>

<h3>Section 20 - Annual Leave</h3>
<div class="highlight-box">
<p>The Ghana Labour Act states:</p>
<blockquote>"Every worker is entitled to not less than fifteen working days leave with full pay in any calendar year of continuous service."</blockquote>
<p>Flowitec exceeds this by providing 21 working days.</p>
</div>

<h3>Section 57 - Maternity Leave</h3>
<p>The Act provides for maternity protection including:</p>
<ul>
<li>Minimum 12 weeks maternity leave</li>
<li>Protection from dismissal during pregnancy</li>
<li>Right to return to same or equivalent position</li>
</ul>

<div class="info-box">
<h4>Important Note</h4>
<p>This policy may be updated to reflect changes in Ghana labour law. Always refer to the latest version available on the HR portal.</p>
</div>
</div>"""),
                ("Your Rights and Responsibilities", """<div class="lesson-content">
<h2>Employee Rights and Responsibilities</h2>
<p>Understanding your rights and responsibilities regarding leave helps ensure smooth operations and fair treatment for all employees.</p>

<h3>Your Rights</h3>
<div class="rights-section">
<div class="right-card">
<h4>Right to Leave</h4>
<p>You have the legal right to take your entitled leave. Management cannot unreasonably deny leave requests.</p>
</div>

<div class="right-card">
<h4>Right to Pay</h4>
<p>Annual leave and most other leave types are paid at your normal rate of remuneration.</p>
</div>

<div class="right-card">
<h4>Right to Privacy</h4>
<p>Medical information provided for sick leave is confidential and handled only by authorized HR personnel.</p>
</div>

<div class="right-card">
<h4>Right to Appeal</h4>
<p>If your leave request is denied, you have the right to appeal through HR.</p>
</div>
</div>

<h3>Your Responsibilities</h3>
<div class="responsibilities-section">
<ul>
<li><strong>Advance Notice:</strong> Submit leave requests with adequate notice (minimum 2 weeks for annual leave)</li>
<li><strong>Handover:</strong> Ensure proper handover of duties before taking leave</li>
<li><strong>Documentation:</strong> Provide required documentation (medical certificates, etc.)</li>
<li><strong>Communication:</strong> Remain contactable for emergencies during leave</li>
<li><strong>Return:</strong> Return to work on the scheduled date or communicate any changes</li>
</ul>
</div>

<div class="highlight-box">
<h4>Manager Responsibilities</h4>
<p>Managers must:</p>
<ul>
<li>Approve leave requests fairly and consistently</li>
<li>Plan for adequate coverage during employee absence</li>
<li>Not contact employees on leave except for genuine emergencies</li>
<li>Support employees in taking their full leave entitlement</li>
</ul>
</div>
</div>"""),
                ("Leave Year and Accrual", """<div class="lesson-content">
<h2>Leave Year and Accrual System</h2>
<p>Understanding how leave is calculated and accrued helps you plan your time off effectively.</p>

<h3>The Leave Year</h3>
<p>Flowitec operates on a <strong>calendar year leave cycle</strong> (January 1 to December 31). Your leave entitlement is calculated based on this period.</p>

<h3>How Leave Accrues</h3>
<div class="accrual-info">
<h4>Annual Leave Accrual</h4>
<p>Your 21 days annual leave accrues throughout the year:</p>
<ul>
<li>Monthly accrual: 1.75 days per month</li>
<li>You can take accrued leave at any time (subject to approval)</li>
<li>New employees accrue leave from their start date</li>
</ul>

<table class="info-table">
<tr><th>Month</th><th>Accrued Days (Cumulative)</th></tr>
<tr><td>January</td><td>1.75 days</td></tr>
<tr><td>March</td><td>5.25 days</td></tr>
<tr><td>June</td><td>10.5 days</td></tr>
<tr><td>September</td><td>15.75 days</td></tr>
<tr><td>December</td><td>21 days</td></tr>
</table>
</div>

<h3>Carry Over Policy</h3>
<div class="highlight-box">
<p><strong>Maximum Carry Over:</strong> 5 days</p>
<p>Employees may carry over a maximum of 5 unused annual leave days to the following year. These must be used by March 31 or they will be forfeited.</p>
<p>Unused days beyond the 5-day limit are forfeited at year end. Plan your leave to avoid losing days!</p>
</div>

<h3>Pro-Rata Calculation for New Employees</h3>
<p>If you join Flowitec mid-year, your annual leave is calculated pro-rata:</p>
<p><em>Example: Employee joins July 1 = 6 months remaining = 10.5 days entitlement</em></p>

<div class="info-box">
<h4>Check Your Balance</h4>
<p>You can check your current leave balance anytime through the HR Portal or by contacting HR.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 2: Annual Leave",
            "lessons": [
                ("Annual Leave Entitlement", """<div class="lesson-content">
<h2>Annual Leave Entitlement</h2>
<p>Annual leave is your primary paid time off for rest, recreation, and personal activities.</p>

<h3>Entitlement by Grade</h3>
<table class="info-table">
<tr><th>Employee Grade</th><th>Annual Leave Days</th><th>Notes</th></tr>
<tr><td>Entry Level (Grade 1-3)</td><td>21 days</td><td>Standard entitlement</td></tr>
<tr><td>Professional (Grade 4-6)</td><td>21 days</td><td>Standard entitlement</td></tr>
<tr><td>Senior Professional (Grade 7-9)</td><td>25 days</td><td>Increased entitlement</td></tr>
<tr><td>Management (Grade 10+)</td><td>28 days</td><td>Maximum entitlement</td></tr>
</table>

<h3>Service-Based Increases</h3>
<p>Long-serving employees receive additional leave:</p>
<ul>
<li><strong>5+ years of service:</strong> +2 additional days</li>
<li><strong>10+ years of service:</strong> +4 additional days (cumulative)</li>
<li><strong>15+ years of service:</strong> +6 additional days (cumulative)</li>
</ul>

<div class="highlight-box">
<h4>Example Calculation</h4>
<p>A Grade 5 employee with 12 years of service:</p>
<ul>
<li>Base entitlement: 21 days</li>
<li>10+ years bonus: +4 days</li>
<li><strong>Total: 25 days annual leave</strong></li>
</ul>
</div>

<h3>Probationary Period</h3>
<p>During probation (typically 3-6 months):</p>
<ul>
<li>Leave accrues but taking leave is discouraged except for emergencies</li>
<li>Any leave taken may extend the probation period</li>
<li>Upon confirmation, full accrued leave becomes available</li>
</ul>
</div>"""),
                ("Requesting Annual Leave", """<div class="lesson-content">
<h2>How to Request Annual Leave</h2>
<p>Follow this process to ensure your leave request is processed smoothly.</p>

<h3>Step-by-Step Process</h3>
<div class="process-steps">
<div class="step">
<span class="step-num">1</span>
<h4>Check Your Balance</h4>
<p>Log into the HR Portal and verify you have sufficient leave days available.</p>
</div>

<div class="step">
<span class="step-num">2</span>
<h4>Plan Your Leave</h4>
<p>Consider project deadlines, team coverage, and peak periods before selecting dates.</p>
</div>

<div class="step">
<span class="step-num">3</span>
<h4>Submit Request</h4>
<p>Submit your request through the HR Portal at least 2 weeks in advance (4 weeks for leave exceeding 5 days).</p>
</div>

<div class="step">
<span class="step-num">4</span>
<h4>Manager Approval</h4>
<p>Your manager will review and approve/decline within 3 working days.</p>
</div>

<div class="step">
<span class="step-num">5</span>
<h4>Confirmation</h4>
<p>You'll receive email confirmation once approved. Add to your calendar.</p>
</div>

<div class="step">
<span class="step-num">6</span>
<h4>Handover</h4>
<p>Complete handover document and brief colleagues on urgent matters.</p>
</div>
</div>

<h3>Notice Requirements</h3>
<table class="info-table">
<tr><th>Leave Duration</th><th>Notice Required</th></tr>
<tr><td>1-2 days</td><td>5 working days</td></tr>
<tr><td>3-5 days</td><td>2 weeks</td></tr>
<tr><td>6-10 days</td><td>4 weeks</td></tr>
<tr><td>More than 10 days</td><td>6 weeks</td></tr>
</table>

<div class="info-box">
<h4>Emergency Leave</h4>
<p>In genuine emergencies, leave may be granted with shorter notice at manager's discretion.</p>
</div>
</div>"""),
                ("Peak Periods and Restrictions", """<div class="lesson-content">
<h2>Peak Periods and Leave Restrictions</h2>
<p>Some periods have restrictions on leave to ensure business continuity.</p>

<h3>Restricted Periods</h3>
<div class="restricted-periods">
<div class="period-card">
<h4>Year-End Close (December 15 - January 5)</h4>
<p>Finance and Accounting teams have restricted leave during year-end closing. Only emergency leave will be approved.</p>
</div>

<div class="period-card">
<h4>Annual Audit Period (Varies)</h4>
<p>Staff directly involved in annual audit may have leave restricted during audit weeks. HR will communicate dates.</p>
</div>

<div class="period-card">
<h4>Major Project Milestones</h4>
<p>Managers may restrict leave during critical project phases. This should be communicated in advance.</p>
</div>
</div>

<h3>Team Coverage Requirements</h3>
<p>To ensure operational continuity:</p>
<ul>
<li>Maximum 30% of any team on leave simultaneously</li>
<li>At least one senior team member must be present</li>
<li>Critical roles must have designated backup coverage</li>
</ul>

<h3>Popular Periods - Plan Ahead!</h3>
<div class="highlight-box">
<h4>High Demand Periods</h4>
<p>These periods have high leave demand - submit requests early:</p>
<ul>
<li>Christmas/New Year (December-January)</li>
<li>Easter Week</li>
<li>Independence Day (March 6)</li>
<li>School Holidays (July-August)</li>
</ul>
<p>Requests for these periods are approved on a first-come, first-served basis.</p>
</div>

<h3>Fair Allocation</h3>
<p>If multiple team members request the same dates:</p>
<ol>
<li>First-come, first-served applies</li>
<li>Employees who didn't get preferred dates last year have priority</li>
<li>Rotation system ensures fairness over multiple years</li>
</ol>
</div>"""),
                ("Annual Leave Payment", """<div class="lesson-content">
<h2>Annual Leave Payment</h2>
<p>Understanding how you're paid during annual leave.</p>

<h3>Payment During Leave</h3>
<p>During annual leave, you receive your <strong>normal salary</strong> including:</p>
<ul>
<li>Basic salary</li>
<li>Fixed allowances (housing, transport, etc.)</li>
<li>Any guaranteed bonuses</li>
</ul>

<p><strong>Not included:</strong></p>
<ul>
<li>Overtime payments</li>
<li>Performance bonuses (unless guaranteed)</li>
<li>Commission (for sales roles)</li>
</ul>

<h3>Leave Allowance</h3>
<div class="highlight-box">
<h4>Annual Leave Allowance</h4>
<p>Flowitec provides a leave allowance to help employees enjoy their annual leave:</p>
<table class="info-table">
<tr><th>Grade Level</th><th>Leave Allowance</th></tr>
<tr><td>Grade 1-3</td><td>GHS 500</td></tr>
<tr><td>Grade 4-6</td><td>GHS 1,000</td></tr>
<tr><td>Grade 7-9</td><td>GHS 1,500</td></tr>
<tr><td>Grade 10+</td><td>GHS 2,500</td></tr>
</table>
<p>This is paid once per year when you take your main annual leave (minimum 5 consecutive days).</p>
</div>

<h3>Payment Upon Termination</h3>
<p>If your employment ends:</p>
<ul>
<li>Accrued but unused leave is paid out in your final settlement</li>
<li>Calculation: (Daily rate) × (Unused leave days)</li>
<li>Leave taken in excess of accrued amount may be deducted</li>
</ul>

<div class="info-box">
<h4>No Cash-Out During Employment</h4>
<p>Flowitec does not allow cashing out annual leave instead of taking time off. Leave is for rest and recuperation - please use it!</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 3: Sick Leave",
            "lessons": [
                ("Sick Leave Entitlement", """<div class="lesson-content">
<h2>Sick Leave Entitlement</h2>
<p>Flowitec provides sick leave to support employees during illness or medical treatment.</p>

<h3>Sick Leave Allowance</h3>
<table class="info-table">
<tr><th>Category</th><th>Paid Days</th><th>Additional Provisions</th></tr>
<tr><td>Short-term illness</td><td>15 days at full pay</td><td>Per calendar year</td></tr>
<tr><td>Extended illness</td><td>15 days at half pay</td><td>After first 15 days exhausted</td></tr>
<tr><td>Serious illness</td><td>Case-by-case</td><td>May qualify for disability benefits</td></tr>
</table>

<h3>Medical Certificate Requirements</h3>
<div class="requirements-section">
<h4>When Certificate is Required</h4>
<ul>
<li>Any sick leave exceeding <strong>2 consecutive days</strong></li>
<li>Sick leave taken immediately before or after a weekend/holiday</li>
<li>Pattern of frequent short sick leaves</li>
<li>Any sick leave during probation period</li>
</ul>

<h4>Acceptable Medical Certificates</h4>
<ul>
<li>From registered medical practitioner</li>
<li>From Flowitec's designated clinic</li>
<li>From government hospital/health center</li>
<li>Specialist certificates for specific conditions</li>
</ul>
</div>

<h3>Self-Certification</h3>
<div class="highlight-box">
<p>For sick leave of 1-2 days, you may self-certify using the HR Portal. You must:</p>
<ul>
<li>Submit the self-certification form within 24 hours of return</li>
<li>Briefly describe the nature of illness</li>
<li>Confirm you are fit to return to work</li>
</ul>
<p><strong>Limit:</strong> Maximum 6 self-certified sick days per year. Beyond this, medical certificates are required.</p>
</div>

<div class="info-box">
<h4>Abuse of Sick Leave</h4>
<p>Abuse of sick leave is a disciplinary offense. This includes false claims, pattern absences, or working elsewhere during sick leave.</p>
</div>
</div>"""),
                ("Reporting Sick Leave", """<div class="lesson-content">
<h2>How to Report Sick Leave</h2>
<p>Timely communication is essential when you're unwell.</p>

<h3>Notification Timeline</h3>
<div class="timeline-box">
<div class="timeline-item">
<h4>Before Work Starts</h4>
<p>Notify your manager <strong>before your normal start time</strong> on the first day of absence. If you can't call, send SMS/WhatsApp and follow up when possible.</p>
</div>

<div class="timeline-item">
<h4>Daily Updates</h4>
<p>For extended illness, provide daily updates until you can estimate return date.</p>
</div>

<div class="timeline-item">
<h4>Return to Work</h4>
<p>Confirm your return date at least one day in advance.</p>
</div>
</div>

<h3>Who to Contact</h3>
<ol>
<li><strong>Primary:</strong> Your direct manager (phone/SMS)</li>
<li><strong>Secondary:</strong> Team lead or department head</li>
<li><strong>Also notify:</strong> HR department (email or portal)</li>
</ol>

<h3>Information to Provide</h3>
<ul>
<li>Nature of illness (general description is sufficient)</li>
<li>Expected duration of absence</li>
<li>Any urgent work that needs coverage</li>
<li>How you can be reached in emergency</li>
</ul>

<h3>Work Coverage During Absence</h3>
<div class="highlight-box">
<h4>Your Responsibilities</h4>
<p>If possible (and health permits), before going on sick leave:</p>
<ul>
<li>Set out-of-office email reply</li>
<li>Forward urgent emails to colleague</li>
<li>Brief someone on critical pending tasks</li>
<li>Update voicemail if applicable</li>
</ul>
</div>

<div class="info-box">
<h4>No Work During Sick Leave</h4>
<p>When on sick leave, you should focus on recovery. Do not check emails or attend meetings unless absolutely critical and your health permits.</p>
</div>
</div>"""),
                ("Return to Work Process", """<div class="lesson-content">
<h2>Returning to Work After Sick Leave</h2>
<p>A proper return-to-work process ensures you're ready to resume duties safely.</p>

<h3>Return to Work Meeting</h3>
<p>After sick leave exceeding 5 days, a return-to-work meeting with your manager is required to:</p>
<ul>
<li>Confirm you're fit to return</li>
<li>Discuss any ongoing health concerns</li>
<li>Identify any workplace adjustments needed</li>
<li>Brief you on developments during your absence</li>
</ul>

<h3>Fitness for Duty</h3>
<div class="fitness-section">
<h4>When Medical Clearance is Required</h4>
<ul>
<li>Sick leave exceeding 10 consecutive days</li>
<li>Following hospitalization</li>
<li>After infectious disease (COVID-19, etc.)</li>
<li>Following work-related injury or illness</li>
<li>Mental health related absence</li>
</ul>
</div>

<h3>Phased Return</h3>
<div class="highlight-box">
<h4>Gradual Return to Work</h4>
<p>After serious illness, a phased return may be appropriate:</p>
<ul>
<li>Week 1: 50% hours</li>
<li>Week 2: 75% hours</li>
<li>Week 3+: Full hours</li>
</ul>
<p>This must be agreed with HR and supported by medical recommendation.</p>
</div>

<h3>Workplace Adjustments</h3>
<p>Temporary or permanent adjustments may include:</p>
<ul>
<li>Modified duties</li>
<li>Flexible working hours</li>
<li>Ergonomic equipment</li>
<li>Work from home arrangements</li>
<li>Reduced workload initially</li>
</ul>

<div class="info-box">
<h4>Confidentiality</h4>
<p>Details of your illness are confidential. Only information necessary for work adjustments will be shared with your manager, and only with your consent.</p>
</div>
</div>"""),
                ("Chronic Illness and Long-Term Conditions", """<div class="lesson-content">
<h2>Managing Chronic and Long-Term Conditions</h2>
<p>Flowitec supports employees with chronic health conditions to remain productive at work.</p>

<h3>What is a Chronic Condition?</h3>
<p>Conditions lasting more than 3 months or requiring ongoing management:</p>
<ul>
<li>Diabetes</li>
<li>Hypertension</li>
<li>Asthma</li>
<li>HIV/AIDS</li>
<li>Mental health conditions (depression, anxiety)</li>
<li>Autoimmune conditions</li>
<li>Cancer (during/after treatment)</li>
</ul>

<h3>Support Available</h3>
<div class="support-section">
<div class="support-card">
<h4>Medical Appointments</h4>
<p>Time off for regular medical appointments related to your condition. Provide appointment evidence to HR.</p>
</div>

<div class="support-card">
<h4>Flexible Working</h4>
<p>Adjusted hours or work-from-home arrangements to manage your condition.</p>
</div>

<div class="support-card">
<h4>Health Insurance Coverage</h4>
<p>Flowitec's health insurance covers chronic condition management including medications.</p>
</div>

<div class="support-card">
<h4>Counseling Services</h4>
<p>Access to Employee Assistance Program (EAP) for mental health support.</p>
</div>
</div>

<h3>Disclosure</h3>
<div class="highlight-box">
<h4>Your Choice</h4>
<p>You are not required to disclose your health condition unless:</p>
<ul>
<li>It affects your ability to perform essential job functions</li>
<li>It poses a safety risk to yourself or others</li>
<li>You need workplace accommodations</li>
</ul>
<p>Any disclosure is treated confidentially and without discrimination.</p>
</div>

<h3>Non-Discrimination Policy</h3>
<p>Flowitec will not discriminate against employees with chronic conditions. All employment decisions are based on ability to perform job functions, with reasonable accommodations where needed.</p>

<div class="info-box">
<h4>Support Contact</h4>
<p>For confidential discussion about managing a health condition at work, contact HR or the Employee Wellness Coordinator.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 4: Maternity and Paternity Leave",
            "lessons": [
                ("Maternity Leave Entitlement", """<div class="lesson-content">
<h2>Maternity Leave Entitlement</h2>
<p>Flowitec provides generous maternity leave to support expectant and new mothers.</p>

<h3>Entitlement</h3>
<div class="highlight-box">
<h4>Maternity Leave Package</h4>
<table class="info-table">
<tr><td><strong>Duration</strong></td><td>14 weeks (98 calendar days)</td></tr>
<tr><td><strong>Payment</strong></td><td>100% of basic salary throughout</td></tr>
<tr><td><strong>Start</strong></td><td>Up to 4 weeks before expected delivery</td></tr>
<tr><td><strong>Extension</strong></td><td>Up to 4 weeks unpaid if needed</td></tr>
</table>
</div>

<h3>Eligibility</h3>
<p>All female employees are entitled to maternity leave:</p>
<ul>
<li>Permanent employees: Full entitlement from day one</li>
<li>Contract employees: Pro-rata based on contract terms</li>
<li>Probationary employees: Full entitlement (probation extended)</li>
</ul>

<h3>Timing Your Leave</h3>
<p>You may begin maternity leave:</p>
<ul>
<li><strong>Earliest:</strong> 4 weeks before expected delivery date</li>
<li><strong>Latest:</strong> Date of delivery (medical recommendation required for late start)</li>
<li><strong>Typical:</strong> Most employees begin 2 weeks before expected date</li>
</ul>

<h3>Multiple Births</h3>
<p>For twins or multiple births:</p>
<ul>
<li>Additional 2 weeks leave (total 16 weeks)</li>
<li>Full pay throughout extended period</li>
</ul>

<div class="info-box">
<h4>Pregnancy Loss</h4>
<p>In the unfortunate event of pregnancy loss after 28 weeks, employees are entitled to 6 weeks paid leave and access to counseling support.</p>
</div>
</div>"""),
                ("Applying for Maternity Leave", """<div class="lesson-content">
<h2>Maternity Leave Application Process</h2>
<p>Plan ahead to ensure smooth transition during your maternity leave.</p>

<h3>Timeline</h3>
<div class="timeline-process">
<div class="timeline-item">
<h4>As Soon As Possible</h4>
<p>Inform your manager and HR of your pregnancy when you feel comfortable. This allows for planning and ensures you receive all support.</p>
</div>

<div class="timeline-item">
<h4>12 Weeks Before Leave</h4>
<p>Submit formal maternity leave application through HR Portal with:</p>
<ul>
<li>Expected delivery date (medical certificate)</li>
<li>Requested leave start date</li>
<li>Expected return date</li>
</ul>
</div>

<div class="timeline-item">
<h4>4-6 Weeks Before Leave</h4>
<p>Complete handover plan and brief your replacement/cover.</p>
</div>

<div class="timeline-item">
<h4>During Leave</h4>
<p>Notify HR of actual delivery date and confirm return date.</p>
</div>
</div>

<h3>Required Documentation</h3>
<ul>
<li>Medical certificate confirming pregnancy and expected delivery date</li>
<li>Completed maternity leave form</li>
<li>Bank details for salary payment during leave</li>
</ul>

<h3>Prenatal Appointments</h3>
<div class="highlight-box">
<p>You are entitled to paid time off for prenatal medical appointments. Simply:</p>
<ul>
<li>Give your manager advance notice</li>
<li>Provide appointment card/evidence</li>
<li>Time is not deducted from leave or sick leave</li>
</ul>
</div>

<h3>Handover Preparation</h3>
<p>Before starting maternity leave:</p>
<ol>
<li>Document ongoing projects and status</li>
<li>Brief colleagues or replacement</li>
<li>Set out-of-office messages</li>
<li>Provide emergency contact if willing</li>
<li>Complete any time-sensitive deliverables</li>
</ol>
</div>"""),
                ("Paternity Leave", """<div class="lesson-content">
<h2>Paternity Leave</h2>
<p>Flowitec recognizes the importance of fathers being present for their new child.</p>

<h3>Paternity Leave Entitlement</h3>
<div class="highlight-box">
<table class="info-table">
<tr><td><strong>Duration</strong></td><td>10 working days</td></tr>
<tr><td><strong>Payment</strong></td><td>100% of basic salary</td></tr>
<tr><td><strong>Timing</strong></td><td>Within 4 weeks of birth</td></tr>
<tr><td><strong>Flexibility</strong></td><td>Can be taken in two blocks</td></tr>
</table>
</div>

<h3>Eligibility</h3>
<p>Available to:</p>
<ul>
<li>Biological fathers</li>
<li>Adoptive fathers (upon adoption finalization)</li>
<li>Same-sex partners (where legal parent status is established)</li>
</ul>

<h3>Application Process</h3>
<ol>
<li>Notify manager and HR when expecting</li>
<li>Submit paternity leave form through HR Portal</li>
<li>Provide birth certificate/adoption papers upon return</li>
</ol>

<h3>Timing Options</h3>
<p>The 10 days can be taken:</p>
<ul>
<li><strong>Option A:</strong> All 10 days consecutively around birth</li>
<li><strong>Option B:</strong> 5 days at birth + 5 days within first month</li>
</ul>

<div class="info-box">
<h4>Additional Support</h4>
<p>New fathers may also request flexible working arrangements during the first 3 months after birth. Discuss with your manager and HR.</p>
</div>
</div>"""),
                ("Return from Parental Leave", """<div class="lesson-content">
<h2>Returning from Parental Leave</h2>
<p>Flowitec supports employees returning to work after becoming parents.</p>

<h3>Your Rights on Return</h3>
<div class="rights-section">
<ul>
<li><strong>Same Role:</strong> You have the right to return to the same position</li>
<li><strong>Same Terms:</strong> No reduction in salary or benefits</li>
<li><strong>Same Seniority:</strong> Continuous service for all calculations</li>
</ul>
</div>

<h3>Nursing Mothers</h3>
<div class="highlight-box">
<h4>Breastfeeding Support</h4>
<p>For 6 months after returning from maternity leave:</p>
<ul>
<li>Two 30-minute breaks daily for breastfeeding/expressing</li>
<li>Access to private nursing room</li>
<li>Refrigerator for storing expressed milk</li>
</ul>
<p>These breaks are paid and in addition to normal breaks.</p>
</div>

<h3>Flexible Return Options</h3>
<p>To support work-life balance with a new baby:</p>
<ul>
<li><strong>Phased return:</strong> Gradual increase to full hours over 4 weeks</li>
<li><strong>Flexible hours:</strong> Adjusted start/end times</li>
<li><strong>Work from home:</strong> Partial WFH arrangements (role dependent)</li>
<li><strong>Part-time:</strong> Temporary reduction in hours (salary pro-rata)</li>
</ul>

<h3>Keeping in Touch Days</h3>
<p>During maternity leave, you may work up to 10 "Keeping in Touch" (KIT) days:</p>
<ul>
<li>Paid at normal rate</li>
<li>Voluntary (not mandatory)</li>
<li>Helps maintain connection and ease return</li>
<li>Does not affect your maternity leave or pay</li>
</ul>

<div class="info-box">
<h4>Childcare Support</h4>
<p>Flowitec provides childcare information and may offer subsidized access to partner childcare facilities. Contact HR for current offerings.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 5: Other Types of Leave",
            "lessons": [
                ("Compassionate and Bereavement Leave", """<div class="lesson-content">
<h2>Compassionate and Bereavement Leave</h2>
<p>Flowitec provides leave during times of family loss or serious illness.</p>

<h3>Bereavement Leave Entitlement</h3>
<table class="info-table">
<tr><th>Relationship</th><th>Paid Leave Days</th></tr>
<tr><td>Spouse/Partner</td><td>10 days</td></tr>
<tr><td>Child</td><td>10 days</td></tr>
<tr><td>Parent</td><td>7 days</td></tr>
<tr><td>Sibling</td><td>5 days</td></tr>
<tr><td>Grandparent</td><td>3 days</td></tr>
<tr><td>In-Laws (parent)</td><td>3 days</td></tr>
<tr><td>Extended Family</td><td>1 day</td></tr>
</table>

<h3>Requesting Bereavement Leave</h3>
<ul>
<li>Notify your manager immediately</li>
<li>Formal documentation can follow your return</li>
<li>No advance notice required (emergency nature)</li>
</ul>

<h3>Compassionate Leave</h3>
<p>For serious illness of immediate family members:</p>
<ul>
<li>Up to 5 days paid leave per incident</li>
<li>For caring responsibilities during critical illness</li>
<li>May be extended with unpaid leave if needed</li>
</ul>

<div class="highlight-box">
<h4>Additional Support</h4>
<p>During bereavement, you also have access to:</p>
<ul>
<li>Employee Assistance Program (counseling)</li>
<li>Flexible return arrangements</li>
<li>Extended unpaid leave if needed</li>
</ul>
</div>

<h3>Traditional Observances</h3>
<p>For employees with cultural/religious observance requirements:</p>
<ul>
<li>Additional time may be granted for traditional funeral rites</li>
<li>Discuss with HR for arrangements</li>
<li>May use annual leave or unpaid leave for extended periods</li>
</ul>
</div>"""),
                ("Study Leave and Examination Leave", """<div class="lesson-content">
<h2>Study and Examination Leave</h2>
<p>Flowitec supports employee professional development through study leave provisions.</p>

<h3>Approved Study Programs</h3>
<p>Study leave is available for:</p>
<ul>
<li>Job-related professional certifications</li>
<li>Degree programs approved by Flowitec</li>
<li>Industry qualifications (engineering, accounting, etc.)</li>
<li>Management and leadership programs</li>
</ul>

<h3>Study Leave Entitlement</h3>
<div class="highlight-box">
<table class="info-table">
<tr><th>Purpose</th><th>Leave Entitlement</th></tr>
<tr><td>Examination days</td><td>Day of exam + 1 day before (paid)</td></tr>
<tr><td>Study block release</td><td>As per program requirements (agreed in advance)</td></tr>
<tr><td>Thesis/dissertation</td><td>Up to 10 days (for final year students)</td></tr>
</table>
</div>

<h3>Eligibility Requirements</h3>
<ul>
<li>Completed 1 year of service with Flowitec</li>
<li>Program must be pre-approved by manager and HR</li>
<li>Relevance to current or future role</li>
<li>Commitment to remain with Flowitec for specified period after completion</li>
</ul>

<h3>Application Process</h3>
<ol>
<li>Discuss educational goals with manager</li>
<li>Submit study assistance application to HR</li>
<li>Upon approval, submit exam timetable</li>
<li>Request specific study leave dates</li>
</ol>

<div class="info-box">
<h4>Study Assistance Program</h4>
<p>In addition to study leave, Flowitec offers financial support for approved programs. Contact HR for details on tuition assistance.</p>
</div>
</div>"""),
                ("Marriage Leave and Special Occasions", """<div class="lesson-content">
<h2>Marriage Leave and Special Occasions</h2>
<p>Flowitec recognizes important life events with special leave provisions.</p>

<h3>Marriage Leave</h3>
<div class="highlight-box">
<h4>For Your Own Marriage</h4>
<ul>
<li><strong>Entitlement:</strong> 5 working days paid leave</li>
<li><strong>Timing:</strong> Must be taken around the wedding date</li>
<li><strong>Documentation:</strong> Marriage certificate required upon return</li>
</ul>
</div>

<p><strong>For Immediate Family Marriage:</strong></p>
<ul>
<li>1-2 days for sibling, child, or parent's marriage</li>
<li>Subject to manager approval</li>
</ul>

<h3>Religious Observance Leave</h3>
<p>For religious holidays not covered by public holidays:</p>
<ul>
<li>Up to 2 days unpaid leave per year</li>
<li>Or use annual leave days</li>
<li>Advance notice required</li>
</ul>

<h3>Civic Duty Leave</h3>
<table class="info-table">
<tr><th>Activity</th><th>Leave Provision</th></tr>
<tr><td>Jury duty (if applicable)</td><td>Full duration, paid</td></tr>
<tr><td>Voting</td><td>2 hours paid (election day)</td></tr>
<tr><td>Court witness summons</td><td>As required, paid</td></tr>
<tr><td>Military reserve duty</td><td>Up to 10 days, paid difference</td></tr>
</table>

<h3>Volunteer Leave</h3>
<div class="highlight-box">
<h4>Community Service Day</h4>
<p>Flowitec encourages community involvement:</p>
<ul>
<li>1 paid day per year for approved volunteer activities</li>
<li>Must be with registered charity/NGO</li>
<li>Pre-approval from manager required</li>
</ul>
</div>
</div>"""),
                ("Unpaid Leave and Leave of Absence", """<div class="lesson-content">
<h2>Unpaid Leave and Leave of Absence</h2>
<p>For extended time off beyond paid leave entitlements.</p>

<h3>When Unpaid Leave May Be Granted</h3>
<ul>
<li>Extended family care responsibilities</li>
<li>Personal development or sabbatical</li>
<li>Extended travel (once-in-lifetime opportunity)</li>
<li>Resolving personal matters</li>
<li>Accompanying spouse on overseas posting</li>
</ul>

<h3>Request Process</h3>
<div class="process-steps">
<div class="step">
<span class="step-num">1</span>
<p>Discuss with manager and submit written request to HR</p>
</div>
<div class="step">
<span class="step-num">2</span>
<p>Include reason, duration, and proposed arrangements</p>
</div>
<div class="step">
<span class="step-num">3</span>
<p>HR and department head review and decide</p>
</div>
<div class="step">
<span class="step-num">4</span>
<p>If approved, sign leave of absence agreement</p>
</div>
</div>

<h3>Implications of Unpaid Leave</h3>
<div class="highlight-box">
<h4>Important Considerations</h4>
<ul>
<li><strong>Salary:</strong> No payment during unpaid leave</li>
<li><strong>Benefits:</strong> Most benefits suspended (discuss with HR)</li>
<li><strong>Pension:</strong> Contributions paused</li>
<li><strong>Health Insurance:</strong> May self-pay to maintain coverage</li>
<li><strong>Service:</strong> Period may not count toward service calculations</li>
</ul>
</div>

<h3>Return Guarantee</h3>
<p>For approved leave of absence:</p>
<ul>
<li>Up to 3 months: Guaranteed return to same position</li>
<li>3-6 months: Return to same or equivalent position</li>
<li>Over 6 months: Return subject to availability</li>
</ul>

<div class="info-box">
<h4>Career Break Scheme</h4>
<p>Employees with 5+ years service may be eligible for the Career Break Scheme - up to 12 months unpaid leave with guaranteed return. Contact HR for details.</p>
</div>
</div>"""),
                ("Public Holidays", """<div class="lesson-content">
<h2>Public Holidays</h2>
<p>Flowitec observes all Ghana public holidays plus company-specific days.</p>

<h3>Ghana Public Holidays</h3>
<table class="info-table">
<tr><th>Holiday</th><th>Date</th></tr>
<tr><td>New Year's Day</td><td>January 1</td></tr>
<tr><td>Constitution Day</td><td>January 7</td></tr>
<tr><td>Independence Day</td><td>March 6</td></tr>
<tr><td>Good Friday</td><td>Varies</td></tr>
<tr><td>Easter Monday</td><td>Varies</td></tr>
<tr><td>May Day</td><td>May 1</td></tr>
<tr><td>Africa Union Day</td><td>May 25</td></tr>
<tr><td>Republic Day</td><td>July 1</td></tr>
<tr><td>Founder's Day</td><td>August 4</td></tr>
<tr><td>Kwame Nkrumah Memorial Day</td><td>September 21</td></tr>
<tr><td>Eid al-Fitr</td><td>Varies</td></tr>
<tr><td>Eid al-Adha</td><td>Varies</td></tr>
<tr><td>Farmers' Day</td><td>December 6</td></tr>
<tr><td>Christmas Day</td><td>December 25</td></tr>
<tr><td>Boxing Day</td><td>December 26</td></tr>
</table>

<h3>Company Days</h3>
<div class="highlight-box">
<p>In addition to public holidays, Flowitec provides:</p>
<ul>
<li><strong>Flowitec Anniversary Day:</strong> [Date TBD]</li>
<li><strong>Year-End Closedown:</strong> December 27-31 (varies yearly)</li>
</ul>
</div>

<h3>Working on Public Holidays</h3>
<p>If required to work on a public holiday:</p>
<ul>
<li>Premium pay at 2x normal rate, OR</li>
<li>Lieu day off within 30 days</li>
</ul>

<h3>When Holidays Fall on Weekend</h3>
<p>If a public holiday falls on:</p>
<ul>
<li><strong>Saturday:</strong> Observed on following Monday</li>
<li><strong>Sunday:</strong> Observed on following Monday</li>
</ul>

<div class="info-box">
<h4>Holiday Calendar</h4>
<p>HR publishes the annual holiday calendar each December for the following year. Check the HR Portal for exact dates.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 6: Policy Administration",
            "lessons": [
                ("Leave Records and Documentation", """<div class="lesson-content">
<h2>Leave Records and Documentation</h2>
<p>Proper documentation ensures accurate tracking and compliance.</p>

<h3>Record Keeping</h3>
<p>The following leave records are maintained:</p>
<ul>
<li>Leave applications and approvals</li>
<li>Leave balances and history</li>
<li>Medical certificates</li>
<li>Return-to-work forms</li>
</ul>

<h3>Your Responsibilities</h3>
<ul>
<li>Submit leave requests through official HR Portal</li>
<li>Provide required documentation promptly</li>
<li>Keep your own records of leave taken</li>
<li>Report any discrepancies to HR</li>
</ul>

<h3>Accessing Your Records</h3>
<div class="highlight-box">
<p>You can view your leave records anytime:</p>
<ul>
<li><strong>HR Portal:</strong> Self-service leave dashboard</li>
<li><strong>Monthly Statement:</strong> Leave balance on payslip</li>
<li><strong>Request:</strong> Formal statement from HR</li>
</ul>
</div>

<h3>Data Privacy</h3>
<p>Your leave records are confidential:</p>
<ul>
<li>Only accessible by you, HR, and your manager</li>
<li>Medical information restricted to HR only</li>
<li>Protected under data protection laws</li>
</ul>

<div class="info-box">
<h4>Disputes</h4>
<p>If you disagree with your leave balance or a leave decision, raise it with HR within 30 days. Formal grievance procedures are available if not resolved.</p>
</div>
</div>"""),
                ("Policy Updates and Queries", """<div class="lesson-content">
<h2>Policy Updates and Getting Help</h2>
<p>This policy may be updated - here's how to stay informed and get support.</p>

<h3>Policy Updates</h3>
<ul>
<li>This policy is reviewed annually</li>
<li>Updates communicated via email and HR Portal</li>
<li>Major changes require 30 days notice</li>
<li>Current version always available on HR Portal</li>
</ul>

<h3>Getting Help</h3>
<div class="help-section">
<div class="help-card">
<h4>HR Portal</h4>
<p>Self-service for leave requests, balances, and FAQs</p>
</div>

<div class="help-card">
<h4>HR Team</h4>
<p>Email: hr@flowitec.com<br>Phone: [Internal extension]</p>
</div>

<div class="help-card">
<h4>Your Manager</h4>
<p>First point of contact for leave planning and approval</p>
</div>

<div class="help-card">
<h4>Employee Handbook</h4>
<p>Complete reference for all HR policies</p>
</div>
</div>

<h3>Frequently Asked Questions</h3>
<div class="faq-section">
<div class="faq-item">
<h4>Can I take half-day leave?</h4>
<p>Yes, leave can be taken in half-day increments.</p>
</div>

<div class="faq-item">
<h4>What if I'm sick during annual leave?</h4>
<p>If you become ill during annual leave and obtain a medical certificate, those days can be converted to sick leave.</p>
</div>

<div class="faq-item">
<h4>Can my leave request be denied?</h4>
<p>Managers may deny or reschedule leave for operational reasons. You have the right to appeal through HR.</p>
</div>
</div>

<div class="highlight-box">
<h4>Course Complete!</h4>
<p>You have completed the Leave Policy - Ghana course. Please proceed to the quiz to test your knowledge.</p>
</div>
</div>""")
            ]
        }
    ]
    
    order_counter = 0
    for module in leave_modules:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": leave_course_id,
            "title": module["title"],
            "description": f"Comprehensive coverage of {module['title']}",
            "order": leave_modules.index(module)
        })
        
        for lesson_title, lesson_content in module["lessons"]:
            await db.lessons.insert_one({
                "id": str(uuid.uuid4()),
                "module_id": module_id,
                "title": lesson_title,
                "content_type": "text",
                "content": lesson_content,
                "duration_minutes": 10,
                "order": order_counter
            })
            order_counter += 1
    
    # Create quiz for Leave Policy course
    await create_course_quiz(db, leave_course_id, "Leave Policy - Ghana", [
        {
            "question": "How many days of annual leave are standard employees entitled to at Flowitec?",
            "options": ["15 days", "18 days", "21 days", "25 days"],
            "correct_answer": 2
        },
        {
            "question": "What is the maximum number of annual leave days that can be carried over to the next year?",
            "options": ["3 days", "5 days", "7 days", "10 days"],
            "correct_answer": 1
        },
        {
            "question": "How many weeks of maternity leave does Flowitec provide?",
            "options": ["10 weeks", "12 weeks", "14 weeks", "16 weeks"],
            "correct_answer": 2
        },
        {
            "question": "How many days of paternity leave are fathers entitled to?",
            "options": ["5 days", "7 days", "10 days", "14 days"],
            "correct_answer": 2
        },
        {
            "question": "After how many consecutive sick leave days is a medical certificate required?",
            "options": ["1 day", "2 days", "3 days", "5 days"],
            "correct_answer": 1
        },
        {
            "question": "How much advance notice is required for annual leave of 3-5 days?",
            "options": ["1 week", "2 weeks", "4 weeks", "6 weeks"],
            "correct_answer": 1
        },
        {
            "question": "What is the bereavement leave entitlement for the loss of a parent?",
            "options": ["3 days", "5 days", "7 days", "10 days"],
            "correct_answer": 2
        },
        {
            "question": "How many self-certified sick days are allowed per year?",
            "options": ["3 days", "6 days", "10 days", "Unlimited"],
            "correct_answer": 1
        },
        {
            "question": "When must carried-over leave days be used by?",
            "options": ["January 31", "February 28", "March 31", "June 30"],
            "correct_answer": 2
        },
        {
            "question": "What is the daily accrual rate for annual leave?",
            "options": ["1.5 days/month", "1.75 days/month", "2 days/month", "2.25 days/month"],
            "correct_answer": 1
        }
    ])
    
    print("Created Course: Leave Policy - Ghana (20 pages + quiz)")
    
    # Continue creating the other 3 policy courses...
    await create_code_of_ethics_course(db)
    await create_disciplinary_code_course(db)
    await create_health_safety_course(db)


async def create_course_quiz(db, course_id, course_title, questions):
    """Create a quiz for a course"""
    quiz_id = str(uuid.uuid4())
    await db.quizzes.insert_one({
        "id": quiz_id,
        "course_id": course_id,
        "title": f"{course_title} - Final Assessment",
        "description": f"Test your knowledge of {course_title}",
        "questions": [
            {
                "id": str(uuid.uuid4()),
                "question": q["question"],
                "options": q["options"],
                "correct_answer": q["correct_answer"]
            } for q in questions
        ],
        "passing_score": 70,
        "time_limit_minutes": 20,
        "attempts_allowed": 3,
        "created_at": datetime.now(timezone.utc).isoformat()
    })


async def create_code_of_ethics_course(db):
    """Create Code of Ethics course with 20+ pages"""
    course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": course_id,
        "title": "Code of Ethics & Conduct",
        "description": "Learn about Flowitec's ethical standards, business conduct expectations, and compliance requirements. This course covers integrity, conflicts of interest, confidentiality, and professional behavior.",
        "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop",
        "category": "Ethics",
        "duration_hours": 6,
        "is_published": True,
        "course_type": "required",
        "code": "POL-ETH-002",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    modules = [
        {
            "title": "Module 1: Introduction to Ethics at Flowitec",
            "lessons": [
                ("Welcome and Purpose", """<div class="lesson-content">
<h2>Welcome to Flowitec's Code of Ethics</h2>
<p>This course introduces you to the ethical standards and conduct expectations at Flowitec. Our reputation for integrity is one of our greatest assets.</p>

<div class="highlight-box">
<h3>Our Commitment</h3>
<p>"At Flowitec, we believe that success built on integrity is the only success that lasts. Our commitment to ethical conduct guides every decision we make and every relationship we build."</p>
<p>- Flowitec Leadership Team</p>
</div>

<h3>Why Ethics Matter</h3>
<ul>
<li><strong>Trust:</strong> Customers and partners choose us because they trust us</li>
<li><strong>Reputation:</strong> Our reputation took decades to build</li>
<li><strong>Sustainability:</strong> Ethical businesses are sustainable businesses</li>
<li><strong>Legal Compliance:</strong> Ethical conduct keeps us compliant</li>
</ul>

<h3>Scope</h3>
<p>This code applies to:</p>
<ul>
<li>All employees, regardless of position</li>
<li>Board members and executives</li>
<li>Contractors and consultants</li>
<li>Business partners acting on our behalf</li>
</ul>

<div class="info-box">
<h4>Your Responsibility</h4>
<p>Every employee is responsible for understanding and following this code. Ignorance is not an excuse for unethical behavior.</p>
</div>
</div>"""),
                ("Flowitec Core Values", """<div class="lesson-content">
<h2>Flowitec Core Values</h2>
<p>Our core values define who we are and guide our behavior.</p>

<div class="values-grid">
<div class="value-card">
<h4>Integrity</h4>
<p>We do what's right, even when no one is watching. We're honest in all our dealings and keep our promises.</p>
</div>

<div class="value-card">
<h4>Excellence</h4>
<p>We strive for the highest quality in our products, services, and interactions. Good enough is never enough.</p>
</div>

<div class="value-card">
<h4>Respect</h4>
<p>We treat everyone with dignity and fairness. We value diversity and create an inclusive environment.</p>
</div>

<div class="value-card">
<h4>Accountability</h4>
<p>We take ownership of our actions and their consequences. We admit mistakes and learn from them.</p>
</div>

<div class="value-card">
<h4>Customer Focus</h4>
<p>Our customers' success is our success. We go above and beyond to meet their needs.</p>
</div>

<div class="value-card">
<h4>Innovation</h4>
<p>We embrace change and continuously improve. We solve problems creatively.</p>
</div>
</div>

<h3>Living Our Values</h3>
<p>Values are only meaningful when we live them daily:</p>
<ul>
<li>Consider our values when making decisions</li>
<li>Speak up when you see values being compromised</li>
<li>Recognize colleagues who exemplify our values</li>
<li>Reflect on how your actions align with our values</li>
</ul>

<div class="highlight-box">
<h4>The Values Test</h4>
<p>When facing a difficult decision, ask yourself:</p>
<ol>
<li>Is it legal?</li>
<li>Does it align with our values?</li>
<li>Would I be comfortable if it was reported in the news?</li>
<li>Would I be proud to explain it to my family?</li>
</ol>
<p>If you can't answer "yes" to all four, don't do it.</p>
</div>
</div>"""),
                ("Understanding the Code Structure", """<div class="lesson-content">
<h2>How This Code is Organized</h2>
<p>This code covers the major ethical topics relevant to your work at Flowitec.</p>

<h3>Key Areas Covered</h3>
<table class="info-table">
<tr><th>Topic</th><th>Key Issues</th></tr>
<tr><td>Workplace Conduct</td><td>Respect, harassment, discrimination, safety</td></tr>
<tr><td>Business Integrity</td><td>Honesty, fair dealing, accurate records</td></tr>
<tr><td>Conflicts of Interest</td><td>Personal vs. company interests</td></tr>
<tr><td>Confidentiality</td><td>Protecting sensitive information</td></tr>
<tr><td>Anti-Corruption</td><td>Bribery, gifts, facilitation payments</td></tr>
<tr><td>Assets and Resources</td><td>Proper use of company property</td></tr>
<tr><td>External Relationships</td><td>Customers, suppliers, competitors</td></tr>
<tr><td>Reporting Concerns</td><td>How to speak up</td></tr>
</table>

<h3>Your Obligations</h3>
<ul>
<li>Read and understand this entire code</li>
<li>Complete the assessment at the end</li>
<li>Apply these principles daily</li>
<li>Ask questions if anything is unclear</li>
<li>Report violations you observe</li>
</ul>

<div class="info-box">
<h4>Annual Certification</h4>
<p>All employees must certify annually that they have read, understood, and will comply with this code.</p>
</div>
</div>"""),
                ("Making Ethical Decisions", """<div class="lesson-content">
<h2>Framework for Ethical Decision Making</h2>
<p>When facing difficult decisions, use this framework to guide your thinking.</p>

<h3>The ETHICS Framework</h3>
<div class="framework-section">
<div class="framework-item">
<h4>E - Evaluate the situation</h4>
<p>What are the facts? Who is affected? What are the options?</p>
</div>

<div class="framework-item">
<h4>T - Think about stakeholders</h4>
<p>Consider impact on customers, colleagues, company, community</p>
</div>

<div class="framework-item">
<h4>H - Hear other perspectives</h4>
<p>Consult colleagues, manager, HR, or Ethics hotline if needed</p>
</div>

<div class="framework-item">
<h4>I - Identify applicable policies</h4>
<p>What do our policies, laws, and regulations say?</p>
</div>

<div class="framework-item">
<h4>C - Consider consequences</h4>
<p>What are short and long-term consequences of each option?</p>
</div>

<div class="framework-item">
<h4>S - Select and act</h4>
<p>Choose the ethical path and act with integrity</p>
</div>
</div>

<h3>Red Flags to Watch For</h3>
<div class="highlight-box">
<p>Be alert when someone says:</p>
<ul>
<li>"No one will ever know"</li>
<li>"Everyone does it"</li>
<li>"It's not really hurting anyone"</li>
<li>"We've always done it this way"</li>
<li>"Just this once"</li>
<li>"The company owes me this"</li>
</ul>
<p>These phrases often precede ethical lapses.</p>
</div>

<h3>When in Doubt</h3>
<ul>
<li>Pause - don't rush into questionable decisions</li>
<li>Seek advice - consult your manager, HR, or compliance</li>
<li>Document - keep records of your decision process</li>
<li>Err on the side of caution</li>
</ul>
</div>""")
            ]
        },
        {
            "title": "Module 2: Workplace Conduct",
            "lessons": [
                ("Respectful Workplace", """<div class="lesson-content">
<h2>Creating a Respectful Workplace</h2>
<p>Flowitec is committed to maintaining a workplace where everyone is treated with dignity and respect.</p>

<h3>Respect Means</h3>
<ul>
<li>Valuing different perspectives and ideas</li>
<li>Communicating professionally, even in disagreement</li>
<li>Recognizing others' contributions</li>
<li>Giving honest, constructive feedback</li>
<li>Listening actively and empathetically</li>
</ul>

<h3>Prohibited Behaviors</h3>
<div class="prohibited-list">
<ul>
<li>Bullying, intimidation, or threats</li>
<li>Offensive jokes or comments</li>
<li>Exclusion or ostracizing colleagues</li>
<li>Public humiliation or embarrassment</li>
<li>Spreading rumors or gossip</li>
<li>Undermining others' work</li>
</ul>
</div>

<h3>Professional Communication</h3>
<div class="highlight-box">
<h4>Communication Guidelines</h4>
<ul>
<li>Be direct but respectful</li>
<li>Focus on issues, not personalities</li>
<li>Use appropriate channels (not public criticism)</li>
<li>Respond to emails and messages promptly</li>
<li>Maintain confidentiality in sensitive matters</li>
</ul>
</div>

<div class="info-box">
<h4>Impact vs. Intent</h4>
<p>Your intent doesn't matter as much as the impact. Even unintentional disrespect can harm colleagues. Be aware of how your words and actions affect others.</p>
</div>
</div>"""),
                ("Harassment and Discrimination", """<div class="lesson-content">
<h2>Zero Tolerance for Harassment and Discrimination</h2>
<p>Flowitec has zero tolerance for harassment or discrimination of any kind.</p>

<h3>What is Harassment?</h3>
<p>Unwelcome conduct based on protected characteristics that creates an intimidating, hostile, or offensive work environment:</p>
<ul>
<li><strong>Sexual Harassment:</strong> Unwanted advances, comments, or requests</li>
<li><strong>Verbal Harassment:</strong> Slurs, epithets, or derogatory comments</li>
<li><strong>Physical Harassment:</strong> Unwanted touching or physical intimidation</li>
<li><strong>Visual Harassment:</strong> Offensive images, gestures, or materials</li>
<li><strong>Online Harassment:</strong> Cyberbullying or inappropriate digital content</li>
</ul>

<h3>Protected Characteristics</h3>
<p>Discrimination or harassment based on any of these is prohibited:</p>
<table class="info-table">
<tr><td>Race or ethnicity</td><td>Religion or belief</td></tr>
<tr><td>Gender or sex</td><td>Age</td></tr>
<tr><td>Sexual orientation</td><td>Disability</td></tr>
<tr><td>Marital status</td><td>Pregnancy</td></tr>
<tr><td>National origin</td><td>Political affiliation</td></tr>
</table>

<h3>If You Experience Harassment</h3>
<div class="highlight-box">
<ol>
<li>Tell the person to stop (if you feel safe doing so)</li>
<li>Document what happened (dates, witnesses, details)</li>
<li>Report to your manager, HR, or Ethics hotline</li>
<li>You will not face retaliation for reporting</li>
</ol>
</div>

<h3>Consequences</h3>
<p>Violations will result in disciplinary action up to and including termination, regardless of the offender's position.</p>
</div>"""),
                ("Diversity and Inclusion", """<div class="lesson-content">
<h2>Embracing Diversity and Inclusion</h2>
<p>Diversity is a strength. We actively create an environment where everyone can contribute fully.</p>

<h3>What Diversity Means at Flowitec</h3>
<ul>
<li><strong>Visible Diversity:</strong> Race, gender, age, physical ability</li>
<li><strong>Invisible Diversity:</strong> Education, experience, thinking styles</li>
<li><strong>Work Style Diversity:</strong> Different approaches to problem-solving</li>
<li><strong>Cultural Diversity:</strong> Different backgrounds and perspectives</li>
</ul>

<h3>Inclusion in Practice</h3>
<div class="inclusion-practices">
<div class="practice-card">
<h4>In Meetings</h4>
<p>Ensure all voices are heard. Actively invite quieter members to contribute.</p>
</div>

<div class="practice-card">
<h4>In Hiring</h4>
<p>Focus on skills and potential. Avoid unconscious bias in selection.</p>
</div>

<div class="practice-card">
<h4>In Development</h4>
<p>Provide equal opportunities for growth and advancement.</p>
</div>

<div class="practice-card">
<h4>In Daily Work</h4>
<p>Be aware of different communication styles and preferences.</p>
</div>
</div>

<h3>Unconscious Bias</h3>
<div class="highlight-box">
<h4>Common Biases to Watch For</h4>
<ul>
<li><strong>Affinity Bias:</strong> Preferring people similar to us</li>
<li><strong>Confirmation Bias:</strong> Seeking information that confirms our beliefs</li>
<li><strong>Attribution Bias:</strong> Judging others' actions more harshly than our own</li>
<li><strong>Halo Effect:</strong> One positive trait influencing overall perception</li>
</ul>
<p>Awareness is the first step to overcoming bias.</p>
</div>

<div class="info-box">
<h4>Employee Resource Groups</h4>
<p>Flowitec supports employee resource groups for various communities. Contact HR to learn about or start a group.</p>
</div>
</div>"""),
                ("Workplace Safety", """<div class="lesson-content">
<h2>Workplace Safety and Well-being</h2>
<p>Everyone has the right to a safe working environment. Safety is everyone's responsibility.</p>

<h3>Your Safety Responsibilities</h3>
<ul>
<li>Follow all safety procedures and protocols</li>
<li>Use required personal protective equipment (PPE)</li>
<li>Report hazards and near-misses immediately</li>
<li>Participate in safety training</li>
<li>Never take shortcuts that compromise safety</li>
</ul>

<h3>Specific Safety Requirements</h3>
<table class="info-table">
<tr><th>Area</th><th>Key Requirements</th></tr>
<tr><td>Warehouse/Workshop</td><td>Steel-toe boots, hard hat, high-vis vest</td></tr>
<tr><td>Office</td><td>Ergonomic workstation, regular breaks</td></tr>
<tr><td>Customer Sites</td><td>Follow site-specific safety rules</td></tr>
<tr><td>Driving</td><td>No phone use, defensive driving</td></tr>
</table>

<h3>Drug and Alcohol Policy</h3>
<div class="highlight-box">
<p>Flowitec maintains a drug and alcohol-free workplace:</p>
<ul>
<li>Zero tolerance for being under the influence at work</li>
<li>Random testing may be conducted</li>
<li>Support available for those seeking help</li>
</ul>
</div>

<h3>Mental Health</h3>
<p>We recognize mental health as equally important as physical health:</p>
<ul>
<li>Employee Assistance Program (EAP) available</li>
<li>Confidential counseling services</li>
<li>Mental health days are legitimate sick leave</li>
<li>Open conversations about well-being encouraged</li>
</ul>

<div class="info-box">
<h4>See Something, Say Something</h4>
<p>If you see unsafe conditions or practices, report them immediately. You could prevent an injury or save a life.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 3: Business Integrity",
            "lessons": [
                ("Honest Dealings", """<div class="lesson-content">
<h2>Honesty in Business Dealings</h2>
<p>Honesty is the foundation of all our business relationships.</p>

<h3>Being Honest Means</h3>
<ul>
<li>Providing accurate information to customers</li>
<li>Not misrepresenting product capabilities</li>
<li>Keeping promises and commitments</li>
<li>Admitting mistakes and correcting them</li>
<li>Giving truthful answers, even when difficult</li>
</ul>

<h3>With Customers</h3>
<div class="customer-honesty">
<h4>Do</h4>
<ul>
<li>Accurately describe product specifications</li>
<li>Be transparent about pricing and terms</li>
<li>Disclose limitations or issues</li>
<li>Set realistic expectations</li>
</ul>

<h4>Don't</h4>
<ul>
<li>Exaggerate product capabilities</li>
<li>Hide known defects or issues</li>
<li>Make promises you can't keep</li>
<li>Disparage competitors unfairly</li>
</ul>
</div>

<h3>Accurate Records</h3>
<div class="highlight-box">
<h4>Record-Keeping Requirements</h4>
<p>All business records must be:</p>
<ul>
<li><strong>Accurate:</strong> Reflect actual transactions</li>
<li><strong>Complete:</strong> Include all relevant details</li>
<li><strong>Timely:</strong> Recorded promptly</li>
<li><strong>Authorized:</strong> Only for legitimate business</li>
</ul>
<p>Falsifying records is grounds for immediate termination and may be illegal.</p>
</div>

<div class="info-box">
<h4>Expense Reports</h4>
<p>Submit only legitimate business expenses with accurate documentation. Inflating expenses or claiming personal items is fraud.</p>
</div>
</div>"""),
                ("Confidentiality", """<div class="lesson-content">
<h2>Protecting Confidential Information</h2>
<p>Confidential information is a valuable asset that must be protected.</p>

<h3>Types of Confidential Information</h3>
<table class="info-table">
<tr><th>Category</th><th>Examples</th></tr>
<tr><td>Business</td><td>Financial data, strategic plans, pricing</td></tr>
<tr><td>Technical</td><td>Product designs, formulas, processes</td></tr>
<tr><td>Customer</td><td>Client lists, purchase history, contracts</td></tr>
<tr><td>Employee</td><td>Salaries, performance reviews, medical info</td></tr>
<tr><td>Legal</td><td>Litigation matters, contracts, IP</td></tr>
</table>

<h3>Your Obligations</h3>
<ul>
<li>Share confidential information only on need-to-know basis</li>
<li>Secure documents and devices when not in use</li>
<li>Use strong passwords and don't share them</li>
<li>Be careful in public spaces (phone calls, screens)</li>
<li>Follow data protection procedures</li>
</ul>

<h3>Social Media and Public Discussions</h3>
<div class="highlight-box">
<h4>What Not to Share</h4>
<p>Never share the following externally:</p>
<ul>
<li>Unannounced products or projects</li>
<li>Financial information before public release</li>
<li>Customer names or details without permission</li>
<li>Internal disputes or grievances</li>
<li>Anything marked "confidential" or "internal"</li>
</ul>
</div>

<h3>After Leaving Flowitec</h3>
<p>Confidentiality obligations continue after employment ends:</p>
<ul>
<li>Return all company materials</li>
<li>Don't take confidential information</li>
<li>Respect non-disclosure agreements</li>
</ul>
</div>"""),
                ("Conflicts of Interest", """<div class="lesson-content">
<h2>Avoiding Conflicts of Interest</h2>
<p>A conflict of interest occurs when personal interests interfere with your ability to act in Flowitec's best interest.</p>

<h3>Common Conflicts</h3>
<div class="conflict-types">
<div class="conflict-card">
<h4>Financial Interests</h4>
<p>Owning stock in or receiving payments from competitors, suppliers, or customers</p>
</div>

<div class="conflict-card">
<h4>Outside Employment</h4>
<p>Working for or consulting with another company in a way that affects your Flowitec duties</p>
</div>

<div class="conflict-card">
<h4>Family Relationships</h4>
<p>Making business decisions involving family members or their companies</p>
</div>

<div class="conflict-card">
<h4>Business Opportunities</h4>
<p>Taking business opportunities that belong to Flowitec for yourself</p>
</div>
</div>

<h3>Disclosure Requirement</h3>
<div class="highlight-box">
<h4>When to Disclose</h4>
<p>You must disclose potential conflicts to your manager and HR:</p>
<ul>
<li>Before engaging in any outside business activity</li>
<li>When a family member joins a supplier or competitor</li>
<li>If you're involved in decisions affecting related parties</li>
<li>When you're unsure if a conflict exists</li>
</ul>
<p>Disclosure doesn't mean you've done something wrong - it's about transparency.</p>
</div>

<h3>Managing Conflicts</h3>
<p>Once disclosed, conflicts can often be managed:</p>
<ul>
<li>Recuse yourself from related decisions</li>
<li>Implement oversight by uninvolved parties</li>
<li>Document the conflict and management approach</li>
<li>In some cases, you may need to divest the interest</li>
</ul>
</div>"""),
                ("Anti-Corruption and Bribery", """<div class="lesson-content">
<h2>Anti-Corruption and Anti-Bribery</h2>
<p>Flowitec has zero tolerance for bribery and corruption in any form.</p>

<h3>What is Bribery?</h3>
<p>Offering, giving, receiving, or soliciting anything of value to influence a business decision or government action.</p>

<h3>Prohibited Activities</h3>
<div class="prohibited-section">
<ul>
<li>Bribing government officials for permits or approvals</li>
<li>Paying "facilitation" fees to speed up processes</li>
<li>Kickbacks to suppliers or customers</li>
<li>Accepting bribes from any party</li>
<li>Using third parties to make improper payments</li>
</ul>
</div>

<h3>Gifts and Entertainment</h3>
<div class="highlight-box">
<h4>Acceptable</h4>
<ul>
<li>Modest gifts of low value (under GHS 500)</li>
<li>Occasional meals during business discussions</li>
<li>Company-branded promotional items</li>
</ul>

<h4>Not Acceptable</h4>
<ul>
<li>Cash or cash equivalents (gift cards)</li>
<li>Expensive gifts or entertainment</li>
<li>Gifts to influence pending decisions</li>
<li>Anything that would embarrass Flowitec</li>
</ul>
</div>

<h3>Government Officials</h3>
<p>Extra caution applies with government officials:</p>
<ul>
<li>Never offer anything to influence official action</li>
<li>All gifts must be approved in advance by Legal</li>
<li>Document all interactions carefully</li>
<li>Follow local laws strictly</li>
</ul>

<div class="info-box">
<h4>Legal Consequences</h4>
<p>Bribery is illegal in Ghana and internationally. Violations can result in criminal prosecution for individuals and massive fines for the company.</p>
</div>
</div>""")
            ]
        },
        {
            "title": "Module 4: Reporting and Compliance",
            "lessons": [
                ("Speaking Up", """<div class="lesson-content">
<h2>Your Duty to Speak Up</h2>
<p>If you see something wrong, you have a responsibility to report it.</p>

<h3>What to Report</h3>
<ul>
<li>Violations of this Code of Ethics</li>
<li>Illegal activities</li>
<li>Safety hazards</li>
<li>Harassment or discrimination</li>
<li>Financial irregularities</li>
<li>Retaliation against reporters</li>
</ul>

<h3>How to Report</h3>
<table class="info-table">
<tr><th>Channel</th><th>Best For</th></tr>
<tr><td>Direct Manager</td><td>Minor issues, workplace concerns</td></tr>
<tr><td>HR Department</td><td>Personnel matters, harassment</td></tr>
<tr><td>Legal/Compliance</td><td>Legal matters, major violations</td></tr>
<tr><td>Ethics Hotline</td><td>Anonymous reporting, serious concerns</td></tr>
<tr><td>Senior Management</td><td>When other channels aren't working</td></tr>
</table>

<h3>Protection from Retaliation</h3>
<div class="highlight-box">
<h4>Zero Tolerance for Retaliation</h4>
<p>Flowitec strictly prohibits retaliation against anyone who:</p>
<ul>
<li>Reports a concern in good faith</li>
<li>Participates in an investigation</li>
<li>Refuses to participate in wrongdoing</li>
</ul>
<p>Retaliation will result in disciplinary action up to termination.</p>
</div>

<h3>Anonymous Reporting</h3>
<p>You can report anonymously through the Ethics Hotline if you prefer not to identify yourself. However, providing your identity helps with investigation.</p>

<div class="info-box">
<h4>Good Faith Requirement</h4>
<p>Reports must be made in good faith - honestly believing there's a concern. Knowingly false reports are themselves a violation of this code.</p>
</div>
</div>"""),
                ("Investigation Process", """<div class="lesson-content">
<h2>How Concerns Are Investigated</h2>
<p>All reported concerns are taken seriously and investigated appropriately.</p>

<h3>Investigation Steps</h3>
<div class="process-steps">
<div class="step">
<span class="step-num">1</span>
<h4>Receipt</h4>
<p>Concern is logged and assigned to appropriate investigator</p>
</div>

<div class="step">
<span class="step-num">2</span>
<h4>Assessment</h4>
<p>Initial review to understand scope and urgency</p>
</div>

<div class="step">
<span class="step-num">3</span>
<h4>Investigation</h4>
<p>Gather evidence, interview witnesses, review records</p>
</div>

<div class="step">
<span class="step-num">4</span>
<h4>Findings</h4>
<p>Document conclusions based on evidence</p>
</div>

<div class="step">
<span class="step-num">5</span>
<h4>Action</h4>
<p>Implement appropriate consequences and corrective measures</p>
</div>

<div class="step">
<span class="step-num">6</span>
<h4>Follow-up</h4>
<p>Monitor to prevent recurrence</p>
</div>
</div>

<h3>Your Role in Investigations</h3>
<ul>
<li>Cooperate fully if asked to participate</li>
<li>Provide truthful information</li>
<li>Maintain confidentiality</li>
<li>Don't discuss with others or interfere</li>
</ul>

<h3>Confidentiality</h3>
<div class="highlight-box">
<p>Investigations are conducted confidentially:</p>
<ul>
<li>Only those who need to know are informed</li>
<li>Reporter's identity is protected where possible</li>
<li>Accused parties are treated fairly</li>
<li>Records are secured</li>
</ul>
</div>
</div>"""),
                ("Consequences of Violations", """<div class="lesson-content">
<h2>Consequences of Violating the Code</h2>
<p>Violations of this code are taken seriously and result in appropriate consequences.</p>

<h3>Disciplinary Actions</h3>
<p>Depending on severity, violations may result in:</p>
<ul>
<li>Verbal warning and coaching</li>
<li>Written warning</li>
<li>Performance improvement plan</li>
<li>Demotion or transfer</li>
<li>Suspension</li>
<li>Termination of employment</li>
</ul>

<h3>Factors Considered</h3>
<table class="info-table">
<tr><th>Factor</th><th>Impact</th></tr>
<tr><td>Severity of violation</td><td>More serious = more severe consequence</td></tr>
<tr><td>Intent</td><td>Deliberate vs. accidental</td></tr>
<tr><td>Prior history</td><td>Repeat violations = escalated consequence</td></tr>
<tr><td>Cooperation</td><td>Honesty and cooperation may mitigate</td></tr>
<tr><td>Self-reporting</td><td>Coming forward voluntarily viewed favorably</td></tr>
</table>

<h3>Criminal Referral</h3>
<div class="highlight-box">
<p>Some violations may be referred to law enforcement:</p>
<ul>
<li>Theft or fraud</li>
<li>Bribery</li>
<li>Violence or threats</li>
<li>Drug-related offenses</li>
<li>Other criminal acts</li>
</ul>
</div>

<h3>No Exceptions</h3>
<p>This code applies equally to everyone:</p>
<ul>
<li>High performers are not exempt</li>
<li>Senior executives are held to the same standards</li>
<li>"Business necessity" is not an excuse</li>
<li>"Everyone does it" is not a defense</li>
</ul>
</div>"""),
                ("Course Summary and Commitment", """<div class="lesson-content">
<h2>Summary and Your Commitment</h2>
<p>You've completed the Flowitec Code of Ethics & Conduct course.</p>

<h3>Key Takeaways</h3>
<div class="summary-grid">
<div class="summary-card">
<h4>Values-Driven</h4>
<p>Our values of integrity, excellence, respect, and accountability guide all decisions.</p>
</div>

<div class="summary-card">
<h4>Respectful Workplace</h4>
<p>We maintain a workplace free from harassment and discrimination.</p>
</div>

<div class="summary-card">
<h4>Business Integrity</h4>
<p>Honesty, confidentiality, and anti-corruption are non-negotiable.</p>
</div>

<div class="summary-card">
<h4>Speak Up</h4>
<p>Reporting concerns is a responsibility, and retaliation is prohibited.</p>
</div>
</div>

<h3>Your Commitment</h3>
<div class="highlight-box">
<h4>By completing this course, you commit to:</h4>
<ul>
<li>Upholding Flowitec's values in all actions</li>
<li>Following this Code of Ethics & Conduct</li>
<li>Reporting violations you observe</li>
<li>Seeking guidance when uncertain</li>
<li>Being a role model for ethical behavior</li>
</ul>
</div>

<h3>Resources</h3>
<ul>
<li><strong>Full Code Document:</strong> Available on HR Portal</li>
<li><strong>Ethics Hotline:</strong> [Contact details]</li>
<li><strong>HR Department:</strong> hr@flowitec.com</li>
<li><strong>Legal/Compliance:</strong> compliance@flowitec.com</li>
</ul>

<div class="info-box">
<h4>Final Step</h4>
<p>Please complete the quiz to confirm your understanding. You must pass to receive your certificate.</p>
</div>
</div>""")
            ]
        }
    ]
    
    order_counter = 0
    for module in modules:
        module_id = str(uuid.uuid4())
        await db.modules.insert_one({
            "id": module_id,
            "course_id": course_id,
            "title": module["title"],
            "description": f"Comprehensive coverage of {module['title']}",
            "order": modules.index(module)
        })
        
        for lesson_title, lesson_content in module["lessons"]:
            await db.lessons.insert_one({
                "id": str(uuid.uuid4()),
                "module_id": module_id,
                "title": lesson_title,
                "content_type": "text",
                "content": lesson_content,
                "duration_minutes": 8,
                "order": order_counter
            })
            order_counter += 1
    
    # Create quiz
    await create_course_quiz(db, course_id, "Code of Ethics & Conduct", [
        {
            "question": "Which is NOT one of Flowitec's core values?",
            "options": ["Integrity", "Excellence", "Profit Maximization", "Accountability"],
            "correct_answer": 2
        },
        {
            "question": "What should you do if you're unsure whether something is ethical?",
            "options": ["Just do it if no one will know", "Ask your manager or HR", "Ignore your concerns", "Wait and see what happens"],
            "correct_answer": 1
        },
        {
            "question": "What is Flowitec's tolerance for harassment and discrimination?",
            "options": ["Low tolerance", "Moderate tolerance", "Zero tolerance", "Depends on severity"],
            "correct_answer": 2
        },
        {
            "question": "What is a conflict of interest?",
            "options": ["Disagreement with a colleague", "When personal interests interfere with company interests", "A business negotiation", "Competition with other companies"],
            "correct_answer": 1
        },
        {
            "question": "Which is an acceptable gift to give a customer?",
            "options": ["Cash equivalent gift card", "Expensive watch", "Modest company-branded item", "Vacation package"],
            "correct_answer": 2
        },
        {
            "question": "What happens if you report a concern in good faith?",
            "options": ["You might face retaliation", "You are protected from retaliation", "Your job is at risk", "Nothing, reports are ignored"],
            "correct_answer": 1
        },
        {
            "question": "When must you disclose a potential conflict of interest?",
            "options": ["Only if caught", "Before engaging in the activity", "After completing the transaction", "Never"],
            "correct_answer": 1
        },
        {
            "question": "Who does this Code of Ethics apply to?",
            "options": ["Only junior employees", "Only senior managers", "All employees regardless of position", "Only sales staff"],
            "correct_answer": 2
        }
    ])
    
    print("Created Course: Code of Ethics & Conduct (16 pages + quiz)")


async def create_disciplinary_code_course(db):
    """Create Disciplinary Code course - abbreviated version"""
    course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": course_id,
        "title": "Disciplinary Code",
        "description": "Understand Flowitec's disciplinary procedures, categories of misconduct, and the fair process for addressing workplace issues. Essential for all employees.",
        "thumbnail": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=400&h=225&fit=crop",
        "category": "HR Policy",
        "duration_hours": 5,
        "is_published": True,
        "course_type": "required",
        "code": "POL-DIS-003",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    # Create a simplified version with key content
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Disciplinary Procedures",
        "description": "Complete guide to Flowitec's disciplinary procedures",
        "order": 0
    })
    
    lessons = [
        ("Introduction to Disciplinary Code", "<div class='lesson-content'><h2>Introduction</h2><p>This course covers Flowitec's disciplinary procedures and expectations.</p></div>"),
        ("Purpose and Scope", "<div class='lesson-content'><h2>Purpose and Scope</h2><p>Understanding why disciplinary procedures exist and who they apply to.</p></div>"),
        ("Categories of Misconduct", "<div class='lesson-content'><h2>Categories of Misconduct</h2><p>Minor, serious, and gross misconduct categories explained.</p></div>"),
        ("Minor Misconduct", "<div class='lesson-content'><h2>Minor Misconduct</h2><p>Examples include lateness, minor policy breaches, and first-time offenses.</p></div>"),
        ("Serious Misconduct", "<div class='lesson-content'><h2>Serious Misconduct</h2><p>Examples include insubordination, repeated minor offenses, and negligence.</p></div>"),
        ("Gross Misconduct", "<div class='lesson-content'><h2>Gross Misconduct</h2><p>Examples include theft, fraud, violence, and serious safety breaches.</p></div>"),
        ("Disciplinary Process Overview", "<div class='lesson-content'><h2>The Disciplinary Process</h2><p>Step-by-step guide to how disciplinary matters are handled.</p></div>"),
        ("Investigation Procedures", "<div class='lesson-content'><h2>Investigation</h2><p>How investigations are conducted fairly and thoroughly.</p></div>"),
        ("Disciplinary Hearings", "<div class='lesson-content'><h2>Disciplinary Hearings</h2><p>Your rights and what to expect during a hearing.</p></div>"),
        ("Warnings and Sanctions", "<div class='lesson-content'><h2>Warnings and Sanctions</h2><p>Verbal, written, and final written warnings explained.</p></div>"),
        ("Appeal Process", "<div class='lesson-content'><h2>Appeals</h2><p>How to appeal a disciplinary decision.</p></div>"),
        ("Your Rights", "<div class='lesson-content'><h2>Employee Rights</h2><p>Right to representation, fair hearing, and appeal.</p></div>"),
        ("Suspension Procedures", "<div class='lesson-content'><h2>Suspension</h2><p>When and how suspension may be used.</p></div>"),
        ("Termination Procedures", "<div class='lesson-content'><h2>Termination</h2><p>Process for termination in cases of serious misconduct.</p></div>"),
        ("Record Keeping", "<div class='lesson-content'><h2>Record Keeping</h2><p>How disciplinary records are maintained and accessed.</p></div>"),
        ("Rehabilitation", "<div class='lesson-content'><h2>Rehabilitation</h2><p>How warnings expire and records are cleared.</p></div>"),
        ("Manager Responsibilities", "<div class='lesson-content'><h2>For Managers</h2><p>Responsibilities in administering discipline fairly.</p></div>"),
        ("Frequently Asked Questions", "<div class='lesson-content'><h2>FAQs</h2><p>Common questions about disciplinary procedures.</p></div>"),
        ("Case Studies", "<div class='lesson-content'><h2>Case Studies</h2><p>Example scenarios and how they would be handled.</p></div>"),
        ("Summary and Quiz", "<div class='lesson-content'><h2>Summary</h2><p>Key points and preparation for the quiz.</p></div>")
    ]
    
    for i, (title, content) in enumerate(lessons):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": title,
            "content_type": "text",
            "content": content,
            "duration_minutes": 6,
            "order": i
        })
    
    await create_course_quiz(db, course_id, "Disciplinary Code", [
        {"question": "What are the three categories of misconduct?", "options": ["Minor, Medium, Major", "Minor, Serious, Gross", "Low, Medium, High", "Warning, Suspension, Termination"], "correct_answer": 1},
        {"question": "What is an example of gross misconduct?", "options": ["Being 5 minutes late", "Theft or fraud", "Forgetting to clock in", "Minor dress code violation"], "correct_answer": 1},
        {"question": "Do you have the right to representation at a disciplinary hearing?", "options": ["No", "Only for gross misconduct", "Yes, always", "Only if approved"], "correct_answer": 2},
        {"question": "How long does a written warning typically remain on file?", "options": ["3 months", "6 months", "12 months", "Permanently"], "correct_answer": 2},
        {"question": "Can you appeal a disciplinary decision?", "options": ["No", "Yes", "Only if terminated", "Only for gross misconduct"], "correct_answer": 1}
    ])
    
    print("Created Course: Disciplinary Code (20 pages + quiz)")


async def create_health_safety_course(db):
    """Create Health & Safety Policy course - abbreviated version"""
    course_id = str(uuid.uuid4())
    await db.courses.insert_one({
        "id": course_id,
        "title": "Health & Safety Policy",
        "description": "Comprehensive health and safety training covering workplace hazards, emergency procedures, PPE requirements, and your responsibilities for maintaining a safe work environment.",
        "thumbnail": "https://images.unsplash.com/photo-1504439468489-c8920d796a29?w=400&h=225&fit=crop",
        "category": "Safety",
        "duration_hours": 6,
        "is_published": True,
        "course_type": "required",
        "code": "POL-HS-004",
        "enrolled_users": [],
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    module_id = str(uuid.uuid4())
    await db.modules.insert_one({
        "id": module_id,
        "course_id": course_id,
        "title": "Health and Safety Fundamentals",
        "description": "Complete health and safety training",
        "order": 0
    })
    
    lessons = [
        ("Introduction to Workplace Safety", "<div class='lesson-content'><h2>Welcome</h2><p>Introduction to health and safety at Flowitec.</p></div>"),
        ("Legal Framework", "<div class='lesson-content'><h2>Legal Framework</h2><p>Ghana's occupational health and safety laws and regulations.</p></div>"),
        ("Your Safety Responsibilities", "<div class='lesson-content'><h2>Your Responsibilities</h2><p>Every employee's duty to maintain workplace safety.</p></div>"),
        ("Management Responsibilities", "<div class='lesson-content'><h2>Management Duties</h2><p>What managers must do to ensure team safety.</p></div>"),
        ("Hazard Identification", "<div class='lesson-content'><h2>Identifying Hazards</h2><p>How to spot potential hazards in the workplace.</p></div>"),
        ("Risk Assessment", "<div class='lesson-content'><h2>Risk Assessment</h2><p>Evaluating risks and implementing controls.</p></div>"),
        ("Personal Protective Equipment", "<div class='lesson-content'><h2>PPE</h2><p>Required protective equipment and proper use.</p></div>"),
        ("Warehouse and Workshop Safety", "<div class='lesson-content'><h2>Warehouse Safety</h2><p>Safety procedures for warehouse and workshop areas.</p></div>"),
        ("Office Ergonomics", "<div class='lesson-content'><h2>Office Safety</h2><p>Ergonomic workstation setup and preventing injuries.</p></div>"),
        ("Manual Handling", "<div class='lesson-content'><h2>Manual Handling</h2><p>Safe lifting techniques and preventing back injuries.</p></div>"),
        ("Fire Safety", "<div class='lesson-content'><h2>Fire Safety</h2><p>Fire prevention, extinguisher use, and evacuation.</p></div>"),
        ("Emergency Procedures", "<div class='lesson-content'><h2>Emergencies</h2><p>What to do in various emergency situations.</p></div>"),
        ("First Aid", "<div class='lesson-content'><h2>First Aid</h2><p>Basic first aid and location of first aid resources.</p></div>"),
        ("Incident Reporting", "<div class='lesson-content'><h2>Reporting</h2><p>How to report accidents, incidents, and near-misses.</p></div>"),
        ("Chemical Safety", "<div class='lesson-content'><h2>Chemical Hazards</h2><p>Handling chemicals safely and MSDS sheets.</p></div>"),
        ("Electrical Safety", "<div class='lesson-content'><h2>Electrical Safety</h2><p>Working safely around electrical equipment.</p></div>"),
        ("Vehicle and Driving Safety", "<div class='lesson-content'><h2>Driving Safety</h2><p>Safe driving practices for company vehicles.</p></div>"),
        ("Working at Heights", "<div class='lesson-content'><h2>Heights</h2><p>Safety when working on ladders or elevated areas.</p></div>"),
        ("Health and Wellness", "<div class='lesson-content'><h2>Health</h2><p>Physical and mental health in the workplace.</p></div>"),
        ("Summary and Commitment", "<div class='lesson-content'><h2>Summary</h2><p>Key safety points and your safety commitment.</p></div>")
    ]
    
    for i, (title, content) in enumerate(lessons):
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": module_id,
            "title": title,
            "content_type": "text",
            "content": content,
            "duration_minutes": 7,
            "order": i
        })
    
    await create_course_quiz(db, course_id, "Health & Safety Policy", [
        {"question": "Whose responsibility is workplace safety?", "options": ["Only management", "Only the safety officer", "Everyone", "Only HR"], "correct_answer": 2},
        {"question": "What should you do if you identify a hazard?", "options": ["Ignore it", "Report it immediately", "Fix it yourself", "Wait for someone else"], "correct_answer": 1},
        {"question": "When should PPE be worn?", "options": ["Only during inspections", "When you feel like it", "Whenever required by the task", "Never"], "correct_answer": 2},
        {"question": "What is the first thing to do in a fire emergency?", "options": ["Collect belongings", "Raise the alarm", "Continue working", "Wait for instructions"], "correct_answer": 1},
        {"question": "How should near-misses be treated?", "options": ["Ignored since no one was hurt", "Reported and investigated", "Kept secret", "Only told to friends"], "correct_answer": 1}
    ])
    
    print("Created Course: Health & Safety Policy (20 pages + quiz)")
