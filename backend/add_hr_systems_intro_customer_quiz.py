import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://flowitec_admin:Popdhan344@cluster0.b8eqmtl.mongodb.net/flowitec_lms?appName=Cluster0"
DB_NAME = "flowitec_lms"

HR_SYSTEMS_QUESTIONS = [
    {
        "question": "HR systems and processes are designed to:",
        "options": ["Replace HR professionals with technology", "Standardise, streamline and improve the efficiency and consistency of HR activities across the organisation", "Only manage payroll and benefits administration", "Reduce the number of employees in the HR department"],
        "correct_answer": "Standardise, streamline and improve the efficiency and consistency of HR activities across the organisation"
    },
    {
        "question": "The recruitment process in HR systems includes:",
        "options": ["Only advertising job vacancies", "Job analysis, sourcing, screening, interviewing, selection and offer management", "Only conducting interviews", "Only onboarding new employees"],
        "correct_answer": "Job analysis, sourcing, screening, interviewing, selection and offer management"
    },
    {
        "question": "Bands and grades in an HR structure provide:",
        "options": ["A ranking of employees by performance only", "A framework for job levels, pay ranges and career progression that ensures internal equity and external competitiveness", "Only a basis for disciplinary action", "A system for tracking employee attendance"],
        "correct_answer": "A framework for job levels, pay ranges and career progression that ensures internal equity and external competitiveness"
    },
    {
        "question": "The performance management system process includes:",
        "options": ["Only the annual appraisal meeting", "Goal setting, ongoing feedback, mid-year reviews, year-end assessment and development planning", "Only identifying underperforming employees", "Only setting salary increases"],
        "correct_answer": "Goal setting, ongoing feedback, mid-year reviews, year-end assessment and development planning"
    },
    {
        "question": "Key Result Areas (KRAs) in performance management define:",
        "options": ["The employee's salary band", "The primary areas of responsibility where an employee is expected to deliver measurable results", "The company's financial targets only", "The training budget for each department"],
        "correct_answer": "The primary areas of responsibility where an employee is expected to deliver measurable results"
    },
    {
        "question": "Providing effective feedback in HR processes requires feedback to be:",
        "options": ["Only positive to maintain morale", "Specific, timely, balanced and focused on behaviour and outcomes rather than personality", "Given only during the annual review", "Delivered only in writing"],
        "correct_answer": "Specific, timely, balanced and focused on behaviour and outcomes rather than personality"
    },
    {
        "question": "Action planning in performance management involves:",
        "options": ["Planning the company's strategic initiatives", "Agreeing on specific steps the employee and manager will take to address performance gaps or development needs", "Setting the annual HR budget", "Planning the company's recruitment calendar"],
        "correct_answer": "Agreeing on specific steps the employee and manager will take to address performance gaps or development needs"
    },
    {
        "question": "Onboarding and induction as an HR process ensures:",
        "options": ["Only compliance paperwork is completed", "New employees are integrated effectively into the organisation, their role and the team, accelerating productivity and engagement", "The probation period is shortened", "Only technical training is provided to new hires"],
        "correct_answer": "New employees are integrated effectively into the organisation, their role and the team, accelerating productivity and engagement"
    },
    {
        "question": "Recruitment channels in modern HR include:",
        "options": ["Only newspaper advertisements", "Job boards, LinkedIn, social media, employee referrals, recruitment agencies and direct sourcing", "Only internal job postings", "Only university campus recruitment"],
        "correct_answer": "Job boards, LinkedIn, social media, employee referrals, recruitment agencies and direct sourcing"
    },
    {
        "question": "The purpose of HR policies within HR systems is to:",
        "options": ["Restrict employee freedom unnecessarily", "Provide consistent, fair and legally compliant guidance on employment matters across the organisation", "Replace the need for employment contracts", "Only protect the organisation from legal liability"],
        "correct_answer": "Provide consistent, fair and legally compliant guidance on employment matters across the organisation"
    },
]

