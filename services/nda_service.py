# def generate_employment_nda(data):
#     employer_name = data.get("employer_name", [""])[0]
#     employer_type = data.get("employer_type", [""])[0]
#     employee_name = data.get("employee_name", [""])[0]
#     designation = data.get("designation", [""])[0]
#     effective_date = data.get("effective_date", [""])[0]
#     jurisdiction = data.get("jurisdiction", [""])[0]
#     post_duration = data.get("post_duration", [""])[0]
#
#     confidential_items = data.get("confidential[]", [])
#
#     confidential_text = ", ".join(confidential_items)
#
#     nda = f"""
# EMPLOYEE CONFIDENTIALITY AND NON-DISCLOSURE AGREEMENT
#
# This Agreement is made on {effective_date}
#
# BETWEEN
#
# {employer_name}, a {employer_type},
# (hereinafter referred to as the "Employer")
#
# AND
#
# {employee_name}, employed as {designation},
# (hereinafter referred to as the "Employee")
#
# 1. CONFIDENTIAL INFORMATION
# The Employee agrees that all confidential information including
# {confidential_text} shall remain strictly confidential.
#
# 2. PURPOSE
# Confidential information shall be used solely for employment purposes.
#
# 3. TERM
# This Agreement shall continue during employment and for {post_duration} years
# after termination.
#
# 4. RETURN OF PROPERTY
# Upon termination, the Employee shall return all confidential material.
#
# 5. GOVERNING LAW
# This Agreement shall be governed by the laws of India.
# Courts at {jurisdiction} shall have exclusive jurisdiction.
#
# IN WITNESS WHEREOF,
# The parties have executed this Agreement on the date first written above.
# """
#
#     return nda.strip()

def generate_employment_nda(data):
    employer_name = data.get("employer_name", [""])[0]
    employee_name = data.get("employee_name", [""])[0]
    designation = data.get("designation", [""])[0]
    effective_date = data.get("effective_date", [""])[0]
    jurisdiction = data.get("jurisdiction", [""])[0]
    state_law = data.get("state_law", [""])[0]
    confidential_items = data.get("confidential[]", [])
    confidential_text = ", ".join(confidential_items)

    nda = f"""
EMPLOYEE NONDISCLOSURE AGREEMENT

This agreement (the “Agreement”) is entered into on {effective_date} by {employer_name} (“Company”) 
and {employee_name}, employed as {designation} (“Employee”).

In consideration of the commencement of Employee’s employment with Company and the compensation that will be paid, Employee and Company agree as follows:

1. Company’s Trade Secrets

In the performance of Employee’s job duties with Company, Employee will be exposed to Company’s Confidential Information. “Confidential Information” means information or material that is commercially valuable to Company and not generally known or readily ascertainable in the industry. This includes, but is not limited to: {confidential_text}.

2. Nondisclosure of Trade Secrets

The Employee shall keep Company’s Confidential Information, whether or not prepared or developed by Employee, in the strictest confidence. The Employee will not disclose such information to anyone outside Company without Company’s prior written consent, nor will Employee make use of any Confidential Information for Employee’s own purposes or the benefit of anyone other than Company.

However, Employee shall have no obligation to treat as confidential any information which:
(a) was in Employee’s possession or known to Employee, without an obligation to keep it confidential, before such information was disclosed to Employee by Company;
(b) is or becomes public knowledge through a source other than Employee and through no fault of Employee; or
(c) is or becomes lawfully available to Employee from a source other than Company.

3. Confidential Information of Others

The Employee will not disclose to Company, use in Company’s business, or cause Company to use, any trade secret of others.

4. Return of Materials

When Employee’s employment with Company ends, for whatever reason, Employee will promptly deliver to Company all originals and copies of all documents, records, software programs, media and other materials containing any Confidential Information. The Employee will also return all equipment, files, software programs and other personal property belonging to Company.

5. Confidentiality Obligation Survives Employment

Employee’s obligation to maintain the confidentiality and security of Confidential Information remains even after Employee’s employment with Company ends and continues for so long as such Confidential Information remains a trade secret.

6. General Provisions

(a) Relationships: Nothing contained in this Agreement shall be deemed to make Employee a partner or joint venturer of Company for any purpose.
(b) Severability: If a court finds any provision invalid or unenforceable, the remainder shall be interpreted to best effect the intent of the parties.
(c) Integration: This Agreement expresses the complete understanding and supersedes all prior agreements.
(d) Waiver: Failure to exercise any right shall not be a waiver of prior or subsequent rights.
(e) Injunctive Relief: Employee agrees that Company may apply to a court for an order enjoining misappropriation of Confidential Information.
(f) Indemnity: Employee agrees to indemnify Company against losses due to breach of this Agreement.
(g) Attorney Fees: The prevailing party may collect reasonable attorney fees and costs.
(h) Governing Law: This Agreement shall be governed by the laws of the State of {state_law}.
(i) Jurisdiction: The Employee consents to the exclusive jurisdiction of the federal and state courts located in {jurisdiction}.
(j) Successors & Assigns: This Agreement shall bind each party’s heirs, successors, and assigns.

7. Notice of Immunity

Employee is provided notice that they shall not be held criminally or civilly liable under any federal or state trade secret law for disclosure of a trade secret as part of certain legal or governmental proceedings.

8. Signatures

Employee                                                                     Company

Signature _____________________                                              Signature _____________________
Name __________________________                                              Name __________________________
Date __________________________                                              Date __________________________
"""
    return nda.strip()
