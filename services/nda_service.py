def generate_employment_nda(data):
    def get_value(key, default=""):
        return data.get(key, [default])[0].strip()

    employer_name = get_value("employer_name")
    employee_name = get_value("employee_name")
    designation = get_value("designation")
    effective_date = get_value("effective_date", "__________")
    governing_law = get_value("governing_law", "laws of India")
    jurisdiction = get_value("jurisdiction", "Courts at New Delhi")

    confidential_items = data.get("confidential[]", [])
    if confidential_items:
        confidential_text = ", ".join(confidential_items)
    else:
        confidential_text = (
            "business plans, source code, software architecture, trade secrets, "
            "customer data, financial information, internal documents, processes, "
            "product designs, and proprietary technical or commercial information"
        )

    nda = f"""
EMPLOYMENT NON-DISCLOSURE AGREEMENT

This Employment Non-Disclosure Agreement (“Agreement”) is entered into on {effective_date}
between {employer_name}, a company incorporated under the applicable laws (“Company”),
and {employee_name}, employed as {designation} (“Employee”).

1. Purpose

In the course of Employee’s employment and in consideration of Employee’s employment,
continued employment, and access to Confidential Information, Employee agrees to comply
with the obligations set out in this Agreement.

2. Definition of Confidential Information

“Confidential Information” means all information, whether written, electronic, oral,
visual, or in any other form, disclosed to Employee by Company or accessed by Employee
during employment, that is not generally available to the public and is reasonably
understood to be confidential, including but not limited to: {confidential_text}.

Confidential Information does not include information that:
(a) is publicly available through no fault of Employee;
(b) was lawfully known to Employee prior to disclosure by Company;
(c) is lawfully received from a third party without breach of any obligation; or
(d) is required to be disclosed pursuant to law, regulation, or court order,
provided Employee gives prompt notice to Company where legally permissible.

3. Non-Disclosure and Limited Use

Employee shall not, directly or indirectly, during or after employment, disclose
Confidential Information to any third party or use such Confidential Information
for any purpose other than in the ordinary course of performing duties for the
Company, without prior written consent of the Company.

4. Confidential Information of Third Parties

Employee agrees not to improperly use or disclose confidential or proprietary
information belonging to any third party in the course of employment.

5. Return of Company Property

Upon termination of employment for any reason, Employee shall promptly return
all documents, data, records, devices, and materials containing Confidential Information,
whether in physical or electronic form.

6. Survival of Obligations

The obligations under this Agreement shall survive termination of employment
for so long as the Confidential Information remains confidential under applicable law.

7. General Provisions

(a) Severability: If any provision is held unenforceable, the remaining provisions
shall continue in full force and effect.

(b) Entire Agreement: This Agreement constitutes the entire understanding regarding
confidentiality and supersedes all prior agreements on the subject.

(c) Waiver: Failure to enforce any provision shall not constitute a waiver.

(d) Injunctive Relief: Company shall be entitled to seek injunctive or equitable relief
for any breach or threatened breach of this Agreement.

(e) Governing Law: This Agreement shall be governed by the {governing_law}.

(f) Jurisdiction: {jurisdiction} shall have exclusive jurisdiction.

8. Signatures

Employee:
Signature: ______________________
Name: {employee_name}
Date: ______________________

Company:
Signature: ______________________
Name: {employer_name}
Designation: ____________________
Date: ______________________
"""

    return nda.strip()



# def generate_employment_nda(data):
#     employer_name = data.get("employer_name", [""])[0]
#     employee_name = data.get("employee_name", [""])[0]
#     designation = data.get("designation", [""])[0]
#     effective_date = data.get("effective_date", [""])[0]
#     governing_law = data.get("governing_law", ["laws of India"])[0]
#     jurisdiction = data.get("jurisdiction", ["courts at New Delhi"])[0]
#     confidential_items = data.get("confidential[]", [])
#     confidential_text = ", ".join(confidential_items)
#
#     nda = f"""
# EMPLOYMENT NON-DISCLOSURE AGREEMENT
#
# This Employment Non-Disclosure Agreement (“Agreement”) is entered into on {effective_date}
# between {employer_name}, a company incorporated under applicable laws (“Company”),
# and {employee_name}, employed as {designation} (“Employee”).
#
# 1. Purpose
#
# In the course of Employee’s employment and in consideration of Employee’s employment,
# continued employment, and access to Confidential Information, Employee agrees to comply
# with the obligations set out in this Agreement.
#
# 2. Definition of Confidential Information
#
# “Confidential Information” means all information, whether written, electronic, oral,
# visual, or in any other form, disclosed to Employee by Company or accessed by Employee
# during employment, that is not generally available to the public and is reasonably
# understood to be confidential, including but not limited to: {confidential_text}.
#
# Confidential Information does not include information that:
# (a) is publicly available through no fault of Employee;
# (b) was lawfully known to Employee prior to disclosure by Company;
# (c) is lawfully received from a third party without breach of any obligation; or
# (d) is required to be disclosed pursuant to law, regulation, or court order,
# provided Employee gives prompt notice to Company where legally permissible.
#
# 3. Non-Disclosure and Limited Use
#
# Employee shall not, during or after employment, disclose Confidential Information
# to any third party or use such information for any purpose other than performance
# of duties for Company without prior written consent of Company.
#
# 4. Confidential Information of Third Parties
#
# Employee agrees not to improperly use or disclose confidential or proprietary
# information belonging to any third party.
#
# 5. Return of Company Property
#
# Upon termination of employment for any reason, Employee shall promptly return
# all documents, data, records, devices, and materials containing Confidential Information,
# whether in physical or electronic form.
#
# 6. Survival of Obligations
#
# The obligations under this Agreement shall survive termination of employment
# for so long as the Confidential Information remains confidential under applicable law.
#
# 7. General Provisions
#
# (a) No Partnership: Nothing herein creates an employer–employee relationship beyond
# existing employment terms, partnership, or agency.
#
# (b) Severability: If any provision is held unenforceable, the remaining provisions
# shall continue in full force.
#
# (c) Entire Agreement: This Agreement constitutes the entire understanding regarding
# confidentiality and supersedes prior agreements on the subject.
#
# (d) Waiver: Failure to enforce any provision shall not constitute a waiver.
#
# (e) Injunctive Relief: Company shall be entitled to seek injunctive or equitable relief
# for breach of this Agreement.
#
# (f) Governing Law: This Agreement shall be governed by the {governing_law}.
# (g) Jurisdiction: {jurisdiction} shall have exclusive jurisdiction.
#
#
# 8. Signatures
#
# Employee:
# Signature: ______________________
# Name: {employee_name}
# Date: ______________________
#
# Company:
# Signature: ______________________
# Name: {employer_name}
# Date: ______________________
#
# """
#     return nda.strip()