INTRO_HRM_QUESTIONS = [
    {
        "question": "Modern Human Resource Management (HRM) is best described as:",
        "options": ["A purely administrative function focused on paperwork", "A strategic function that manages people as the organisation's most valuable asset to achieve business goals", "A function focused only on hiring and firing", "A compliance-only function that enforces company rules"],
        "correct_answer": "A strategic function that manages people as the organisation's most valuable asset to achieve business goals"
    },
    {
        "question": "The shift from traditional personnel management to modern HRM is characterised by:",
        "options": ["A move from strategic to administrative focus", "A move from reactive, administrative people management to proactive, strategic human capital development", "Reducing HR's involvement in business decisions", "Focusing exclusively on employee welfare programmes"],
        "correct_answer": "A move from reactive, administrative people management to proactive, strategic human capital development"
    },
    {
        "question": "In modern HRM, employees are viewed as:",
        "options": ["A cost to be minimised", "Human capital — a strategic asset whose development creates sustainable competitive advantage", "Interchangeable resources with no unique value", "Only relevant to the HR department's planning"],
        "correct_answer": "Human capital — a strategic asset whose development creates sustainable competitive advantage"
    },
    {
        "question": "The core functions of modern HRM include:",
        "options": ["Only recruitment and payroll", "Talent acquisition, learning and development, performance management, employee relations, compensation and HR strategy", "Only compliance and legal management", "Only training and development"],
        "correct_answer": "Talent acquisition, learning and development, performance management, employee relations, compensation and HR strategy"
    },
    {
        "question": "Organisational culture in modern HRM refers to:",
        "options": ["The company's product range and pricing strategy", "The shared values, beliefs, behaviours and norms that shape how people work and interact within the organisation", "The physical layout of the workplace", "The company's financial performance metrics"],
        "correct_answer": "The shared values, beliefs, behaviours and norms that shape how people work and interact within the organisation"
    },
    {
        "question": "Employee engagement in modern HRM is important because:",
        "options": ["Engaged employees require less supervision", "Highly engaged employees deliver better performance, lower absenteeism, higher retention and stronger customer outcomes", "Engagement only affects employee satisfaction surveys", "Engagement is only relevant for senior employees"],
        "correct_answer": "Highly engaged employees deliver better performance, lower absenteeism, higher retention and stronger customer outcomes"
    },
    {
        "question": "The HR Business Partner model in modern HRM positions HR as:",
        "options": ["An administrative support function only", "A strategic partner embedded in the business to align people strategies with business objectives", "A compliance and legal enforcement function", "A recruitment agency for the organisation"],
        "correct_answer": "A strategic partner embedded in the business to align people strategies with business objectives"
    },
    {
        "question": "Talent management in modern HRM encompasses:",
        "options": ["Only managing high-potential employees", "The end-to-end process of attracting, developing, engaging and retaining the talent needed to execute the business strategy", "Only succession planning for senior roles", "Only the recruitment and selection process"],
        "correct_answer": "The end-to-end process of attracting, developing, engaging and retaining the talent needed to execute the business strategy"
    },
    {
        "question": "Continuous learning and development in modern HRM is driven by:",
        "options": ["Only mandatory compliance training requirements", "The need to build agile, capable workforces that can adapt to rapidly changing business environments and technology", "Only the preferences of individual employees", "Only the annual training budget allocation"],
        "correct_answer": "The need to build agile, capable workforces that can adapt to rapidly changing business environments and technology"
    },
    {
        "question": "The strategic value of modern HRM is demonstrated through:",
        "options": ["Reducing all people-related costs", "Improving organisational performance, building capability, driving engagement and enabling the business to achieve its strategic objectives", "Eliminating the need for external recruitment", "Automating all HR administrative processes"],
        "correct_answer": "Improving organisational performance, building capability, driving engagement and enabling the business to achieve its strategic objectives"
    },
]

