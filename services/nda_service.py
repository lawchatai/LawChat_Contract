def generate_employment_nda(data):
    employer_name = data.get("employer_name", [""])[0]
    employer_type = data.get("employer_type", [""])[0]
    employee_name = data.get("employee_name", [""])[0]
    designation = data.get("designation", [""])[0]
    effective_date = data.get("effective_date", [""])[0]
    jurisdiction = data.get("jurisdiction", [""])[0]
    post_duration = data.get("post_duration", [""])[0]

    confidential_items = data.get("confidential[]", [])

    confidential_text = ", ".join(confidential_items)

    nda = f"""
EMPLOYEE CONFIDENTIALITY AND NON-DISCLOSURE AGREEMENT

This Agreement is made on {effective_date}

BETWEEN

{employer_name}, a {employer_type},  
(hereinafter referred to as the "Employer")

AND

{employee_name}, employed as {designation},  
(hereinafter referred to as the "Employee")

1. CONFIDENTIAL INFORMATION  
The Employee agrees that all confidential information including
{confidential_text} shall remain strictly confidential.

2. PURPOSE  
Confidential information shall be used solely for employment purposes.

3. TERM  
This Agreement shall continue during employment and for {post_duration} years
after termination.

4. RETURN OF PROPERTY  
Upon termination, the Employee shall return all confidential material.

5. GOVERNING LAW  
This Agreement shall be governed by the laws of India.
Courts at {jurisdiction} shall have exclusive jurisdiction.

IN WITNESS WHEREOF,
The parties have executed this Agreement on the date first written above.
"""

    return nda.strip()
