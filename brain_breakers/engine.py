"""Independent source ledger oracle and per-case fault-preserving reduction."""
import copy
import hashlib
import json
from .adapters import ADAPTERS

FAULTS={"none","drop_delete","drop_update","ignore_scope"}
def validate(case):
    if not isinstance(case,dict) or not isinstance(case.get("id"),str) or not isinstance(case.get("documents"),list) or not 1<=len(case["documents"])<=24 or not isinstance(case.get("operations"),list) or len(case["operations"])>12:raise ValueError("invalid_case")
    docs=list(case["documents"])
    for op in case["operations"]:
        if op.get("type") not in ("delete","upsert"):raise ValueError("invalid_operation")
        if op["type"]=="upsert":docs.append(op.get("document"))
        elif not isinstance(op.get("id"),str):raise ValueError("invalid_delete")
    for doc in docs:
        if not isinstance(doc,dict) or any(not isinstance(doc.get(k),str) or not 1<=len(doc[k])<=1000 for k in ("id","tenant","key","value")) or type(doc.get("revision")) is not int or doc["revision"]<0:raise ValueError("invalid_document")
    if len({d["id"] for d in case["documents"]})!=len(case["documents"]):raise ValueError("duplicate_document")
    if any(not isinstance(case.get("query",{}).get(k),str) or not case["query"][k] for k in ("key","tenant")):raise ValueError("invalid_query")
    return case

def oracle(ledger,query):
    rows=[d for d in ledger.values() if d["tenant"]==query["tenant"] and d["key"]==query["key"]]
    if not rows:return {"value":None,"source_ids":[]}
    revision=max(d["revision"] for d in rows);current=[d for d in rows if d["revision"]==revision]
    values={d["value"] for d in current}
    # Conflicting equally current sources demand abstention, not arbitrary tie breaking.
    return {"value":next(iter(values)) if len(values)==1 else None,"source_ids":sorted(d["id"] for d in current),"conflict":len(values)>1}

def answer(rows):
    if not rows:return {"value":None,"source_ids":[]}
    current=sorted(rows,key=lambda d:(-d["revision"],d["id"]));revision=current[0]["revision"];current=[d for d in current if d["revision"]==revision]
    values={d["value"] for d in current}
    return {"value":current[0]["value"] if len(values)==1 else None,"source_ids":sorted(d["id"] for d in current)}

def check(result,rows,ledger,query):
    expected=oracle(ledger,query)
    invalid_sources=[d["id"] for d in rows if d["id"] not in ledger or ledger[d["id"]]!=d]
    leaked=[d["id"] for d in rows if d["tenant"]!=query["tenant"]]
    values_match=result["value"]==expected["value"]
    valid_support=set(result["source_ids"]).issubset(set(expected["source_ids"])) and (result["value"] is None or bool(result["source_ids"]))
    failures=[]
    if not values_match:failures.append("answer_mismatch")
    if invalid_sources:failures.append("stale_retrieval")
    if leaked:failures.append("scope_leak")
    if not valid_support:failures.append("invalid_support")
    return {"passed":not failures,"failures":failures,"expected":expected,"answer":result,"retrieved":rows,"stale_ids":invalid_sources,"leaked_ids":leaked}

def run_trial(case,backend="sqlite_fts5",fault="none"):
    validate(case)
    if backend not in ADAPTERS or fault not in FAULTS:raise ValueError("invalid_adapter")
    adapter=ADAPTERS[backend]();ledger={};indexed={};trace=[]
    try:
        for doc in case["documents"]:adapter.upsert(doc);ledger[doc["id"]]=copy.deepcopy(doc);indexed[doc["id"]]=copy.deepcopy(doc)
        def probe(stage):
            rows=adapter.retrieve(case["query"],scope=fault!="ignore_scope");rows=sorted(rows,key=lambda d:d["id"])
            result=check(answer(rows),rows,ledger,case["query"]);trace.append({"stage":stage,**result});return result
        initial=probe("baseline")
        for i,op in enumerate(case["operations"]):
            if op["type"]=="delete":
                ledger.pop(op["id"],None)
                if fault!="drop_delete":adapter.delete(op["id"]);indexed.pop(op["id"],None)
            else:
                doc=op["document"];ledger[doc["id"]]=copy.deepcopy(doc)
                if fault!="drop_update" or doc["id"] not in indexed:adapter.upsert(doc);indexed[doc["id"]]=copy.deepcopy(doc)
            probe(f"mutation_{i+1}")
        final=trace[-1]
        return {"case_id":case["id"],"backend":backend,"backend_version":adapter.version,"fault":fault,"fault_is_injected_client_integration":fault!="none","initial_passed":initial["passed"],"passed":all(t["passed"] for t in trace),"final":final,"trace":trace,
            "answer_changed":initial["answer"]["value"]!=final["answer"]["value"],"redundant_support_preserved":initial["answer"]["value"]==final["answer"]["value"] and final["passed"] and bool(final["answer"]["source_ids"]),
            "case_sha256":hashlib.sha256(json.dumps(case,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()}
    finally:adapter.close()

def minimize(case,backend="sqlite_fts5",fault="drop_delete"):
    original=run_trial(case,backend,fault);signature=original["final"]["failures"]
    if original["passed"] or not original["initial_passed"]:return {"case":copy.deepcopy(case),"removed":[],"trial":original,"locally_minimal":False}
    result=copy.deepcopy(case);removed=[]
    protected={op["id"] if op["type"]=="delete" else op["document"]["id"] for op in case["operations"]}
    changed=True
    while changed:
        changed=False
        for doc in list(result["documents"]):
            if doc["id"] in protected or len(result["documents"])<=1:continue
            candidate=copy.deepcopy(result);candidate["documents"]=[d for d in candidate["documents"] if d["id"]!=doc["id"]]
            trial=run_trial(candidate,backend,fault)
            if trial["initial_passed"] and trial["final"]["failures"]==signature and not trial["passed"]:result=candidate;removed.append(doc["id"]);changed=True
    return {"case":result,"removed":removed,"trial":run_trial(result,backend,fault),"locally_minimal":True}

def suite(cases,backends=("sqlite_fts5",),reduce=True):
    rows=[]
    for backend in backends:
        for case in cases:
            fault=case["injected_fault"]
            row={"case_id":case["id"],"backend":backend,"injected":run_trial(case,backend,fault),"repaired":run_trial(case,backend,"none")}
            if reduce:row["reduction"]=minimize(case,backend,fault)
            rows.append(row)
    return {"trials":rows,"paired_trials":len(rows),"repaired_passed":sum(r["repaired"]["passed"] for r in rows),"injected_detected":sum(not r["injected"]["passed"] for r in rows),"upstream_bugs_claimed":0,"human_adoption_claimed":False}
