# HR Policy Assistant — LMS Evaluation Report

**Execution Date:** 2026-10-23 15:44:09
**Gemini Model:** `gemini-3.5-flash`
**Embedding Model:** `models/gemini-embedding-001`
**Vector Database:** ChromaDB (`chroma_db`)

## Test Results Summary

| Q# | Question | Expected | Chatbot Answer | Reference | Status |
|---|---|---|---|---|---|
| 1 | How many days of Privilege Leave (PL) does a permanent employee get per year? | FOUND | Permanent employees are allowed 12 days of Privilege Leave (PL) per calendar year. | Page 60, [G] Leave Policy | ✅ PASSED (Verified Page 60) |
| 2 | What is the probation period for employees up to Senior Manager? | FOUND | All employees up to Sr. Manager are placed in probation for a period of 3 months from the date of their joining. | Page 42, [B] Probation Policy | ✅ PASSED (Verified Page 42) |
| 3 | What is the company's health-insurance premium amount? | NOT_FOUND | Not found | N/A | ✅ PASSED (Strict Not found) |
| 4 | What is the current GST rate in India? | NOT_FOUND | Not found | N/A | ✅ PASSED (Strict Not found) |
| 5 | How many days of maternity leave are given? | FOUND | A total of 12 weeks (90 days) of Maternity Leave with pay is provided, of which not more than 6 weeks (45 days) should precede the expected date of delivery. | Page 62, [G] Leave Policy | ✅ PASSED (Verified Page 62) |

---

## Detailed Evidence and Reasoning

### Question 1: How many days of Privilege Leave (PL) does a permanent employee get per year?

- **Expected Behavior:** `FOUND`
- **Model Output:**
  ```
  Answer: Permanent employees are allowed 12 days of Privilege Leave (PL) per calendar year.
  Reference: Page 60, [G] Leave Policy
  ```
- **Validation Status:** ✅ PASSED (Verified Page 60)
- **Top Retrieved Chunk:** Page 60, Section `[G] Leave Policy`
  > *"ԂԂ All leaves should be approved by the manager on mail. Scope & Eligibility Policy Features Leave Type Eligibility Entitlement Encashment Procedure Privilege Leave (PL) -> All permanent      employees are    eligible to avail PL. -> PL is calculat­ ed for a period of  one calendar year  (1st Jan-31..."*



### Question 2: What is the probation period for employees up to Senior Manager?

- **Expected Behavior:** `FOUND`
- **Model Output:**
  ```
  Answer: All employees up to Sr. Manager are placed in probation for a period of 3 months from the date of their joining.
  Reference: Page 42, [B] Probation Policy
  ```
- **Validation Status:** ✅ PASSED (Verified Page 42)
- **Top Retrieved Chunk:** Page 42, Section `[B] Probation Policy`
  > *"HR Manual - 42 [B] Probation Policy Meaning/Purpose      The probationary period is a time for you to learn about your job and become familiar with the Working  culture of Enso Group.       During this time, your supervisor will explain you your department’s policies and procedure, your job  duties,..."*



### Question 3: What is the company's health-insurance premium amount?

- **Expected Behavior:** `NOT_FOUND`
- **Model Output:**
  ```
  Answer: Not found
  Reference: N/A
  ```
- **Validation Status:** ✅ PASSED (Strict Not found)
- **Top Retrieved Chunk:** Page 72, Section `[A] Long Distance Travel Policy`
  > *"ԂԂ Rates to be revsed every 3 years. CLAUSE OF REIMBURSEMENT DURING EXIT: ԂԂ In case of employee resignation, his/her reimbursement requests shall be processed along with full and  final settlement only...."*



### Question 4: What is the current GST rate in India?

- **Expected Behavior:** `NOT_FOUND`
- **Model Output:**
  ```
  Answer: Not found
  Reference: N/A
  ```
- **Validation Status:** ✅ PASSED (Strict Not found)
- **Top Retrieved Chunk:** Page 72, Section `[A] Long Distance Travel Policy`
  > *"ԂԂ Rates to be revsed every 3 years. CLAUSE OF REIMBURSEMENT DURING EXIT: ԂԂ In case of employee resignation, his/her reimbursement requests shall be processed along with full and  final settlement only...."*



### Question 5: How many days of maternity leave are given?

- **Expected Behavior:** `FOUND`
- **Model Output:**
  ```
  Answer: A total of 12 weeks (90 days) of Maternity Leave with pay is provided, of which not more than 6 weeks (45 days) should precede the expected date of delivery.
  Reference: Page 62, [G] Leave Policy
  ```
- **Validation Status:** ✅ PASSED (Verified Page 62)
- **Top Retrieved Chunk:** Page 62, Section `[G] Leave Policy`
  > *"HR Manual - 62 Leave Type Eligibility Entitlement Encashment Procedure Maternity Leave  (Leeway) -> ML shall be     available to all   confirmed female   staff in accordance   with the law   applicable from   time to time. ->Female  staff,  who have worked  for at least 80days  in  preceding  12mont..."*



## Conclusion

**Total Questions:** 5  
**Passed:** 5/5 (100.0%)  

🎉 **All test questions successfully satisfied strict grounding and hallucination prevention criteria!**