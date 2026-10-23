"""
Test Suite for HR Policy Assistant RAG Chatbot.

Evaluates the 5 required LMS test questions against the real Enso Group HR Policy Manual:
1. How many days of Privilege Leave (PL) does a permanent employee get per year?
2. What is the probation period for employees up to Senior Manager?
3. What is the company's health-insurance premium amount?
4. What is the current GST rate in India?
5. How many days of maternity leave are given?

Saves comprehensive test results and citations to reports/test_report.md.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config
from rag_pipeline import query_hr_assistant

TEST_QUESTIONS = [
    {
        "id": 1,
        "question": "How many days of Privilege Leave (PL) does a permanent employee get per year?",
        "expected_status": "FOUND",
        "expected_page": 60,
        "expected_keywords": ["12", "days"],
    },
    {
        "id": 2,
        "question": "What is the probation period for employees up to Senior Manager?",
        "expected_status": "FOUND",
        "expected_page": 42,
        "expected_keywords": ["3", "months"],
    },
    {
        "id": 3,
        "question": "What is the company's health-insurance premium amount?",
        "expected_status": "NOT_FOUND",
        "expected_page": None,
        "expected_keywords": ["not found"],
    },
    {
        "id": 4,
        "question": "What is the current GST rate in India?",
        "expected_status": "NOT_FOUND",
        "expected_page": None,
        "expected_keywords": ["not found"],
    },
    {
        "id": 5,
        "question": "How many days of maternity leave are given?",
        "expected_status": "FOUND",
        "expected_page": 62,
        "expected_keywords": ["12 weeks", "90", "days"],
    },
]


def run_tests():
    print("=" * 80)
    print("🧪 Running Evaluation Suite: 5 LMS Questions on HR Policy Manual")
    print("=" * 80)

    results = []
    report_lines = []
    report_lines.append("# HR Policy Assistant — LMS Evaluation Report")
    report_lines.append(f"\n**Execution Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Gemini Model:** `{config.GEMINI_MODEL}`")
    report_lines.append(f"**Embedding Model:** `{config.EMBEDDING_MODEL}`")
    report_lines.append(f"**Vector Database:** ChromaDB (`{config.CHROMA_DIR.name}`)\n")
    report_lines.append("## Test Results Summary\n")
    report_lines.append("| Q# | Question | Expected | Chatbot Answer | Reference | Status |")
    report_lines.append("|---|---|---|---|---|---|")

    passed_count = 0

    for item in TEST_QUESTIONS:
        qid = item["id"]
        q_text = item["question"]
        print(f"\n--- [Question {qid}] {q_text} ---")

        res = query_hr_assistant(q_text)
        ans = res["answer"]
        ref = res["reference"]
        sources = res["sources"]

        print(f"Chatbot Output:")
        print(f"  Answer:    {ans}")
        print(f"  Reference: {ref}")

        # Validation logic
        passed = False
        if item["expected_status"] == "NOT_FOUND":
            if ans.strip().lower() == "not found":
                passed = True
                status_str = "✅ PASSED (Strict Not found)"
            else:
                status_str = f"❌ FAILED (Expected 'Not found', got '{ans}')"
        else:
            # Expected to be found
            has_keywords = any(k.lower() in ans.lower() for k in item["expected_keywords"])
            has_page = str(item["expected_page"]) in ref or any(
                str(item["expected_page"]) == str(s.get("page")) for s in sources[:2]
            )
            if res["is_found"] and has_keywords and has_page:
                passed = True
                status_str = f"✅ PASSED (Verified Page {item['expected_page']})"
            else:
                status_str = f"❌ FAILED (Keyword match: {has_keywords}, Page match: {has_page})"

        if passed:
            passed_count += 1

        print(f"Evaluation: {status_str}")

        # Add to table
        clean_ans_cell = ans.replace("\n", " ").replace("|", "/")
        clean_ref_cell = ref.replace("\n", " ").replace("|", "/") if ref else "N/A"
        report_lines.append(
            f"| {qid} | {q_text} | {item['expected_status']} | {clean_ans_cell} | {clean_ref_cell} | {status_str} |"
        )

        results.append({
            "item": item,
            "res": res,
            "passed": passed,
            "status_str": status_str,
        })

    # Detailed section
    report_lines.append("\n---\n")
    report_lines.append("## Detailed Evidence and Reasoning\n")

    for r in results:
        it = r["item"]
        resp = r["res"]
        report_lines.append(f"### Question {it['id']}: {it['question']}\n")
        report_lines.append(f"- **Expected Behavior:** `{it['expected_status']}`")
        report_lines.append(f"- **Model Output:**\n  ```\n  Answer: {resp['answer']}\n  Reference: {resp['reference'] or 'N/A'}\n  ```")
        report_lines.append(f"- **Validation Status:** {r['status_str']}")
        
        if resp["sources"]:
            top_source = resp["sources"][0]
            report_lines.append(f"- **Top Retrieved Chunk:** Page {top_source.get('page')}, Section `{top_source.get('section')}`")
            clean_snippet = top_source.get('content', '')[:300].replace('\n', ' ')
            report_lines.append(f"  > *\"{clean_snippet}...\"*\n")
        report_lines.append("\n")

    report_lines.append(f"## Conclusion\n")
    report_lines.append(f"**Total Questions:** {len(TEST_QUESTIONS)}  ")
    report_lines.append(f"**Passed:** {passed_count}/{len(TEST_QUESTIONS)} ({(passed_count / len(TEST_QUESTIONS)) * 100:.1f}%)  ")
    if passed_count == len(TEST_QUESTIONS):
        report_lines.append("\n🎉 **All test questions successfully satisfied strict grounding and hallucination prevention criteria!**")

    # Save report
    config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = config.REPORTS_DIR / "test_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("\n" + "=" * 80)
    print(f"📊 Evaluation Complete: {passed_count}/{len(TEST_QUESTIONS)} Passed!")
    print(f"📄 Detailed Report saved to: {report_path}")
    print("=" * 80)

    return passed_count == len(TEST_QUESTIONS)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