CUSTOMER_SERVICE_QUESTIONS = [
    {
        "question": "Excellent customer service is best defined as:",
        "options": ["Resolving customer complaints as quickly as possible", "Consistently meeting and exceeding customer expectations by delivering helpful, professional and personalised experiences", "Offering the lowest prices in the market", "Responding to customers only when they complain"],
        "correct_answer": "Consistently meeting and exceeding customer expectations by delivering helpful, professional and personalised experiences"
    },
    {
        "question": "Active listening in customer service involves:",
        "options": ["Waiting for the customer to finish speaking before preparing your response", "Fully concentrating on the customer, understanding their message, responding thoughtfully and confirming understanding", "Interrupting the customer to offer solutions quickly", "Only listening to customers who are calm and polite"],
        "correct_answer": "Fully concentrating on the customer, understanding their message, responding thoughtfully and confirming understanding"
    },
    {
        "question": "Empathy in customer service means:",
        "options": ["Agreeing with everything the customer says", "Understanding and acknowledging the customer's feelings and perspective, making them feel heard and valued", "Apologising for every issue regardless of fault", "Offering a discount to resolve every complaint"],
        "correct_answer": "Understanding and acknowledging the customer's feelings and perspective, making them feel heard and valued"
    },
    {
        "question": "When handling a difficult customer, the best approach is to:",
        "options": ["Argue with the customer to defend the company's position", "Stay calm, listen actively, acknowledge their frustration and focus on finding a solution", "Transfer the customer to another department immediately", "Offer a refund without investigating the issue"],
        "correct_answer": "Stay calm, listen actively, acknowledge their frustration and focus on finding a solution"
    },
    {
        "question": "Understanding customer needs requires:",
        "options": ["Assuming all customers want the same thing", "Asking open-ended questions, listening carefully and observing cues to identify what the customer truly needs", "Only responding to what the customer explicitly states", "Offering all available products and services to every customer"],
        "correct_answer": "Asking open-ended questions, listening carefully and observing cues to identify what the customer truly needs"
    },
    {
        "question": "Customer loyalty is built through:",
        "options": ["Offering the lowest prices consistently", "Delivering consistently positive experiences, building trust and making customers feel valued over time", "Resolving complaints with discounts only", "Contacting customers only when there is a problem"],
        "correct_answer": "Delivering consistently positive experiences, building trust and making customers feel valued over time"
    },
    {
        "question": "Effective communication in customer service should be:",
        "options": ["Technical and detailed to demonstrate expertise", "Clear, concise, professional and adapted to the customer's level of understanding and communication style", "Formal and scripted at all times", "Limited to written communication only"],
        "correct_answer": "Clear, concise, professional and adapted to the customer's level of understanding and communication style"
    },
    {
        "question": "A customer complaint should be viewed as:",
        "options": ["An inconvenience to be resolved as quickly as possible", "A valuable opportunity to understand customer needs, improve service and strengthen the relationship", "Evidence that the customer is difficult", "A reason to review the customer's account"],
        "correct_answer": "A valuable opportunity to understand customer needs, improve service and strengthen the relationship"
    },
    {
        "question": "First Call Resolution (FCR) in customer service refers to:",
        "options": ["Answering the customer's call within the first ring", "Resolving the customer's issue completely during the first interaction without requiring follow-up", "The first call a new customer makes to the company", "Resolving only simple queries on the first call"],
        "correct_answer": "Resolving the customer's issue completely during the first interaction without requiring follow-up"
    },
    {
        "question": "The Net Promoter Score (NPS) measures:",
        "options": ["Employee satisfaction with their manager", "The likelihood that customers would recommend the company to others, indicating overall customer loyalty", "The number of customer complaints received", "The average time to resolve customer issues"],
        "correct_answer": "The likelihood that customers would recommend the company to others, indicating overall customer loyalty"
    },
    {
        "question": "Product knowledge in customer service is important because:",
        "options": ["It allows staff to upsell to every customer", "It enables service staff to provide accurate, confident and helpful information that builds customer trust and resolves issues effectively", "It replaces the need for empathy and communication skills", "It is only relevant for technical support roles"],
        "correct_answer": "It enables service staff to provide accurate, confident and helpful information that builds customer trust and resolves issues effectively"
    },
    {
        "question": "Following up with a customer after resolving their issue demonstrates:",
        "options": ["That the company does not trust its own resolution", "Commitment to customer satisfaction and a proactive approach to ensuring the issue was fully resolved", "That the initial resolution was inadequate", "Only that the company wants to sell additional products"],
        "correct_answer": "Commitment to customer satisfaction and a proactive approach to ensuring the issue was fully resolved"
    },
    {
        "question": "Positive body language in face-to-face customer service includes:",
        "options": ["Crossed arms and minimal eye contact", "Open posture, appropriate eye contact, a genuine smile and attentive body language that signals engagement and respect", "Looking at a screen while the customer speaks", "Standing at a distance to give the customer space"],
        "correct_answer": "Open posture, appropriate eye contact, a genuine smile and attentive body language that signals engagement and respect"
    },
    {
        "question": "Service recovery refers to:",
        "options": ["Recovering lost customer data", "The actions taken to resolve a service failure and restore customer satisfaction and trust", "Recovering unpaid customer invoices", "The process of onboarding new customers"],
        "correct_answer": "The actions taken to resolve a service failure and restore customer satisfaction and trust"
    },
    {
        "question": "The ultimate goal of excellent customer service is to:",
        "options": ["Minimise the cost of the customer service department", "Create loyal customers who return, spend more and recommend the company to others, driving sustainable business growth", "Resolve all complaints within 24 hours", "Reduce the number of customer interactions"],
        "correct_answer": "Create loyal customers who return, spend more and recommend the company to others, driving sustainable business growth"
    },
]

