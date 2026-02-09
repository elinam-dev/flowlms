"""
Flowitec Go & Grow LMS - Sales Engineering Course Catalog
17 Comprehensive Sales Courses for the SALES (ENGINEER) Category
All content is tailored for Flowitec - a company selling pumps, valves, and fluid control solutions
"""

import uuid
from datetime import datetime, timezone

# Course 1: Customer Service Skills for Industrial Equipment
COURSE_1 = {
    "title": "Customer Service Skills for Industrial Equipment",
    "description": "Master the art of providing exceptional customer service in the industrial equipment sector. Learn how to understand customer needs, handle inquiries about pumps, valves, and fluid systems, and build lasting relationships with clients in the B2B industrial space.",
    "thumbnail": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=225&fit=crop",
    "category": "SALES (ENGINEER)",
    "duration_hours": 15,
    "code": "SE-CS-001",
    "modules": [
        {
            "title": "Module 1: Understanding Industrial Customer Service",
            "lessons": [
                {
                    "title": "Introduction to Customer Service in the Industrial Sector",
                    "content": """<div class="lesson-content">
<h2>Welcome to Customer Service Excellence at Flowitec</h2>
<p>In the industrial equipment sector, customer service goes far beyond answering phone calls. At Flowitec, we are trusted partners in our clients' operations, providing critical components like pumps, valves, and fluid control systems that keep their businesses running.</p>

<h3>What Makes Industrial Customer Service Unique?</h3>
<div class="highlight-box">
<p>Unlike retail or consumer services, industrial customer service involves:</p>
<ul>
<li><strong>Technical complexity</strong> - Understanding product specifications, applications, and compatibility</li>
<li><strong>Higher stakes</strong> - Equipment failures can halt entire production lines</li>
<li><strong>Longer relationships</strong> - B2B relationships span years or decades</li>
<li><strong>Multiple stakeholders</strong> - Engineers, procurement, operations, and management</li>
</ul>
</div>

<h3>The Flowitec Customer Service Philosophy</h3>
<p>At Flowitec, we believe that exceptional customer service is the foundation of our success. Our customers rely on us for:</p>
<ul>
<li>High-quality pumps and valves for critical applications</li>
<li>Expert technical guidance on product selection</li>
<li>Reliable delivery and after-sales support</li>
<li>Quick response to urgent operational needs</li>
</ul>

<div class="info-box">
<h4>Key Takeaway</h4>
<p>Every interaction with a customer is an opportunity to strengthen our relationship and demonstrate why Flowitec is the preferred partner for fluid control solutions.</p>
</div>
</div>"""
                },
                {
                    "title": "The Role of a Sales Engineer in Customer Service",
                    "content": """<div class="lesson-content">
<h2>Your Role as a Sales Engineer</h2>
<p>As a Sales Engineer at Flowitec, you are the bridge between our technical capabilities and our customers' needs. You combine technical knowledge with customer service skills to deliver comprehensive solutions.</p>

<h3>Key Responsibilities</h3>
<div class="responsibilities-grid">
<div class="resp-card">
<h4>Technical Advisory</h4>
<p>Provide expert guidance on pump and valve selection for specific applications, considering factors like flow rate, pressure, media type, and operating conditions.</p>
</div>
<div class="resp-card">
<h4>Solution Design</h4>
<p>Work with customers to design fluid handling systems that meet their operational requirements and budget constraints.</p>
</div>
<div class="resp-card">
<h4>Problem Resolution</h4>
<p>Quickly diagnose and resolve technical issues, whether related to product performance, installation, or compatibility.</p>
</div>
<div class="resp-card">
<h4>Relationship Building</h4>
<p>Develop long-term partnerships with key accounts through consistent, reliable service and proactive communication.</p>
</div>
</div>

<h3>The Flowitec Product Portfolio</h3>
<p>To serve customers effectively, you must be familiar with our complete range:</p>
<table class="product-table">
<tr><th>Category</th><th>Products</th><th>Key Applications</th></tr>
<tr><td>Centrifugal Pumps</td><td>Single-stage, Multi-stage, Self-priming</td><td>Water transfer, HVAC, Industrial processes</td></tr>
<tr><td>Positive Displacement Pumps</td><td>Gear, Diaphragm, Peristaltic</td><td>Chemical dosing, High-viscosity fluids</td></tr>
<tr><td>Gate Valves</td><td>Rising stem, Non-rising stem</td><td>Isolation, On/Off control</td></tr>
<tr><td>Ball Valves</td><td>Full bore, Reduced bore, V-port</td><td>General service, Throttling</td></tr>
<tr><td>Check Valves</td><td>Swing, Wafer, Silent</td><td>Backflow prevention</td></tr>
<tr><td>Control Valves</td><td>Globe, Butterfly, Pressure regulators</td><td>Process control, Flow regulation</td></tr>
</table>

<div class="info-box">
<h4>Remember</h4>
<p>Your technical expertise combined with excellent customer service skills makes you invaluable to both Flowitec and our customers.</p>
</div>
</div>"""
                },
                {
                    "title": "Understanding Customer Expectations in B2B",
                    "content": """<div class="lesson-content">
<h2>What Industrial Customers Expect</h2>
<p>Understanding customer expectations is the first step to exceeding them. In the industrial equipment sector, expectations are shaped by operational needs, budgets, and past experiences.</p>

<h3>The Five Pillars of Customer Expectation</h3>

<div class="pillar-section">
<div class="pillar">
<h4>1. Reliability</h4>
<p>Customers expect our products to perform consistently and our service to be dependable. When they order a pump or valve, they need it to arrive on time and work as specified.</p>
<ul>
<li>Products that meet specifications</li>
<li>Accurate delivery timelines</li>
<li>Consistent quality across orders</li>
</ul>
</div>

<div class="pillar">
<h4>2. Expertise</h4>
<p>As a Sales Engineer, customers expect you to know more about pumps and valves than they do. They rely on your expertise for:</p>
<ul>
<li>Product recommendations based on their application</li>
<li>Technical troubleshooting</li>
<li>Industry best practices</li>
</ul>
</div>

<div class="pillar">
<h4>3. Responsiveness</h4>
<p>In industrial operations, time is money. A broken pump can halt production and cost thousands per hour. Customers expect:</p>
<ul>
<li>Quick response to inquiries (within 24 hours maximum)</li>
<li>Emergency support availability</li>
<li>Proactive communication on order status</li>
</ul>
</div>

<div class="pillar">
<h4>4. Transparency</h4>
<p>Customers appreciate honesty, even when the news isn't good. They expect:</p>
<ul>
<li>Clear pricing without hidden fees</li>
<li>Honest lead time estimates</li>
<li>Upfront communication about potential issues</li>
</ul>
</div>

<div class="pillar">
<h4>5. Partnership</h4>
<p>The best customer relationships go beyond transactions. Customers value suppliers who:</p>
<ul>
<li>Understand their business challenges</li>
<li>Offer proactive solutions</li>
<li>Provide value beyond just selling products</li>
</ul>
</div>
</div>

<div class="highlight-box">
<h4>Flowitec Standard</h4>
<p>At Flowitec, we aim to exceed these expectations at every touchpoint. This is how we differentiate ourselves from competitors and build lasting customer loyalty.</p>
</div>
</div>"""
                },
                {
                    "title": "The Customer Journey in Industrial Sales",
                    "content": """<div class="lesson-content">
<h2>Mapping the Industrial Customer Journey</h2>
<p>Understanding the customer journey helps you anticipate needs and provide proactive service at each stage.</p>

<h3>The Six Stages of the Customer Journey</h3>

<div class="journey-timeline">
<div class="stage">
<div class="stage-number">1</div>
<h4>Awareness</h4>
<p>Customer identifies a need for pumps, valves, or fluid handling equipment. They may be:</p>
<ul>
<li>Planning a new project or facility</li>
<li>Replacing aging equipment</li>
<li>Addressing operational problems</li>
</ul>
<p><strong>Your Role:</strong> Be visible through marketing, referrals, and industry presence.</p>
</div>

<div class="stage">
<div class="stage-number">2</div>
<h4>Research & Evaluation</h4>
<p>Customer compares suppliers, products, and pricing. Key factors include:</p>
<ul>
<li>Technical specifications</li>
<li>Price and total cost of ownership</li>
<li>Supplier reputation and reliability</li>
</ul>
<p><strong>Your Role:</strong> Provide detailed technical information, case studies, and competitive analysis.</p>
</div>

<div class="stage">
<div class="stage-number">3</div>
<h4>Purchase Decision</h4>
<p>Customer selects Flowitec and places an order. This stage involves:</p>
<ul>
<li>Final negotiations</li>
<li>Contract signing</li>
<li>Order confirmation</li>
</ul>
<p><strong>Your Role:</strong> Facilitate smooth ordering, confirm specifications, and set clear expectations.</p>
</div>

<div class="stage">
<div class="stage-number">4</div>
<h4>Delivery & Installation</h4>
<p>Products are delivered and installed. Customer expectations are highest during this phase:</p>
<ul>
<li>On-time delivery</li>
<li>Products match specifications</li>
<li>Installation support if needed</li>
</ul>
<p><strong>Your Role:</strong> Monitor delivery, provide installation guidance, verify customer satisfaction.</p>
</div>

<div class="stage">
<div class="stage-number">5</div>
<h4>Operation & Support</h4>
<p>Equipment is in service. Customer may need:</p>
<ul>
<li>Technical support</li>
<li>Spare parts</li>
<li>Maintenance advice</li>
</ul>
<p><strong>Your Role:</strong> Provide ongoing support, preventive maintenance recommendations.</p>
</div>

<div class="stage">
<div class="stage-number">6</div>
<h4>Loyalty & Advocacy</h4>
<p>Satisfied customers become repeat buyers and recommend Flowitec to others:</p>
<ul>
<li>Repeat orders</li>
<li>Referrals</li>
<li>Long-term partnerships</li>
</ul>
<p><strong>Your Role:</strong> Nurture relationship, seek referrals, explore expansion opportunities.</p>
</div>
</div>

<div class="info-box">
<h4>Key Insight</h4>
<p>Customer service quality at every stage of this journey determines whether we earn a one-time sale or a lifetime customer.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 2: Communication Excellence",
            "lessons": [
                {
                    "title": "Professional Communication in Technical Sales",
                    "content": """<div class="lesson-content">
<h2>The Art of Technical Communication</h2>
<p>As a Sales Engineer at Flowitec, you must bridge the gap between complex technical concepts and customer understanding. Effective communication is your most powerful tool.</p>

<h3>The Communication Triangle</h3>
<div class="triangle-model">
<div class="triangle-point">
<h4>Clarity</h4>
<p>Use clear, concise language. Avoid jargon unless the customer is technically fluent.</p>
</div>
<div class="triangle-point">
<h4>Accuracy</h4>
<p>Ensure all technical specifications and information are correct. One error can damage credibility.</p>
</div>
<div class="triangle-point">
<h4>Relevance</h4>
<p>Focus on information that matters to the customer. Don't overwhelm with unnecessary details.</p>
</div>
</div>

<h3>Adapting Your Communication Style</h3>
<p>Different stakeholders require different communication approaches:</p>

<table class="comm-styles">
<tr><th>Audience</th><th>Focus</th><th>Communication Style</th></tr>
<tr><td>Engineers</td><td>Technical specifications, performance data</td><td>Detailed, data-driven, technical terminology</td></tr>
<tr><td>Procurement</td><td>Price, lead time, terms</td><td>Business-focused, ROI, competitive comparison</td></tr>
<tr><td>Operations</td><td>Reliability, ease of maintenance</td><td>Practical, problem-solving oriented</td></tr>
<tr><td>Management</td><td>Total cost, strategic fit</td><td>High-level, business impact, executive summary</td></tr>
</table>

<h3>Example: Describing a Centrifugal Pump</h3>
<div class="example-box">
<p><strong>To an Engineer:</strong> "This Flowitec CP-200 centrifugal pump delivers 200 m³/h at 40m head, with an efficiency of 78% at the best efficiency point. The NPSH required is 3.5m, suitable for your available NPSH of 5m."</p>

<p><strong>To Procurement:</strong> "The Flowitec CP-200 offers the best value in its class, with a 5-year warranty and the lowest total cost of ownership due to its high efficiency and minimal maintenance requirements."</p>

<p><strong>To Operations:</strong> "The CP-200 is designed for easy maintenance with a back pull-out design, allowing impeller access without disturbing piping. Seal replacement takes under 30 minutes."</p>
</div>

<div class="highlight-box">
<h4>Flowitec Communication Standard</h4>
<p>Every communication should be professional, accurate, and focused on the customer's specific needs and concerns.</p>
</div>
</div>"""
                },
                {
                    "title": "Active Listening for Customer Needs",
                    "content": """<div class="lesson-content">
<h2>Active Listening: The Foundation of Understanding</h2>
<p>Before you can provide solutions, you must truly understand the customer's needs. Active listening is the skill that transforms good sales engineers into exceptional ones.</p>

<h3>The HEAR Framework</h3>
<div class="framework">
<div class="fw-item">
<h4>H - Halt</h4>
<p>Stop what you're doing and give the customer your full attention. Close email, put away your phone, and focus completely on the conversation.</p>
</div>
<div class="fw-item">
<h4>E - Engage</h4>
<p>Show you're listening through verbal cues ("I understand", "Yes, go on") and non-verbal cues (nodding, maintaining eye contact).</p>
</div>
<div class="fw-item">
<h4>A - Anticipate</h4>
<p>Listen for underlying needs, not just stated requirements. What problem is the customer really trying to solve?</p>
</div>
<div class="fw-item">
<h4>R - Respond</h4>
<p>Summarize what you've heard to confirm understanding before proposing solutions.</p>
</div>
</div>

<h3>Asking the Right Questions</h3>
<p>Effective questions uncover true customer needs:</p>

<div class="question-types">
<div class="q-type">
<h4>Open Questions</h4>
<p>Start with What, How, Why to encourage detailed responses:</p>
<ul>
<li>"What challenges are you experiencing with your current pumping system?"</li>
<li>"How does this equipment fit into your overall process?"</li>
<li>"Why is this project a priority right now?"</li>
</ul>
</div>

<div class="q-type">
<h4>Probing Questions</h4>
<p>Dig deeper into specific areas:</p>
<ul>
<li>"Can you tell me more about the operating conditions?"</li>
<li>"What flow rates are you working with?"</li>
<li>"What's the fluid temperature and viscosity?"</li>
</ul>
</div>

<div class="q-type">
<h4>Confirming Questions</h4>
<p>Verify your understanding:</p>
<ul>
<li>"So if I understand correctly, you need a pump that can handle 150°C water at 10 bar pressure?"</li>
<li>"Just to confirm, your main priority is reliability over initial cost?"</li>
</ul>
</div>
</div>

<h3>What to Listen For</h3>
<p>Pay attention to these key elements:</p>
<ul>
<li><strong>Application details</strong> - What will the equipment be used for?</li>
<li><strong>Operating conditions</strong> - Temperature, pressure, flow rate, media</li>
<li><strong>Pain points</strong> - What problems have they experienced before?</li>
<li><strong>Decision factors</strong> - What matters most (price, quality, delivery)?</li>
<li><strong>Timeline</strong> - When do they need the equipment?</li>
</ul>

<div class="info-box">
<h4>Remember</h4>
<p>Customers don't buy pumps and valves - they buy solutions to their problems. Active listening helps you understand the real problem behind the inquiry.</p>
</div>
</div>"""
                },
                {
                    "title": "Written Communication Best Practices",
                    "content": """<div class="lesson-content">
<h2>Professional Written Communication</h2>
<p>In B2B sales, written communication creates lasting impressions and serves as official records. Your emails, quotations, and technical documents represent Flowitec's professionalism.</p>

<h3>Email Excellence</h3>
<div class="email-structure">
<h4>Subject Line</h4>
<p>Clear, specific, and action-oriented:</p>
<ul>
<li>✓ "Quotation for ABC Mining - 3x Centrifugal Pumps (REF: Q-2024-0456)"</li>
<li>✗ "Your enquiry"</li>
</ul>

<h4>Opening</h4>
<p>Professional greeting and context:</p>
<ul>
<li>✓ "Dear Mr. Mensah, Thank you for your inquiry regarding pumps for your cooling water system."</li>
<li>✗ "Hi, got your message"</li>
</ul>

<h4>Body</h4>
<p>Organized, concise, and relevant:</p>
<ul>
<li>Use bullet points for multiple items</li>
<li>Keep paragraphs short (3-4 sentences max)</li>
<li>Include specific details (model numbers, prices, lead times)</li>
</ul>

<h4>Closing</h4>
<p>Clear next steps and professional sign-off:</p>
<ul>
<li>✓ "Please let me know if you need any clarification. I'll follow up on Friday to discuss next steps."</li>
<li>Include your full signature with contact details</li>
</ul>
</div>

<h3>Technical Documents</h3>
<p>When preparing quotations and technical proposals:</p>

<div class="doc-checklist">
<h4>Quotation Checklist</h4>
<ul>
<li>□ Customer name and reference correct</li>
<li>□ Product specifications accurate</li>
<li>□ Prices and currency clearly stated</li>
<li>□ Delivery terms and timeline specified</li>
<li>□ Payment terms included</li>
<li>□ Validity period stated</li>
<li>□ Terms and conditions attached</li>
</ul>
</div>

<h3>Common Mistakes to Avoid</h3>
<div class="mistakes-list">
<div class="mistake">
<span class="cross">✗</span>
<p>Spelling and grammar errors</p>
</div>
<div class="mistake">
<span class="cross">✗</span>
<p>Wrong customer name or company</p>
</div>
<div class="mistake">
<span class="cross">✗</span>
<p>Incorrect technical specifications</p>
</div>
<div class="mistake">
<span class="cross">✗</span>
<p>Missing attachments mentioned in email</p>
</div>
<div class="mistake">
<span class="cross">✗</span>
<p>Delayed responses without acknowledgment</p>
</div>
</div>

<div class="highlight-box">
<h4>Flowitec Standard</h4>
<p>All written communications should be proofread before sending. When in doubt, have a colleague review important documents.</p>
</div>
</div>"""
                },
                {
                    "title": "Telephone and Virtual Meeting Etiquette",
                    "content": """<div class="lesson-content">
<h2>Professional Telephone and Virtual Presence</h2>
<p>Even in our digital age, phone calls and virtual meetings remain critical touchpoints with customers. Your professional conduct on these platforms reflects on Flowitec.</p>

<h3>Telephone Best Practices</h3>
<div class="phone-guide">
<h4>Answering Calls</h4>
<ul>
<li>Answer within 3 rings when possible</li>
<li>Use a professional greeting: "Good morning, Flowitec Sales, this is [Name] speaking. How may I help you?"</li>
<li>Smile when you speak - it affects your tone</li>
<li>Have a notepad ready for taking notes</li>
</ul>

<h4>During the Call</h4>
<ul>
<li>Speak clearly and at a moderate pace</li>
<li>Use the customer's name periodically</li>
<li>Avoid putting customers on hold unnecessarily</li>
<li>If you must hold, ask permission and provide a time estimate</li>
<li>Take detailed notes for follow-up</li>
</ul>

<h4>Closing the Call</h4>
<ul>
<li>Summarize agreed actions</li>
<li>Confirm next steps and timeline</li>
<li>Thank the customer for their time</li>
<li>Allow the customer to hang up first</li>
</ul>
</div>

<h3>Virtual Meeting Excellence</h3>
<div class="virtual-guide">
<h4>Before the Meeting</h4>
<ul>
<li>Test your technology (camera, microphone, internet connection)</li>
<li>Set up in a quiet, professional environment</li>
<li>Have relevant documents open and ready to share</li>
<li>Dress professionally (yes, even from home)</li>
<li>Join 2-3 minutes early</li>
</ul>

<h4>During the Meeting</h4>
<ul>
<li>Keep camera on whenever possible</li>
<li>Look at the camera when speaking (not the screen)</li>
<li>Mute when not speaking to reduce background noise</li>
<li>Use screen sharing effectively for presentations</li>
<li>Be mindful of time zones for international customers</li>
</ul>

<h4>Handling Technical Difficulties</h4>
<ul>
<li>Have a backup plan (phone number, alternative platform)</li>
<li>Communicate immediately if you're having issues</li>
<li>Don't let technical problems derail the meeting's purpose</li>
</ul>
</div>

<h3>Voicemail Guidelines</h3>
<div class="voicemail-template">
<p><strong>Template:</strong> "Hello, this is [Name] from Flowitec calling for [Customer Name] regarding [Topic]. My number is [Number]. I'll try calling again [When] or please feel free to return my call. Thank you."</p>
</div>

<div class="info-box">
<h4>Key Point</h4>
<p>Every phone call and virtual meeting is an opportunity to demonstrate Flowitec's professionalism and customer commitment.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 3: Understanding Flowitec Products",
            "lessons": [
                {
                    "title": "Pump Technology Fundamentals",
                    "content": """<div class="lesson-content">
<h2>Understanding Pump Technology</h2>
<p>As a Sales Engineer, deep product knowledge enables you to recommend the right solutions and answer customer questions confidently. Let's explore the fundamentals of pump technology.</p>

<h3>How Pumps Work</h3>
<p>Pumps transfer mechanical energy to a fluid, increasing its pressure or velocity. All pumps fall into two main categories:</p>

<div class="pump-types">
<div class="pump-type">
<h4>Dynamic Pumps (Centrifugal)</h4>
<p>Use rotating impellers to impart velocity to the fluid, which is then converted to pressure.</p>
<ul>
<li><strong>Principle:</strong> Centrifugal force from rotating impeller</li>
<li><strong>Flow:</strong> Continuous, smooth</li>
<li><strong>Best for:</strong> High flow, low to medium pressure</li>
<li><strong>Flowitec Range:</strong> CP Series, Multi-stage, Booster pumps</li>
</ul>
</div>

<div class="pump-type">
<h4>Positive Displacement Pumps</h4>
<p>Trap and move fixed volumes of fluid with each cycle.</p>
<ul>
<li><strong>Principle:</strong> Mechanical displacement of fluid</li>
<li><strong>Flow:</strong> Pulsating, but precise</li>
<li><strong>Best for:</strong> High pressure, viscous fluids, precise dosing</li>
<li><strong>Flowitec Range:</strong> Gear pumps, Diaphragm pumps, Peristaltic pumps</li>
</ul>
</div>
</div>

<h3>Key Pump Parameters</h3>
<p>Understanding these parameters is essential for correct pump selection:</p>

<table class="param-table">
<tr><th>Parameter</th><th>Definition</th><th>Units</th></tr>
<tr><td>Flow Rate (Q)</td><td>Volume of fluid pumped per unit time</td><td>m³/h, L/min, GPM</td></tr>
<tr><td>Head (H)</td><td>Energy imparted to fluid, expressed as height</td><td>meters, feet</td></tr>
<tr><td>NPSH</td><td>Net Positive Suction Head - pressure available at pump inlet</td><td>meters</td></tr>
<tr><td>Efficiency</td><td>Ratio of hydraulic power to input power</td><td>%</td></tr>
<tr><td>Power</td><td>Energy consumption</td><td>kW, HP</td></tr>
</table>

<h3>The Pump Performance Curve</h3>
<p>Every pump has a characteristic curve showing the relationship between flow and head:</p>
<div class="curve-explanation">
<ul>
<li><strong>Best Efficiency Point (BEP):</strong> The point where the pump operates most efficiently</li>
<li><strong>Operating Range:</strong> Pumps should operate within 70-120% of BEP flow</li>
<li><strong>Cavitation Zone:</strong> Area where NPSH available is insufficient - causes damage</li>
</ul>
</div>

<div class="highlight-box">
<h4>Sales Tip</h4>
<p>Always select pumps to operate near their BEP. This ensures maximum efficiency, minimum wear, and longest service life - key selling points for customers.</p>
</div>
</div>"""
                },
                {
                    "title": "Valve Technology Fundamentals",
                    "content": """<div class="lesson-content">
<h2>Understanding Valve Technology</h2>
<p>Valves are essential components in any fluid handling system. They control flow, pressure, and direction. Flowitec offers a comprehensive range to meet diverse customer needs.</p>

<h3>Valve Functions</h3>
<div class="functions-grid">
<div class="function-card">
<h4>Isolation</h4>
<p>Completely stop flow (on/off control)</p>
<p><em>Examples: Gate valves, Ball valves</em></p>
</div>
<div class="function-card">
<h4>Regulation</h4>
<p>Control flow rate or pressure</p>
<p><em>Examples: Globe valves, Control valves</em></p>
</div>
<div class="function-card">
<h4>Prevention</h4>
<p>Prevent reverse flow</p>
<p><em>Examples: Check valves</em></p>
</div>
<div class="function-card">
<h4>Safety</h4>
<p>Protect system from over-pressure</p>
<p><em>Examples: Relief valves, Safety valves</em></p>
</div>
</div>

<h3>Flowitec Valve Range</h3>
<table class="valve-table">
<tr><th>Valve Type</th><th>Application</th><th>Key Features</th></tr>
<tr><td>Gate Valve</td><td>Full isolation, on/off service</td><td>Minimal pressure drop, not for throttling</td></tr>
<tr><td>Ball Valve</td><td>Quick isolation, general service</td><td>Quarter-turn operation, tight shutoff</td></tr>
<tr><td>Globe Valve</td><td>Flow regulation, throttling</td><td>Good control characteristics, higher pressure drop</td></tr>
<tr><td>Butterfly Valve</td><td>Large pipe isolation, moderate control</td><td>Compact, lightweight, economical for large sizes</td></tr>
<tr><td>Check Valve</td><td>Backflow prevention</td><td>Automatic operation, various styles available</td></tr>
<tr><td>Control Valve</td><td>Precise flow/pressure control</td><td>Actuator-operated, various trim options</td></tr>
</table>

<h3>Valve Selection Factors</h3>
<p>When recommending valves to customers, consider:</p>
<ul>
<li><strong>Media:</strong> Water, chemicals, gases, slurries?</li>
<li><strong>Temperature:</strong> Affects material selection</li>
<li><strong>Pressure:</strong> Determines pressure class (PN, Class)</li>
<li><strong>Size:</strong> Based on flow requirements</li>
<li><strong>End connections:</strong> Flanged, threaded, welded?</li>
<li><strong>Operation:</strong> Manual, pneumatic, electric?</li>
<li><strong>Application:</strong> Isolation, control, safety?</li>
</ul>

<h3>Materials of Construction</h3>
<div class="materials-info">
<p><strong>Body Materials:</strong> Carbon steel, Stainless steel, Cast iron, Bronze</p>
<p><strong>Seat/Seal Materials:</strong> PTFE, EPDM, Viton, Metal-to-metal</p>
<p><strong>Selection depends on:</strong> Media compatibility, temperature, pressure</p>
</div>

<div class="info-box">
<h4>Customer Value Proposition</h4>
<p>Help customers understand that selecting the right valve type and material can significantly extend service life and reduce maintenance costs.</p>
</div>
</div>"""
                },
                {
                    "title": "Application Engineering Basics",
                    "content": """<div class="lesson-content">
<h2>Application Engineering for Pumps and Valves</h2>
<p>Application engineering is about matching the right equipment to the customer's specific requirements. This skill differentiates Flowitec from competitors who simply quote from catalogs.</p>

<h3>The Application Data Sheet</h3>
<p>Always collect this information before recommending equipment:</p>

<div class="data-sheet">
<h4>Pump Application Data</h4>
<table>
<tr><td>Liquid Type</td><td>Water, oil, chemical, slurry?</td></tr>
<tr><td>Temperature</td><td>Operating and maximum</td></tr>
<tr><td>Specific Gravity</td><td>Affects power calculation</td></tr>
<tr><td>Viscosity</td><td>Critical for pump selection</td></tr>
<tr><td>Solids Content</td><td>Percentage and particle size</td></tr>
<tr><td>Flow Rate Required</td><td>Minimum, normal, maximum</td></tr>
<tr><td>Total Head</td><td>Static + friction + pressure</td></tr>
<tr><td>Suction Conditions</td><td>NPSH available</td></tr>
<tr><td>Operating Pattern</td><td>Continuous, intermittent, cyclical?</td></tr>
</table>
</div>

<h3>Common Industrial Applications</h3>
<div class="applications">
<div class="app-card">
<h4>Water Supply & Distribution</h4>
<ul>
<li>Centrifugal pumps for main transfer</li>
<li>Gate/butterfly valves for isolation</li>
<li>Check valves to prevent backflow</li>
<li>Pressure sustaining valves</li>
</ul>
</div>

<div class="app-card">
<h4>HVAC Systems</h4>
<ul>
<li>Circulating pumps for hot/chilled water</li>
<li>Balancing valves for flow distribution</li>
<li>Control valves for temperature regulation</li>
<li>Strainers to protect equipment</li>
</ul>
</div>

<div class="app-card">
<h4>Industrial Process</h4>
<ul>
<li>Chemical transfer pumps (material critical)</li>
<li>Metering pumps for precise dosing</li>
<li>Control valves for process control</li>
<li>Safety relief valves</li>
</ul>
</div>

<div class="app-card">
<h4>Mining & Heavy Industry</h4>
<ul>
<li>Slurry pumps for abrasive media</li>
<li>High-pressure multistage pumps</li>
<li>Heavy-duty knife gate valves</li>
<li>Pinch valves for slurries</li>
</ul>
</div>
</div>

<h3>Sizing Example: Cooling Water Pump</h3>
<div class="example-calculation">
<p><strong>Customer Requirement:</strong></p>
<ul>
<li>Transfer cooling water to heat exchangers</li>
<li>Flow: 100 m³/h</li>
<li>Discharge pressure: 4 bar</li>
<li>Suction: Atmospheric tank, 2m below pump</li>
<li>Temperature: 35°C</li>
</ul>

<p><strong>Calculation:</strong></p>
<ul>
<li>Static head: 4 bar = 40m + suction lift 2m = 42m</li>
<li>Friction losses (estimated): 8m</li>
<li>Total head: 50m</li>
<li>NPSH available: 10.3m - 2m - 0.5m (losses) = 7.8m</li>
</ul>

<p><strong>Recommendation:</strong> Flowitec CP-150 centrifugal pump (100 m³/h @ 55m head, NPSH required: 4m)</p>
</div>

<div class="highlight-box">
<h4>Expert Tip</h4>
<p>Always include a safety margin (10-15%) in your calculations. This accounts for system uncertainties and future capacity increases.</p>
</div>
</div>"""
                },
                {
                    "title": "Competitive Positioning and Value Proposition",
                    "content": """<div class="lesson-content">
<h2>Positioning Flowitec Against Competition</h2>
<p>Understanding how Flowitec's products compare to competitors enables you to articulate our value proposition effectively.</p>

<h3>The Flowitec Advantage</h3>
<div class="advantages">
<div class="advantage-card highlight">
<h4>Quality & Reliability</h4>
<p>All Flowitec products undergo rigorous testing and comply with international standards (ISO, API, EN). Our quality control ensures consistent performance.</p>
</div>

<div class="advantage-card">
<h4>Technical Support</h4>
<p>Our sales engineers provide expert guidance from selection through installation and beyond. We don't just sell products - we provide solutions.</p>
</div>

<div class="advantage-card">
<h4>Local Stock & Service</h4>
<p>Strategic warehousing ensures quick delivery. Our service network provides installation support and after-sales service.</p>
</div>

<div class="advantage-card">
<h4>Total Cost of Ownership</h4>
<p>While initial price may not always be lowest, Flowitec products offer the best long-term value through efficiency, durability, and low maintenance.</p>
</div>
</div>

<h3>Handling Price Objections</h3>
<p>When customers focus on price:</p>
<div class="objection-handling">
<div class="scenario">
<p><strong>Customer:</strong> "Your competitor is 15% cheaper."</p>
<p><strong>Response Strategy:</strong></p>
<ul>
<li>Acknowledge the price difference</li>
<li>Ask about the total cost comparison (warranty, efficiency, maintenance)</li>
<li>Highlight Flowitec's advantages that justify the premium</li>
<li>Calculate total cost of ownership over 5-10 years</li>
</ul>
<p><strong>Example Response:</strong> "I understand price is important. Let me show you the total cost analysis. Our pump operates at 78% efficiency versus 72% for the competitor. Over 5 years of operation, this efficiency difference saves you GHS 45,000 in electricity costs - more than offsetting the initial price difference."</p>
</div>
</div>

<h3>Value-Based Selling</h3>
<p>Focus on value, not just features:</p>
<table class="value-table">
<tr><th>Feature</th><th>Benefit</th><th>Value Statement</th></tr>
<tr><td>78% pump efficiency</td><td>Lower energy consumption</td><td>"Saves GHS 9,000/year in electricity"</td></tr>
<tr><td>5-year warranty</td><td>Peace of mind, lower risk</td><td>"No replacement costs for 5 years"</td></tr>
<tr><td>Local stock</td><td>Fast delivery</td><td>"Reduce your downtime risk"</td></tr>
<tr><td>Technical support</td><td>Correct first-time selection</td><td>"Avoid costly mistakes"</td></tr>
</table>

<div class="info-box">
<h4>Remember</h4>
<p>Price is what customers pay. Value is what they receive. Your job is to help customers see the full value that Flowitec provides.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 4: Handling Customer Complaints",
            "lessons": [
                {
                    "title": "The Psychology of Customer Complaints",
                    "content": """<div class="lesson-content">
<h2>Understanding Customer Complaints</h2>
<p>In industrial sales, complaints are inevitable. How we handle them determines whether we lose customers or strengthen relationships. At Flowitec, we view complaints as opportunities.</p>

<h3>Why Customers Complain</h3>
<div class="complaint-reasons">
<div class="reason-card">
<h4>Product Issues</h4>
<ul>
<li>Equipment not performing as expected</li>
<li>Premature failure or defects</li>
<li>Wrong product delivered</li>
<li>Specification mismatch</li>
</ul>
</div>

<div class="reason-card">
<h4>Service Issues</h4>
<ul>
<li>Late delivery</li>
<li>Poor communication</li>
<li>Unresolved problems</li>
<li>Unmet promises</li>
</ul>
</div>

<div class="reason-card">
<h4>Expectation Gaps</h4>
<ul>
<li>Misunderstanding of capabilities</li>
<li>Unrealistic expectations</li>
<li>Miscommunication</li>
</ul>
</div>
</div>

<h3>The Hidden Opportunity in Complaints</h3>
<div class="stats-box">
<p><strong>Industry Statistics:</strong></p>
<ul>
<li>For every customer who complains, 26 others remain silent</li>
<li>91% of unhappy customers who don't complain simply leave</li>
<li>A customer whose complaint is resolved quickly is 70% more likely to do business again</li>
<li>Customers who complain and are satisfied tell 5-7 others about their experience</li>
</ul>
</div>

<h3>The Customer's Emotional State</h3>
<p>When customers complain, they experience various emotions:</p>
<ul>
<li><strong>Frustration:</strong> Their operations are affected</li>
<li><strong>Disappointment:</strong> Expectations weren't met</li>
<li><strong>Anger:</strong> They feel let down or ignored</li>
<li><strong>Anxiety:</strong> Worried about the impact on their work</li>
<li><strong>Skepticism:</strong> Will the problem be resolved?</li>
</ul>

<div class="highlight-box">
<h4>Key Insight</h4>
<p>Before you can solve the technical problem, you must address the emotional problem. Acknowledge feelings first, then move to solutions.</p>
</div>
</div>"""
                },
                {
                    "title": "The HEART Method for Complaint Resolution",
                    "content": """<div class="lesson-content">
<h2>The HEART Method</h2>
<p>Flowitec uses the HEART method to handle complaints professionally and effectively. This structured approach ensures consistency and positive outcomes.</p>

<div class="heart-framework">
<div class="heart-step">
<div class="letter">H</div>
<div class="content">
<h4>Hear</h4>
<p>Listen actively without interrupting. Let the customer fully express their concern.</p>
<ul>
<li>Give your complete attention</li>
<li>Take notes on key points</li>
<li>Don't become defensive</li>
<li>Use phrases like "I understand" and "Please continue"</li>
</ul>
</div>
</div>

<div class="heart-step">
<div class="letter">E</div>
<div class="content">
<h4>Empathize</h4>
<p>Show genuine understanding of their situation and feelings.</p>
<ul>
<li>"I can understand how frustrating this must be"</li>
<li>"If I were in your position, I'd feel the same way"</li>
<li>"This situation is not acceptable, and I'm sorry you're experiencing it"</li>
</ul>
</div>
</div>

<div class="heart-step">
<div class="letter">A</div>
<div class="content">
<h4>Apologize</h4>
<p>Offer a sincere apology, even if you're not personally at fault.</p>
<ul>
<li>Apologize for the inconvenience caused</li>
<li>Take ownership on behalf of Flowitec</li>
<li>Avoid blame-shifting or excuses</li>
</ul>
</div>
</div>

<div class="heart-step">
<div class="letter">R</div>
<div class="content">
<h4>Resolve</h4>
<p>Take action to fix the problem.</p>
<ul>
<li>Propose a solution</li>
<li>If you can't solve it immediately, explain next steps</li>
<li>Give realistic timelines</li>
<li>Involve others if needed (supervisor, technical team)</li>
</ul>
</div>
</div>

<div class="heart-step">
<div class="letter">T</div>
<div class="content">
<h4>Thank</h4>
<p>Thank the customer for bringing the issue to your attention.</p>
<ul>
<li>"Thank you for letting us know about this"</li>
<li>"Your feedback helps us improve"</li>
<li>"We value your business and appreciate your patience"</li>
</ul>
</div>
</div>
</div>

<h3>Example Dialogue</h3>
<div class="dialogue-example">
<p><strong>Customer:</strong> "Your pump broke down after only 3 months! Our production line has been stopped for 2 days. This is unacceptable!"</p>

<p><strong>H - Hear:</strong> "I understand. Please tell me more about what happened."</p>

<p><strong>E - Empathize:</strong> "I can imagine how frustrating this is. Production downtime has significant costs, and you trusted us to deliver reliable equipment."</p>

<p><strong>A - Apologize:</strong> "On behalf of Flowitec, I sincerely apologize for this situation. This is not the level of performance we promise."</p>

<p><strong>R - Resolve:</strong> "Here's what we're going to do: I'll dispatch our service engineer today to assess the pump. If it's a manufacturing defect, we'll replace it under warranty and cover any additional costs incurred. Can we have someone on-site by 2 PM?"</p>

<p><strong>T - Thank:</strong> "Thank you for bringing this to my attention directly. Your business is important to us, and we'll make this right."</p>
</div>

<div class="info-box">
<h4>Remember</h4>
<p>The goal isn't just to resolve the complaint - it's to restore and strengthen the customer relationship.</p>
</div>
</div>"""
                },
                {
                    "title": "Escalation Procedures and Documentation",
                    "content": """<div class="lesson-content">
<h2>When and How to Escalate</h2>
<p>Not all complaints can be resolved at the first level. Knowing when and how to escalate ensures issues are handled appropriately.</p>

<h3>When to Escalate</h3>
<div class="escalation-triggers">
<div class="trigger">
<h4>Technical Complexity</h4>
<p>When the issue requires specialized knowledge or investigation beyond your expertise.</p>
</div>
<div class="trigger">
<h4>Financial Impact</h4>
<p>Claims or resolutions involving significant costs (typically above GHS 10,000).</p>
</div>
<div class="trigger">
<h4>Legal Implications</h4>
<p>Any mention of legal action, contractual disputes, or regulatory issues.</p>
</div>
<div class="trigger">
<h4>Repeat Issues</h4>
<p>When the same customer has complained about the same issue multiple times.</p>
</div>
<div class="trigger">
<h4>Key Accounts</h4>
<p>Major customers may require management involvement regardless of issue size.</p>
</div>
</div>

<h3>The Escalation Process</h3>
<div class="process-steps">
<div class="step">
<span class="step-num">1</span>
<h4>Document Everything</h4>
<p>Record the complaint details before escalating.</p>
</div>
<div class="step">
<span class="step-num">2</span>
<h4>Inform the Customer</h4>
<p>"I want to ensure you receive the best resolution. I'm involving our [Technical Manager/Service Manager] who has the expertise/authority to address this fully."</p>
</div>
<div class="step">
<span class="step-num">3</span>
<h4>Brief Your Colleague</h4>
<p>Provide complete background before they contact the customer. No customer should have to repeat their story.</p>
</div>
<div class="step">
<span class="step-num">4</span>
<h4>Follow Up</h4>
<p>Even after escalating, stay involved to ensure resolution and demonstrate continued care.</p>
</div>
</div>

<h3>Documentation Requirements</h3>
<div class="doc-template">
<h4>Complaint Record Template</h4>
<table>
<tr><td>Date/Time Received</td><td></td></tr>
<tr><td>Customer Name/Company</td><td></td></tr>
<tr><td>Contact Person/Number</td><td></td></tr>
<tr><td>Product/Order Reference</td><td></td></tr>
<tr><td>Description of Complaint</td><td></td></tr>
<tr><td>Customer's Desired Resolution</td><td></td></tr>
<tr><td>Immediate Actions Taken</td><td></td></tr>
<tr><td>Escalated To</td><td></td></tr>
<tr><td>Resolution Provided</td><td></td></tr>
<tr><td>Date Resolved</td><td></td></tr>
<tr><td>Customer Satisfaction Confirmed</td><td></td></tr>
</table>
</div>

<div class="highlight-box">
<h4>Flowitec Standard</h4>
<p>All complaints must be logged in our CRM system within 24 hours. This enables tracking, reporting, and continuous improvement.</p>
</div>
</div>"""
                },
                {
                    "title": "Turning Complaints into Opportunities",
                    "content": """<div class="lesson-content">
<h2>From Complaint to Opportunity</h2>
<p>The most loyal customers are often those who have had a problem resolved excellently. A well-handled complaint can strengthen relationships and create opportunities.</p>

<h3>The Recovery Paradox</h3>
<div class="paradox-box">
<p>Research shows that customers who experience a service failure followed by excellent recovery often become more loyal than customers who never had a problem at all.</p>
<p><strong>Why?</strong> Because they've seen how you respond under pressure, and that builds trust.</p>
</div>

<h3>Creating Opportunities from Complaints</h3>
<div class="opportunities">
<div class="opp-card">
<h4>Upgrade Opportunities</h4>
<p>A complaint about equipment limitations might lead to an upgrade discussion.</p>
<p><em>Example: "Since you've outgrown this pump's capacity, let's discuss our higher-capacity range that would better match your current needs."</em></p>
</div>

<div class="opp-card">
<h4>Service Contracts</h4>
<p>Equipment failure complaints can lead to preventive maintenance agreements.</p>
<p><em>Example: "To prevent future unexpected failures, I'd recommend our annual maintenance program that includes quarterly inspections."</em></p>
</div>

<div class="opp-card">
<h4>Additional Products</h4>
<p>Understanding the root cause might reveal needs for complementary products.</p>
<p><em>Example: "The premature seal wear was caused by cavitation. Installing a larger suction strainer would prevent this and extend seal life significantly."</em></p>
</div>

<div class="opp-card">
<h4>Referrals</h4>
<p>Satisfied post-complaint customers become strong advocates.</p>
<p><em>Example: "We really appreciate how you handled our issue. Do you work with other companies that might need reliable pump suppliers?"</em></p>
</div>
</div>

<h3>Post-Resolution Follow-Up</h3>
<p>Don't let the relationship end with the resolution:</p>
<ul>
<li><strong>1 Week Later:</strong> Call to confirm the resolution is holding and customer is satisfied</li>
<li><strong>1 Month Later:</strong> Check if any other needs have emerged</li>
<li><strong>Quarterly:</strong> Include in regular account review discussions</li>
</ul>

<h3>Learning from Complaints</h3>
<p>Every complaint teaches us something:</p>
<ul>
<li>Product quality issues → Feedback to manufacturing</li>
<li>Delivery problems → Logistics process improvement</li>
<li>Communication gaps → Training needs identification</li>
<li>Expectation mismatches → Improved sales processes</li>
</ul>

<div class="info-box">
<h4>Final Thought</h4>
<p>The true test of a company is not whether problems occur - they always do. The true test is how well we resolve them. At Flowitec, we aim to turn every complaint into a demonstration of our commitment to customer success.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 5: Managing Stress in Customer Service",
            "lessons": [
                {
                    "title": "Understanding Stress in Sales Roles",
                    "content": """<div class="lesson-content">
<h2>The Reality of Stress in Sales</h2>
<p>Sales engineering is rewarding but challenging. Understanding stress and developing coping strategies is essential for long-term success and well-being.</p>

<h3>Common Stressors in Industrial Sales</h3>
<div class="stressor-list">
<div class="stressor">
<h4>Target Pressure</h4>
<p>Monthly and quarterly sales targets create ongoing pressure to perform.</p>
</div>
<div class="stressor">
<h4>Customer Demands</h4>
<p>Urgent requests, unrealistic expectations, and difficult conversations.</p>
</div>
<div class="stressor">
<h4>Technical Complexity</h4>
<p>The need to stay current with products, applications, and industry knowledge.</p>
</div>
<div class="stressor">
<h4>Rejection</h4>
<p>Losing quotes to competitors or having proposals rejected.</p>
</div>
<div class="stressor">
<h4>Work-Life Balance</h4>
<p>Customer calls outside hours, travel requirements, administrative workload.</p>
</div>
</div>

<h3>Recognizing Stress Signs</h3>
<div class="signs-table">
<h4>Physical Signs</h4>
<ul>
<li>Fatigue and low energy</li>
<li>Headaches or muscle tension</li>
<li>Sleep difficulties</li>
<li>Appetite changes</li>
</ul>

<h4>Emotional Signs</h4>
<ul>
<li>Irritability or short temper</li>
<li>Anxiety about work</li>
<li>Feeling overwhelmed</li>
<li>Loss of motivation</li>
</ul>

<h4>Behavioral Signs</h4>
<ul>
<li>Procrastination</li>
<li>Withdrawal from colleagues</li>
<li>Decreased productivity</li>
<li>Increased errors</li>
</ul>
</div>

<h3>The Impact of Unmanaged Stress</h3>
<p>Chronic stress affects:</p>
<ul>
<li><strong>Performance:</strong> Reduced effectiveness in customer interactions</li>
<li><strong>Relationships:</strong> Strained relationships with colleagues and customers</li>
<li><strong>Health:</strong> Physical and mental health consequences</li>
<li><strong>Career:</strong> Burnout can lead to leaving the profession</li>
</ul>

<div class="highlight-box">
<h4>Important</h4>
<p>Managing stress is not a sign of weakness - it's a professional skill that supports sustainable high performance.</p>
</div>
</div>"""
                },
                {
                    "title": "Stress Management Techniques",
                    "content": """<div class="lesson-content">
<h2>Practical Stress Management</h2>
<p>Effective stress management combines immediate coping techniques with long-term strategies. Here are proven methods for sales professionals.</p>

<h3>Immediate Stress Relief Techniques</h3>
<div class="techniques">
<div class="technique">
<h4>The 4-7-8 Breathing Technique</h4>
<p>Before a difficult call or meeting:</p>
<ol>
<li>Breathe in quietly through your nose for 4 seconds</li>
<li>Hold your breath for 7 seconds</li>
<li>Exhale completely through your mouth for 8 seconds</li>
<li>Repeat 3-4 times</li>
</ol>
</div>

<div class="technique">
<h4>The 5-Minute Reset</h4>
<p>Between challenging customer interactions:</p>
<ul>
<li>Step away from your desk</li>
<li>Walk for 2-3 minutes</li>
<li>Drink water</li>
<li>Mentally transition before the next task</li>
</ul>
</div>

<div class="technique">
<h4>Reframe Your Thinking</h4>
<p>Change negative self-talk:</p>
<ul>
<li>Instead of: "I can't handle this customer"</li>
<li>Think: "This is a challenging situation, and I have the skills to manage it"</li>
</ul>
</div>
</div>

<h3>Daily Stress Prevention</h3>
<div class="prevention-strategies">
<div class="strategy">
<h4>Morning Routine</h4>
<ul>
<li>Start 15 minutes early to avoid rushing</li>
<li>Review your day's priorities</li>
<li>Identify potential stressors and plan responses</li>
</ul>
</div>

<div class="strategy">
<h4>Work Organization</h4>
<ul>
<li>Tackle difficult tasks when energy is highest</li>
<li>Break large tasks into smaller steps</li>
<li>Set realistic daily goals</li>
<li>Schedule buffer time between meetings</li>
</ul>
</div>

<div class="strategy">
<h4>End of Day</h4>
<ul>
<li>Complete urgent follow-ups</li>
<li>Prepare tomorrow's priority list</li>
<li>Leave work at work when possible</li>
<li>Transition activity (music, podcast, short walk)</li>
</ul>
</div>
</div>

<h3>Long-Term Resilience Building</h3>
<ul>
<li><strong>Physical Exercise:</strong> Regular activity reduces stress hormones</li>
<li><strong>Adequate Sleep:</strong> 7-8 hours improves coping ability</li>
<li><strong>Social Support:</strong> Connect with colleagues who understand the role</li>
<li><strong>Professional Development:</strong> Confidence in skills reduces anxiety</li>
<li><strong>Hobbies:</strong> Activities outside work provide mental breaks</li>
</ul>

<div class="info-box">
<h4>Flowitec Support</h4>
<p>If stress becomes overwhelming, speak with your manager or HR. Flowitec values employee well-being and has resources to support you.</p>
</div>
</div>"""
                },
                {
                    "title": "Handling Difficult Customers",
                    "content": """<div class="lesson-content">
<h2>Strategies for Difficult Customer Interactions</h2>
<p>Some customer interactions are inherently challenging. Having strategies prepared helps you handle them professionally while protecting your well-being.</p>

<h3>Types of Difficult Customers</h3>
<div class="customer-types">
<div class="type">
<h4>The Angry Customer</h4>
<p><strong>Behavior:</strong> Raised voice, accusations, threats</p>
<p><strong>Strategy:</strong></p>
<ul>
<li>Stay calm - don't match their energy</li>
<li>Let them vent without interruption</li>
<li>Use their name to personalize the interaction</li>
<li>Focus on what you CAN do, not what you can't</li>
</ul>
</div>

<div class="type">
<h4>The Demanding Customer</h4>
<p><strong>Behavior:</strong> Unrealistic expectations, impatience, persistent pressure</p>
<p><strong>Strategy:</strong></p>
<ul>
<li>Set clear boundaries professionally</li>
<li>Explain constraints without being defensive</li>
<li>Offer alternatives where possible</li>
<li>Document commitments clearly</li>
</ul>
</div>

<div class="type">
<h4>The Know-It-All</h4>
<p><strong>Behavior:</strong> Challenges your expertise, contradicts recommendations</p>
<p><strong>Strategy:</strong></p>
<ul>
<li>Acknowledge their knowledge</li>
<li>Use data and evidence to support your points</li>
<li>Ask questions to understand their perspective</li>
<li>Avoid power struggles - focus on outcomes</li>
</ul>
</div>

<div class="type">
<h4>The Indecisive Customer</h4>
<p><strong>Behavior:</strong> Can't make decisions, constant changes, delays</p>
<p><strong>Strategy:</strong></p>
<ul>
<li>Help structure the decision process</li>
<li>Provide clear comparisons</li>
<li>Gently create urgency with deadlines</li>
<li>Confirm decisions in writing immediately</li>
</ul>
</div>
</div>

<h3>De-escalation Techniques</h3>
<div class="techniques-list">
<ul>
<li><strong>Lower your voice:</strong> Speaking quietly often causes others to do the same</li>
<li><strong>Use empathy statements:</strong> "I understand this is frustrating"</li>
<li><strong>Find common ground:</strong> "We both want to resolve this quickly"</li>
<li><strong>Take responsibility:</strong> "Let me take ownership of getting this sorted"</li>
<li><strong>Propose action:</strong> "Here's what I'm going to do right now"</li>
</ul>
</div>

<h3>When to Step Back</h3>
<p>It's appropriate to involve others when:</p>
<ul>
<li>The customer becomes abusive or threatening</li>
<li>You feel your ability to remain professional is compromised</li>
<li>The situation requires authority you don't have</li>
<li>You've tried multiple approaches without success</li>
</ul>

<div class="highlight-box">
<h4>Remember</h4>
<p>You can be professional without accepting abuse. Flowitec supports employees in maintaining respectful interactions.</p>
</div>
</div>"""
                },
                {
                    "title": "Building Resilience for Long-Term Success",
                    "content": """<div class="lesson-content">
<h2>Developing Career Resilience</h2>
<p>Resilience is the ability to bounce back from setbacks and maintain performance under pressure. It's a skill that can be developed and strengthened over time.</p>

<h3>The Pillars of Professional Resilience</h3>
<div class="pillars-grid">
<div class="pillar-card">
<h4>Self-Awareness</h4>
<p>Know your strengths, weaknesses, stress triggers, and energy patterns.</p>
<ul>
<li>Regular self-reflection</li>
<li>Seek feedback from trusted colleagues</li>
<li>Track what energizes vs. drains you</li>
</ul>
</div>

<div class="pillar-card">
<h4>Optimism</h4>
<p>Maintain a positive but realistic outlook.</p>
<ul>
<li>Focus on what you can control</li>
<li>View setbacks as temporary and specific</li>
<li>Celebrate wins, even small ones</li>
</ul>
</div>

<div class="pillar-card">
<h4>Purpose</h4>
<p>Connect your work to meaningful goals.</p>
<ul>
<li>Remember why you chose this career</li>
<li>See how your work helps customers</li>
<li>Set personal growth objectives</li>
</ul>
</div>

<div class="pillar-card">
<h4>Support Network</h4>
<p>Build relationships that sustain you.</p>
<ul>
<li>Colleagues who understand the role</li>
<li>Mentor or coach for guidance</li>
<li>Personal relationships outside work</li>
</ul>
</div>
</div>

<h3>Learning from Setbacks</h3>
<p>Every lost deal or difficult situation offers lessons:</p>
<div class="reflection-questions">
<ul>
<li>What can I learn from this experience?</li>
<li>What would I do differently next time?</li>
<li>What was outside my control?</li>
<li>What went well despite the outcome?</li>
<li>Who can I ask for perspective?</li>
</ul>
</div>

<h3>Career Sustainability Practices</h3>
<ul>
<li><strong>Continuous Learning:</strong> Stay engaged through skill development</li>
<li><strong>Variety:</strong> Seek diverse projects and customer types</li>
<li><strong>Recognition:</strong> Acknowledge your own achievements</li>
<li><strong>Boundaries:</strong> Protect time for rest and recovery</li>
<li><strong>Future Focus:</strong> Keep career goals in view</li>
</ul>

<h3>Final Thoughts: The Resilient Sales Engineer</h3>
<div class="conclusion-box">
<p>A career in sales engineering at Flowitec offers tremendous opportunity for those who develop both technical skills and personal resilience.</p>
<p>Remember:</p>
<ul>
<li>Stress is manageable with the right tools and mindset</li>
<li>Difficult customers are opportunities to demonstrate value</li>
<li>Your well-being supports your performance</li>
<li>Flowitec is invested in your success</li>
</ul>
<p>By completing this course, you've taken an important step toward becoming an exceptional customer service professional who can thrive in this demanding but rewarding field.</p>
</div>
</div>"""
                }
            ]
        }
    ]
}

# Course 2: B2B Customer Success Management for Industrial Equipment
COURSE_2 = {
    "title": "B2B Customer Success Management",
    "description": "Learn how to manage long-term customer relationships in the B2B industrial equipment sector. Master strategies for customer retention, account growth, and building partnerships that drive mutual success in the pumps and valves industry.",
    "thumbnail": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=225&fit=crop",
    "category": "SALES (ENGINEER)",
    "duration_hours": 12,
    "code": "SE-CSM-002",
    "modules": [
        {
            "title": "Module 1: Introduction to B2B Customer Success",
            "lessons": [
                {
                    "title": "What is Customer Success in Industrial B2B?",
                    "content": """<div class="lesson-content">
<h2>Understanding Customer Success in Industrial Markets</h2>
<p>Customer Success is a proactive approach to ensuring customers achieve their desired outcomes using your products and services. In the industrial equipment sector, this means helping customers maximize the value they receive from their Flowitec pumps, valves, and fluid handling systems.</p>

<h3>Customer Success vs. Customer Service</h3>
<div class="comparison-box">
<div class="comparison-item">
<h4>Customer Service</h4>
<ul>
<li><strong>Reactive:</strong> Responds when customers reach out</li>
<li><strong>Problem-focused:</strong> Addresses issues and complaints</li>
<li><strong>Transactional:</strong> Often one-time interactions</li>
<li><strong>Metric:</strong> Resolution time, satisfaction scores</li>
</ul>
</div>

<div class="comparison-item">
<h4>Customer Success</h4>
<ul>
<li><strong>Proactive:</strong> Reaches out before issues arise</li>
<li><strong>Outcome-focused:</strong> Ensures customers achieve goals</li>
<li><strong>Relationship:</strong> Ongoing partnership</li>
<li><strong>Metric:</strong> Customer retention, growth, lifetime value</li>
</ul>
</div>
</div>

<h3>Why Customer Success Matters for Flowitec</h3>
<div class="stats-section">
<div class="stat">
<span class="number">5x</span>
<p>Cost to acquire new customer vs. retaining existing one</p>
</div>
<div class="stat">
<span class="number">60-70%</span>
<p>Probability of selling to existing customer (vs. 5-20% for new)</p>
</div>
<div class="stat">
<span class="number">65%</span>
<p>Of company revenue comes from repeat customers</p>
</div>
</div>

<h3>The Flowitec Customer Success Mission</h3>
<div class="highlight-box">
<p>At Flowitec, Customer Success means ensuring every customer:</p>
<ul>
<li>Gets the right equipment for their application</li>
<li>Achieves maximum uptime and reliability</li>
<li>Optimizes their total cost of ownership</li>
<li>Has access to expert support when needed</li>
<li>Views Flowitec as a strategic partner, not just a supplier</li>
</ul>
</div>

<div class="info-box">
<h4>Key Takeaway</h4>
<p>Customer Success is about moving from "What can I sell?" to "How can I help my customer succeed?" This mindset shift transforms transactional relationships into strategic partnerships.</p>
</div>
</div>"""
                },
                {
                    "title": "The Customer Success Manager Role",
                    "content": """<div class="lesson-content">
<h2>Your Role as a Customer Success Professional</h2>
<p>At Flowitec, every Sales Engineer incorporates Customer Success principles into their work. Understanding this role helps you deliver exceptional value to your accounts.</p>

<h3>Core Responsibilities</h3>
<div class="responsibilities-grid">
<div class="resp-card">
<h4>Onboarding New Customers</h4>
<p>Ensure new customers are set up for success from day one:</p>
<ul>
<li>Verify correct installation of equipment</li>
<li>Provide operational training if needed</li>
<li>Establish communication channels</li>
<li>Set expectations for ongoing support</li>
</ul>
</div>

<div class="resp-card">
<h4>Account Health Monitoring</h4>
<p>Proactively track customer satisfaction and engagement:</p>
<ul>
<li>Regular check-in calls (quarterly minimum)</li>
<li>Monitor equipment performance</li>
<li>Track order patterns and changes</li>
<li>Identify potential issues early</li>
</ul>
</div>

<div class="resp-card">
<h4>Value Realization</h4>
<p>Help customers get maximum value from their investment:</p>
<ul>
<li>Share best practices and optimization tips</li>
<li>Provide performance data and benchmarks</li>
<li>Recommend upgrades when beneficial</li>
<li>Calculate and communicate ROI</li>
</ul>
</div>

<div class="resp-card">
<h4>Growth & Expansion</h4>
<p>Identify opportunities to expand the relationship:</p>
<ul>
<li>Understand customer's full operation</li>
<li>Propose solutions for additional needs</li>
<li>Facilitate introductions to other departments</li>
<li>Support project planning</li>
</ul>
</div>
</div>

<h3>Key Success Metrics</h3>
<table class="metrics-table">
<tr><th>Metric</th><th>Definition</th><th>Target</th></tr>
<tr><td>Customer Retention Rate</td><td>% of customers who continue buying</td><td>>90%</td></tr>
<tr><td>Net Promoter Score (NPS)</td><td>Would customer recommend Flowitec?</td><td>>50</td></tr>
<tr><td>Customer Lifetime Value</td><td>Total revenue from customer over time</td><td>Growing year over year</td></tr>
<tr><td>Expansion Revenue</td><td>Additional revenue from existing customers</td><td>20%+ of total sales</td></tr>
</table>

<div class="info-box">
<h4>Remember</h4>
<p>Your success is measured by your customers' success. When they thrive, so does your career at Flowitec.</p>
</div>
</div>"""
                },
                {
                    "title": "Understanding Your Customer's Business",
                    "content": """<div class="lesson-content">
<h2>Deep Customer Understanding</h2>
<p>To help customers succeed, you must understand their business as deeply as they do - perhaps even more so when it comes to fluid handling systems.</p>

<h3>The Customer Knowledge Framework</h3>
<div class="framework-layers">
<div class="layer">
<h4>Layer 1: Company Overview</h4>
<ul>
<li>Industry and market position</li>
<li>Company size and structure</li>
<li>Key products or services</li>
<li>Major customers they serve</li>
<li>Growth trajectory and plans</li>
</ul>
</div>

<div class="layer">
<h4>Layer 2: Operations</h4>
<ul>
<li>Production processes and requirements</li>
<li>Critical equipment and systems</li>
<li>Maintenance practices and schedules</li>
<li>Operational challenges and pain points</li>
<li>Quality and safety standards</li>
</ul>
</div>

<div class="layer">
<h4>Layer 3: Decision Making</h4>
<ul>
<li>Key decision makers and influencers</li>
<li>Procurement processes</li>
<li>Budget cycles and approval thresholds</li>
<li>Vendor evaluation criteria</li>
<li>Current supplier relationships</li>
</ul>
</div>

<div class="layer">
<h4>Layer 4: Goals and Challenges</h4>
<ul>
<li>Business objectives (efficiency, growth, cost reduction)</li>
<li>Technical challenges</li>
<li>Competitive pressures</li>
<li>Regulatory requirements</li>
<li>Future plans and projects</li>
</ul>
</div>
</div>

<h3>Questions to Ask</h3>
<div class="questions-section">
<h4>Strategic Questions</h4>
<ul>
<li>"What are your top priorities for this year?"</li>
<li>"Where do you see the biggest opportunities for improvement?"</li>
<li>"What challenges keep you up at night?"</li>
</ul>

<h4>Operational Questions</h4>
<ul>
<li>"How critical is this equipment to your operation?"</li>
<li>"What would happen if this system failed?"</li>
<li>"How much downtime can you tolerate?"</li>
</ul>

<h4>Relationship Questions</h4>
<ul>
<li>"What do you value most in a supplier relationship?"</li>
<li>"What would make working with us easier?"</li>
<li>"How can we be more valuable to you?"</li>
</ul>
</div>

<div class="highlight-box">
<h4>Flowitec Approach</h4>
<p>We don't just sell pumps and valves - we become experts in our customers' operations. This expertise allows us to add value beyond just supplying equipment.</p>
</div>
</div>"""
                },
                {
                    "title": "Building Your Customer Success Plan",
                    "content": """<div class="lesson-content">
<h2>Creating Customer Success Plans</h2>
<p>A Customer Success Plan is a roadmap for helping each key account achieve their goals while growing the Flowitec relationship.</p>

<h3>Elements of a Customer Success Plan</h3>
<div class="plan-sections">
<div class="section">
<h4>1. Customer Profile</h4>
<table>
<tr><td>Company</td><td>[Customer Name]</td></tr>
<tr><td>Industry</td><td>[e.g., Mining, Food & Beverage, Water Treatment]</td></tr>
<tr><td>Key Contacts</td><td>[Names, roles, contact details]</td></tr>
<tr><td>Flowitec Relationship Since</td><td>[Date]</td></tr>
<tr><td>Annual Spend</td><td>[GHS Value]</td></tr>
</table>
</div>

<div class="section">
<h4>2. Current State Assessment</h4>
<ul>
<li><strong>Installed Flowitec Equipment:</strong> [List of pumps, valves, etc.]</li>
<li><strong>Performance Status:</strong> [Any issues, maintenance needs]</li>
<li><strong>Customer Satisfaction:</strong> [Current NPS or feedback]</li>
<li><strong>Relationship Health:</strong> [Strong/Moderate/At Risk]</li>
</ul>
</div>

<div class="section">
<h4>3. Customer Goals</h4>
<p>What is the customer trying to achieve?</p>
<ul>
<li>Short-term (0-6 months): [e.g., Reduce pump maintenance costs]</li>
<li>Medium-term (6-18 months): [e.g., Expand production capacity]</li>
<li>Long-term (18+ months): [e.g., Upgrade entire water system]</li>
</ul>
</div>

<div class="section">
<h4>4. How Flowitec Helps</h4>
<p>Specific actions to support customer goals:</p>
<ul>
<li>Technical support and optimization</li>
<li>Product upgrades and recommendations</li>
<li>Training and knowledge sharing</li>
<li>Preventive maintenance advice</li>
</ul>
</div>

<div class="section">
<h4>5. Success Milestones</h4>
<table>
<tr><th>Milestone</th><th>Timeline</th><th>Owner</th></tr>
<tr><td>Quarterly business review</td><td>Every 3 months</td><td>Sales Engineer</td></tr>
<tr><td>Equipment performance check</td><td>Bi-annually</td><td>Service Team</td></tr>
<tr><td>New project discussion</td><td>As identified</td><td>Sales Engineer</td></tr>
</table>
</div>

<div class="section">
<h4>6. Risk Mitigation</h4>
<p>Potential threats to the relationship:</p>
<ul>
<li>Competitor activity</li>
<li>Budget constraints</li>
<li>Personnel changes</li>
<li>Equipment issues</li>
</ul>
</div>
</div>

<div class="info-box">
<h4>Best Practice</h4>
<p>Develop formal Customer Success Plans for your top 10-20 accounts. Review and update them quarterly.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 2: Customer Onboarding Excellence",
            "lessons": [
                {
                    "title": "The Critical First 90 Days",
                    "content": """<div class="lesson-content">
<h2>Setting Customers Up for Success</h2>
<p>The first 90 days after a customer's initial purchase are the most critical period for establishing a successful long-term relationship. This is when expectations are set and trust is built or broken.</p>

<h3>Why Onboarding Matters</h3>
<div class="onboarding-stats">
<div class="stat-card">
<p>Customers who have a positive onboarding experience are</p>
<span class="big-number">3x</span>
<p>more likely to remain loyal for 3+ years</p>
</div>
</div>

<h3>The Flowitec 90-Day Onboarding Framework</h3>
<div class="timeline">
<div class="phase">
<h4>Days 1-7: Welcome & Setup</h4>
<ul>
<li>Welcome call to confirm order and set expectations</li>
<li>Provide order tracking and delivery schedule</li>
<li>Share installation guides and requirements</li>
<li>Introduce key Flowitec contacts</li>
</ul>
</div>

<div class="phase">
<h4>Days 8-30: Delivery & Installation</h4>
<ul>
<li>Coordinate delivery logistics</li>
<li>Verify installation is correct</li>
<li>Provide startup support and commissioning assistance</li>
<li>Address any initial questions or concerns</li>
</ul>
</div>

<div class="phase">
<h4>Days 31-60: Early Operation</h4>
<ul>
<li>Check-in call to verify equipment performance</li>
<li>Gather feedback on the purchase experience</li>
<li>Address any issues promptly</li>
<li>Share relevant maintenance tips</li>
</ul>
</div>

<div class="phase">
<h4>Days 61-90: Relationship Establishment</h4>
<ul>
<li>Schedule first quarterly business review</li>
<li>Discuss future needs and projects</li>
<li>Confirm customer satisfaction</li>
<li>Document account in CRM</li>
</ul>
</div>
</div>

<h3>Onboarding Checklist</h3>
<div class="checklist">
<ul>
<li>☐ Welcome call completed</li>
<li>☐ Delivery confirmed on time</li>
<li>☐ Installation verified correct</li>
<li>☐ Startup support provided</li>
<li>☐ 30-day check-in completed</li>
<li>☐ Any issues resolved</li>
<li>☐ 60-day feedback gathered</li>
<li>☐ First quarterly review scheduled</li>
<li>☐ Customer success plan created</li>
</ul>
</div>

<div class="highlight-box">
<h4>Key Principle</h4>
<p>Over-communicate during onboarding. Customers should never wonder what's happening with their order or feel abandoned after the sale.</p>
</div>
</div>"""
                },
                {
                    "title": "Technical Onboarding Best Practices",
                    "content": """<div class="lesson-content">
<h2>Ensuring Technical Success from Day One</h2>
<p>For industrial equipment like pumps and valves, technical onboarding is crucial. Proper installation and startup are essential for long-term performance.</p>

<h3>Pre-Delivery Preparation</h3>
<div class="prep-section">
<h4>What to Verify with the Customer</h4>
<ul>
<li><strong>Site Readiness:</strong> Is the installation site prepared (foundations, piping, electrical)?</li>
<li><strong>Receiving Capability:</strong> Do they have equipment to unload (forklift, crane)?</li>
<li><strong>Installation Resources:</strong> Who will install - their team or contractors?</li>
<li><strong>Technical Documentation Needed:</strong> What manuals or drawings do they need?</li>
</ul>

<h4>What to Provide</h4>
<ul>
<li>Installation and operation manual</li>
<li>Technical drawings and dimensions</li>
<li>Electrical connection requirements</li>
<li>Spare parts list and recommendations</li>
<li>Warranty registration information</li>
</ul>
</div>

<h3>Installation Support</h3>
<div class="install-guide">
<h4>Common Installation Issues to Prevent</h4>
<table class="issues-table">
<tr><th>Issue</th><th>Cause</th><th>Prevention</th></tr>
<tr><td>Misalignment</td><td>Improper coupling installation</td><td>Provide alignment procedure, offer site support</td></tr>
<tr><td>Cavitation damage</td><td>Insufficient NPSH</td><td>Verify suction conditions before installation</td></tr>
<tr><td>Pipe strain</td><td>Improper pipe support</td><td>Include pipe support requirements in documentation</td></tr>
<tr><td>Electrical issues</td><td>Incorrect wiring</td><td>Provide clear wiring diagrams</td></tr>
</table>
</div>

<h3>Startup Commissioning</h3>
<div class="commissioning-steps">
<h4>Pre-Startup Checklist (Pumps)</h4>
<ol>
<li>Verify rotation direction (bump start motor)</li>
<li>Check alignment within specifications</li>
<li>Confirm suction and discharge valves are in correct position</li>
<li>Prime pump if not self-priming</li>
<li>Verify motor overload settings</li>
</ol>

<h4>Startup Procedure</h4>
<ol>
<li>Start pump with discharge valve slightly open</li>
<li>Gradually open discharge valve to operating position</li>
<li>Verify flow and pressure match specifications</li>
<li>Check for unusual noise or vibration</li>
<li>Monitor motor current</li>
</ol>
</div>

<div class="info-box">
<h4>Value-Add Service</h4>
<p>Offering startup support - even remotely by phone - differentiates Flowitec from competitors who simply ship and forget.</p>
</div>
</div>"""
                },
                {
                    "title": "Managing Customer Expectations",
                    "content": """<div class="lesson-content">
<h2>Setting and Managing Expectations</h2>
<p>Customer satisfaction is the gap between expectations and reality. By managing expectations proactively, you ensure customers are satisfied even when things aren't perfect.</p>

<h3>The Expectation Equation</h3>
<div class="equation-box">
<p><strong>Customer Satisfaction = Perceived Performance - Expectations</strong></p>
<ul>
<li>If Performance > Expectations → Delighted customer</li>
<li>If Performance = Expectations → Satisfied customer</li>
<li>If Performance < Expectations → Disappointed customer</li>
</ul>
</div>

<h3>Key Areas to Set Expectations</h3>
<div class="expectation-areas">
<div class="area">
<h4>Delivery Timelines</h4>
<p><strong>Best Practice:</strong> Quote realistic lead times, then try to beat them.</p>
<ul>
<li>Always add buffer for unexpected delays</li>
<li>Communicate proactively if delays occur</li>
<li>Never promise what you can't deliver</li>
</ul>
</div>

<div class="area">
<h4>Product Performance</h4>
<p><strong>Best Practice:</strong> Be accurate about capabilities and limitations.</p>
<ul>
<li>Share performance data from similar applications</li>
<li>Discuss operating range (not just optimal point)</li>
<li>Explain what conditions are required for best performance</li>
</ul>
</div>

<div class="area">
<h4>Support Availability</h4>
<p><strong>Best Practice:</strong> Clarify what support is included and how to access it.</p>
<ul>
<li>Define standard response times</li>
<li>Explain escalation process for urgent issues</li>
<li>Provide multiple contact channels</li>
</ul>
</div>

<div class="area">
<h4>Warranty Terms</h4>
<p><strong>Best Practice:</strong> Review warranty coverage clearly.</p>
<ul>
<li>What's covered and what's not</li>
<li>Duration and conditions</li>
<li>Claim process</li>
</ul>
</div>
</div>

<h3>Communication Best Practices</h3>
<div class="comm-tips">
<h4>Under-Promise, Over-Deliver</h4>
<p>Build in margin to exceed expectations:</p>
<ul>
<li>"Delivery in 4-6 weeks" (actually 3-4 weeks)</li>
<li>"Response within 24 hours" (actually same day)</li>
<li>"Expected efficiency 75%" (actually achieves 78%)</li>
</ul>

<h4>Proactive Updates</h4>
<p>Don't wait for customers to ask:</p>
<ul>
<li>Send order status updates automatically</li>
<li>Alert immediately to any delays or issues</li>
<li>Follow up after delivery without being asked</li>
</ul>
</div>

<div class="highlight-box">
<h4>Golden Rule</h4>
<p>It's better to set lower expectations and exceed them than to over-promise and disappoint. Trust is built through consistent delivery on promises.</p>
</div>
</div>"""
                },
                {
                    "title": "Building Long-Term Relationships",
                    "content": """<div class="lesson-content">
<h2>From Transaction to Partnership</h2>
<p>The goal of customer success is to transform one-time buyers into long-term partners. This requires deliberate relationship building beyond the immediate transaction.</p>

<h3>The Relationship Ladder</h3>
<div class="ladder">
<div class="rung rung-5">
<h4>Level 5: Strategic Partner</h4>
<p>Customer involves you in long-term planning, provides referrals, co-develops solutions</p>
</div>
<div class="rung rung-4">
<h4>Level 4: Trusted Advisor</h4>
<p>Customer seeks your expertise for decisions beyond products</p>
</div>
<div class="rung rung-3">
<h4>Level 3: Preferred Supplier</h4>
<p>Customer consistently chooses you for repeat purchases</p>
</div>
<div class="rung rung-2">
<h4>Level 2: Approved Vendor</h4>
<p>Customer considers you for quotes alongside competitors</p>
</div>
<div class="rung rung-1">
<h4>Level 1: Known Supplier</h4>
<p>Customer is aware of Flowitec but hasn't purchased</p>
</div>
</div>

<h3>Relationship Building Activities</h3>
<div class="activities">
<div class="activity">
<h4>Regular Business Reviews</h4>
<ul>
<li>Quarterly meetings to review performance</li>
<li>Discuss upcoming projects and needs</li>
<li>Share industry insights and trends</li>
<li>Gather feedback for improvement</li>
</ul>
</div>

<div class="activity">
<h4>Value-Added Services</h4>
<ul>
<li>Technical training for customer's team</li>
<li>Preventive maintenance recommendations</li>
<li>Energy efficiency audits</li>
<li>System optimization reviews</li>
</ul>
</div>

<div class="activity">
<h4>Proactive Communication</h4>
<ul>
<li>Share relevant industry news</li>
<li>Notify about new products or technologies</li>
<li>Invite to Flowitec events and training</li>
<li>Remember important dates (anniversaries, birthdays)</li>
</ul>
</div>

<div class="activity">
<h4>Personal Touch</h4>
<ul>
<li>Know names of key contacts' assistants</li>
<li>Remember personal details (hobbies, family)</li>
<li>Send handwritten notes for milestones</li>
<li>Visit in person, not just phone/email</li>
</ul>
</div>
</div>

<h3>Key Account Identification</h3>
<p>Not all customers require the same level of attention. Prioritize based on:</p>
<ul>
<li><strong>Revenue:</strong> Current and potential spend</li>
<li><strong>Strategic fit:</strong> Alignment with Flowitec's target markets</li>
<li><strong>Growth potential:</strong> Expanding company or market</li>
<li><strong>Reference value:</strong> Influential in industry</li>
<li><strong>Relationship quality:</strong> Willingness to partner</li>
</ul>

<div class="info-box">
<h4>Goal</h4>
<p>Aim to have at least 10 accounts at Level 4 (Trusted Advisor) or above. These relationships provide stability and growth for your business.</p>
</div>
</div>"""
                }
            ]
        },
        {
            "title": "Module 3: Proactive Customer Support",
            "lessons": [
                {
                    "title": "Moving from Reactive to Proactive Support",
                    "content": """<div class="lesson-content">
<h2>The Power of Proactive Support</h2>
<p>Proactive support means reaching out to customers before they have problems, not waiting for them to call with complaints. This approach dramatically improves customer satisfaction and retention.</p>

<h3>Reactive vs. Proactive Support</h3>
<div class="comparison">
<div class="column reactive">
<h4>Reactive (Traditional)</h4>
<ul>
<li>Wait for customer to report issue</li>
<li>Respond to complaints</li>
<li>Fix problems after they occur</li>
<li>Customer experiences downtime</li>
<li>Relationship is transactional</li>
</ul>
</div>

<div class="column proactive">
<h4>Proactive (Customer Success)</h4>
<ul>
<li>Anticipate and prevent issues</li>
<li>Reach out before problems occur</li>
<li>Address potential concerns early</li>
<li>Minimize customer downtime</li>
<li>Relationship is partnership</li>
</ul>
</div>
</div>

<h3>Proactive Support Activities</h3>
<div class="activities-list">
<div class="activity-card">
<h4>Scheduled Check-Ins</h4>
<p>Regular contact to assess satisfaction and needs:</p>
<ul>
<li>30-day post-purchase call</li>
<li>Quarterly business reviews</li>
<li>Annual account planning</li>
</ul>
</div>

<div class="activity-card">
<h4>Preventive Maintenance Reminders</h4>
<p>Help customers maintain equipment properly:</p>
<ul>
<li>Service interval notifications</li>
<li>Spare parts recommendations</li>
<li>Best practice guidelines</li>
</ul>
</div>

<div class="activity-card">
<h4>Performance Monitoring</h4>
<p>Track equipment performance proactively:</p>
<ul>
<li>Warranty claim tracking</li>
<li>Common issue alerts</li>
<li>Operating condition verification</li>
</ul>
</div>

<div class="activity-card">
<h4>Industry Updates</h4>
<p>Share relevant information:</p>
<ul>
<li>New product announcements</li>
<li>Technical bulletins</li>
<li>Regulatory changes affecting them</li>
</ul>
</div>
</div>

<h3>Creating a Proactive Support Calendar</h3>
<table class="support-calendar">
<tr><th>Timeframe</th><th>Activity</th><th>Purpose</th></tr>
<tr><td>Weekly</td><td>Review open orders and deliveries</td><td>Anticipate delivery issues</td></tr>
<tr><td>Monthly</td><td>Contact accounts with no recent activity</td><td>Maintain relationship</td></tr>
<tr><td>Quarterly</td><td>Business review with key accounts</td><td>Deepen partnership</td></tr>
<tr><td>Annually</td><td>Equipment review and planning</td><td>Identify upgrade opportunities</td></tr>
</table>

<div class="highlight-box">
<h4>Flowitec Differentiator</h4>
<p>Most suppliers wait for customers to call. Flowitec Sales Engineers who proactively reach out demonstrate that we genuinely care about customer success.</p>
</div>
</div>"""
                },
                {
                    "title": "Customer Health Scoring",
                    "content": """<div class="lesson-content">
<h2>Measuring Customer Health</h2>
<p>Customer health scoring helps you identify which accounts need attention before problems escalate. It's an early warning system for relationship issues.</p>

<h3>The Customer Health Score Model</h3>
<div class="health-model">
<p>Customer health is measured across multiple dimensions:</p>

<div class="dimension">
<h4>1. Engagement (30% weight)</h4>
<ul>
<li>Frequency of communication</li>
<li>Response to outreach</li>
<li>Participation in reviews/meetings</li>
<li>Portal/website usage</li>
</ul>
</div>

<div class="dimension">
<h4>2. Product Usage/Performance (25% weight)</h4>
<ul>
<li>Equipment operating as expected</li>
<li>Service calls or complaints</li>
<li>Warranty claims</li>
<li>Maintenance compliance</li>
</ul>
</div>

<div class="dimension">
<h4>3. Growth Signals (25% weight)</h4>
<ul>
<li>Repeat purchase frequency</li>
<li>Order value trend (increasing/decreasing)</li>
<li>New project discussions</li>
<li>Expansion to new locations/applications</li>
</ul>
</div>

<div class="dimension">
<h4>4. Satisfaction Indicators (20% weight)</h4>
<ul>
<li>Direct feedback and NPS</li>
<li>Complaint resolution satisfaction</li>
<li>Referrals provided</li>
<li>Public testimonials/reviews</li>
</ul>
</div>
</div>

<h3>Health Score Categories</h3>
<div class="score-categories">
<div class="category green">
<h4>Healthy (Score 75-100)</h4>
<p>Strong relationship, engaged customer, growth opportunity</p>
<p><strong>Action:</strong> Maintain relationship, explore expansion</p>
</div>

<div class="category yellow">
<h4>At Risk (Score 50-74)</h4>
<p>Some warning signs, needs attention</p>
<p><strong>Action:</strong> Schedule review, address concerns, increase contact</p>
</div>

<div class="category red">
<h4>Critical (Score 0-49)</h4>
<p>Serious issues, risk of losing customer</p>
<p><strong>Action:</strong> Urgent intervention, escalate if needed, recovery plan</p>
</div>
</div>

<h3>Warning Signs to Watch For</h3>
<div class="warning-signs">
<ul>
<li>🚩 Decreased order frequency or value</li>
<li>🚩 Not responding to calls/emails</li>
<li>🚩 Multiple complaints in short period</li>
<li>🚩 Requests for competitor information</li>
<li>🚩 New contact person (champion may have left)</li>
<li>🚩 Budget cuts or organizational changes</li>
<li>🚩 Delayed payments</li>
</ul>
</div>

<div class="info-box">
<h4>Best Practice</h4>
<p>Review your customer health scores monthly. Address any account dropping from green to yellow immediately, before it becomes critical.</p>
</div>
</div>"""
                },
                {
                    "title": "Customer Success Metrics and KPIs",
                    "content": """<div class="lesson-content">
<h2>Measuring Customer Success</h2>
<p>What gets measured gets managed. Understanding and tracking key metrics helps you demonstrate value and continuously improve your customer success efforts.</p>

<h3>Essential Customer Success Metrics</h3>
<div class="metrics-section">
<div class="metric-card">
<h4>Customer Retention Rate</h4>
<p><strong>Definition:</strong> Percentage of customers who continue purchasing over a period</p>
<p><strong>Formula:</strong> (Customers at End - New Customers) / Customers at Start × 100</p>
<p><strong>Target:</strong> >90% annually</p>
<p><strong>Why It Matters:</strong> Direct measure of customer loyalty and relationship health</p>
</div>

<div class="metric-card">
<h4>Net Promoter Score (NPS)</h4>
<p><strong>Definition:</strong> Likelihood of customer to recommend Flowitec</p>
<p><strong>Question:</strong> "On a scale of 0-10, how likely are you to recommend Flowitec?"</p>
<p><strong>Formula:</strong> % Promoters (9-10) - % Detractors (0-6)</p>
<p><strong>Target:</strong> >50</p>
</div>

<div class="metric-card">
<h4>Customer Lifetime Value (CLV)</h4>
<p><strong>Definition:</strong> Total revenue expected from a customer over the relationship</p>
<p><strong>Formula:</strong> Average Order Value × Purchase Frequency × Customer Lifespan</p>
<p><strong>Why It Matters:</strong> Guides investment in customer success activities</p>
</div>

<div class="metric-card">
<h4>Churn Rate</h4>
<p><strong>Definition:</strong> Percentage of customers lost over a period</p>
<p><strong>Formula:</strong> Lost Customers / Total Customers × 100</p>
<p><strong>Target:</strong> <10% annually</p>
<p><strong>Action:</strong> Analyze every lost customer to prevent future churn</p>
</div>

<div class="metric-card">
<h4>Expansion Revenue</h4>
<p><strong>Definition:</strong> Additional revenue from existing customers (upsell, cross-sell)</p>
<p><strong>Target:</strong> 20%+ of total revenue from existing customers</p>
<p><strong>Why It Matters:</strong> Shows relationship deepening and value delivery</p>
</div>
</div>

<h3>Tracking and Reporting</h3>
<div class="tracking-guide">
<h4>Monthly Review</h4>
<ul>
<li>Customer health score changes</li>
<li>New at-risk accounts</li>
<li>Complaints and resolutions</li>
<li>Order trends by key account</li>
</ul>

<h4>Quarterly Review</h4>
<ul>
<li>NPS survey results</li>
<li>Retention rate calculation</li>
<li>Customer success plan progress</li>
<li>Expansion revenue tracking</li>
</ul>

<h4>Annual Review</h4>
<ul>
<li>CLV analysis</li>
<li>Churn analysis and root causes</li>
<li>Customer segmentation review</li>
<li>Strategy and goal setting for next year</li>
</ul>
</div>

<div class="highlight-box">
<h4>Actionable Insight</h4>
<p>Don't just track metrics - act on them. Each metric should trigger specific actions when it moves outside target range.</p>
</div>
</div>"""
                },
                {
                    "title": "Conducting Effective Business Reviews",
                    "content": """<div class="lesson-content">
<h2>Quarterly Business Reviews</h2>
<p>Business reviews are structured meetings with key accounts to discuss performance, address concerns, and plan for the future. They demonstrate commitment and uncover opportunities.</p>

<h3>QBR Agenda Template</h3>
<div class="agenda">
<div class="agenda-item">
<span class="time">5 min</span>
<h4>1. Introduction & Objectives</h4>
<p>Set the stage for a productive discussion</p>
</div>

<div class="agenda-item">
<span class="time">15 min</span>
<h4>2. Business Update</h4>
<p>Customer shares updates on their business, challenges, and priorities</p>
</div>

<div class="agenda-item">
<span class="time">15 min</span>
<h4>3. Performance Review</h4>
<p>Review Flowitec's performance: deliveries, support, equipment performance</p>
</div>

<div class="agenda-item">
<span class="time">10 min</span>
<h4>4. Issue Resolution</h4>
<p>Address any outstanding concerns or problems</p>
</div>

<div class="agenda-item">
<span class="time">10 min</span>
<h4>5. Value Delivered</h4>
<p>Highlight the value Flowitec has provided (cost savings, efficiency, uptime)</p>
</div>

<div class="agenda-item">
<span class="time">15 min</span>
<h4>6. Future Planning</h4>
<p>Discuss upcoming projects, needs, and opportunities</p>
</div>

<div class="agenda-item">
<span class="time">5 min</span>
<h4>7. Action Items & Close</h4>
<p>Summarize agreements and next steps</p>
</div>
</div>

<h3>Preparation Checklist</h3>
<div class="checklist">
<ul>
<li>☐ Review account history (orders, complaints, interactions)</li>
<li>☐ Calculate value delivered (savings, uptime, etc.)</li>
<li>☐ Identify 2-3 expansion opportunities</li>
<li>☐ Prepare relevant case studies or success stories</li>
<li>☐ Create presentation with data visualizations</li>
<li>☐ Confirm attendees and logistics</li>
</ul>
</div>

<h3>Best Practices for QBRs</h3>
<div class="best-practices">
<ul>
<li><strong>Be prepared:</strong> Have data and insights ready, not just a blank agenda</li>
<li><strong>Listen more than talk:</strong> This is about them, not us</li>
<li><strong>Bring value:</strong> Share insights they can't get elsewhere</li>
<li><strong>Be honest:</strong> If there were issues, acknowledge and address them</li>
<li><strong>Document everything:</strong> Send summary within 24 hours</li>
<li><strong>Follow through:</strong> Action items must be completed</li>
</ul>
</div>

<h3>Sample Value Statement</h3>
<div class="example-box">
<p>"Over the past quarter, the three Flowitec CP-200 pumps in your cooling system have operated at 99.2% uptime. Based on your cost of downtime of GHS 5,000 per hour, this represents approximately GHS 35,000 in avoided downtime costs compared to industry average pump reliability of 96%."</p>
</div>

<div class="info-box">
<h4>Remember</h4>
<p>QBRs are not sales pitches - they're partnership discussions. The goal is to understand, align, and strengthen the relationship.</p>
</div>
</div>"""
                }
            ]
        }
    ]
}

# Additional courses will follow the same comprehensive structure...
# For brevity in this seed file, we'll include the structure for the remaining 15 courses

def get_all_courses():
    """Return all 17 SALES courses"""
    return [
        COURSE_1,
        COURSE_2,
        # Courses 3-17 will be defined with full content
        {
            "title": "Customer Care Skills and Telephone Etiquette",
            "description": "Develop exceptional telephone communication skills for industrial sales. Learn professional etiquette, handling inquiries about pumps and valves over the phone, and creating positive impressions in every customer interaction.",
            "thumbnail": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 10,
            "code": "SE-TEL-003",
            "modules": []  # Full content to be added
        },
        {
            "title": "Diploma in Sales Management",
            "description": "Comprehensive diploma course covering all aspects of sales management in the industrial equipment sector. Learn team leadership, territory management, forecasting, and strategic sales planning for pumps and valves distribution.",
            "thumbnail": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 20,
            "code": "SE-DSM-004",
            "modules": []
        },
        {
            "title": "B2B Partnership Development",
            "description": "Learn how to identify, develop, and maintain strategic B2B partnerships in the industrial equipment market. Focus on building distributor networks, OEM relationships, and strategic alliances for Flowitec products.",
            "thumbnail": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-BPD-005",
            "modules": []
        },
        {
            "title": "Mastering Influence and Negotiation",
            "description": "Develop advanced negotiation skills for complex B2B sales in the industrial sector. Learn persuasion techniques, handling objections, and closing strategies for high-value pump and valve contracts.",
            "thumbnail": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 14,
            "code": "SE-MIN-006",
            "modules": []
        },
        {
            "title": "Marketing Management - Capturing Market Insights",
            "description": "Learn how to gather and analyze market intelligence in the industrial equipment sector. Understand competitor analysis, customer needs assessment, and market trends affecting the pumps and valves industry.",
            "thumbnail": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-MMI-007",
            "modules": []
        },
        {
            "title": "Introduction to Marketing Management",
            "description": "Foundational course in marketing management principles applied to industrial equipment sales. Learn marketing fundamentals, positioning strategies, and promotional approaches for Flowitec products.",
            "thumbnail": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 10,
            "code": "SE-IMM-008",
            "modules": []
        },
        {
            "title": "Mastering Influence in Sales",
            "description": "Advanced course on building influence with industrial customers. Learn how to become a trusted advisor, guide purchase decisions, and influence stakeholders across engineering, procurement, and management.",
            "thumbnail": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-MIS-009",
            "modules": []
        },
        {
            "title": "Sales Techniques - Interacting with Customers",
            "description": "Practical sales techniques for effective customer interactions in industrial settings. Learn consultative selling, needs discovery, solution presentation, and relationship building for pumps and valves sales.",
            "thumbnail": "https://images.unsplash.com/photo-1557426272-fc759fdf7a8d?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-STI-010",
            "modules": []
        },
        {
            "title": "Sales and Negotiation Skills",
            "description": "Comprehensive course combining sales methodology with negotiation tactics for industrial equipment. Learn the complete sales cycle from prospecting to closing for high-value fluid handling solutions.",
            "thumbnail": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 14,
            "code": "SE-SNS-011",
            "modules": []
        },
        {
            "title": "Understanding Key Account Management",
            "description": "Master the art of managing strategic accounts in the industrial sector. Learn account planning, relationship mapping, growth strategies, and retention tactics for major pump and valve customers.",
            "thumbnail": "https://images.unsplash.com/photo-1552581234-26160f608093?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 14,
            "code": "SE-KAM-012",
            "modules": []
        },
        {
            "title": "Understanding Market Demand, Branding and Communications",
            "description": "Learn to analyze market demand and build brand presence in the industrial equipment market. Understand how branding and communications drive sales success for pumps and valves.",
            "thumbnail": "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-MBC-013",
            "modules": []
        },
        {
            "title": "Effective Sales Skills",
            "description": "Core sales skills development for industrial equipment professionals. Learn prospecting, qualifying, presenting, handling objections, and closing techniques specific to the pumps and valves industry.",
            "thumbnail": "https://images.unsplash.com/photo-1560472355-536de3962603?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-ESS-014",
            "modules": []
        },
        {
            "title": "Sales Techniques - Using Competitive Strategies",
            "description": "Advanced competitive strategies for industrial sales. Learn to analyze competitors, position against them, and win deals in competitive bid situations for pumps, valves, and fluid systems.",
            "thumbnail": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 12,
            "code": "SE-CSS-015",
            "modules": []
        },
        {
            "title": "B2B Lead Generation Techniques",
            "description": "Learn proven techniques for generating quality leads in the industrial B2B space. Master digital and traditional lead generation strategies for the pumps and valves market.",
            "thumbnail": "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 10,
            "code": "SE-BLG-016",
            "modules": []
        },
        {
            "title": "Advanced B2B Marketing Strategies",
            "description": "Advanced marketing strategies for B2B industrial markets. Learn account-based marketing, content marketing, digital strategies, and integrated campaigns for the fluid handling industry.",
            "thumbnail": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=225&fit=crop",
            "category": "SALES (ENGINEER)",
            "duration_hours": 14,
            "code": "SE-ABM-017",
            "modules": []
        }
    ]