async def add():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    # Course 59: HR Systems and Processes
    c59 = await db.courses.find_one({"id": "1691275b-0076-4ee9-add3-11e077ccfa2a"})
    if c59:
        print(f"Found: {c59['title']}")
        module = await db.modules.find_one({"course_id": c59["id"]})
        existing = await db.quizzes.find_one({"module_id": module["id"]})
        if existing:
            await db.quizzes.delete_one({"module_id": module["id"]})
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()), "module_id": module["id"], "course_id": c59["id"],
            "title": "Human Resource Systems and Processes - Final Assessment",
            "description": "Test your knowledge of HR systems, recruitment, performance management and HR policies. You need 70% to pass.",
            "passing_score": 70,
            "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(HR_SYSTEMS_QUESTIONS)]
        })
        print(f"Added quiz with {len(HR_SYSTEMS_QUESTIONS)} questions to '{c59['title']}'")
    else:
        print("HR Systems course not found")

    # Course 60: Introduction to Modern HRM
    c60 = await db.courses.find_one({"title": {"$regex": "introduction to modern human resource", "$options": "i"}})
    if c60:
        print(f"Found: {c60['title']}")
        module = await db.modules.find_one({"course_id": c60["id"]})
        existing = await db.quizzes.find_one({"module_id": module["id"]})
        if existing:
            await db.quizzes.delete_one({"module_id": module["id"]})
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()), "module_id": module["id"], "course_id": c60["id"],
            "title": "Introduction to Modern Human Resource Management - Final Assessment",
            "description": "Test your knowledge of modern HRM principles, human capital, talent management and strategic HR. You need 70% to pass.",
            "passing_score": 70,
            "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(INTRO_HRM_QUESTIONS)]
        })
        print(f"Added quiz with {len(INTRO_HRM_QUESTIONS)} questions to '{c60['title']}'")
    else:
        print("Intro Modern HRM course not found")

    # Course 61: Customer Service Skills
    c61 = await db.courses.find_one({"title": {"$regex": "customer service skills", "$options": "i"}})
    if c61:
        print(f"Found: {c61['title']}")
        module = await db.modules.find_one({"course_id": c61["id"]})
        existing = await db.quizzes.find_one({"module_id": module["id"]})
        if existing:
            await db.quizzes.delete_one({"module_id": module["id"]})
        await db.quizzes.insert_one({
            "id": str(uuid.uuid4()), "module_id": module["id"], "course_id": c61["id"],
            "title": "Customer Service Skills - Final Assessment",
            "description": "Test your knowledge of customer service principles, communication, complaint handling and building customer loyalty. You need 70% to pass.",
            "passing_score": 70,
            "questions": [{"question": q["question"], "question_type": "multiple_choice", "options": q["options"], "correct_answer": q["correct_answer"], "points": 1, "order": i} for i, q in enumerate(CUSTOMER_SERVICE_QUESTIONS)]
        })
        print(f"Added quiz with {len(CUSTOMER_SERVICE_QUESTIONS)} questions to '{c61['title']}'")
    else:
        print("Customer Service Skills course not found")

    client.close()

if __name__ == "__main__":
    asyncio.run(add())
