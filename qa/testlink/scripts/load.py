"""Load one tester's requirements + test cases (scripts/<name>_testdata.py) into the local TestLink.

Usage: python3 -I qa/testlink/scripts/load.py <name>     e.g. load.py aland
Resumes interrupted imports and refreshes cases by stable name. Writes requirements XML to qa/project1/<name>/.
"""
import importlib
import html
import http.cookiejar
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid
import xmlrpc.client
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
NAME = sys.argv[1].lower()
_data = importlib.import_module(f"{NAME}_testdata")
from validate import validate_module
validate_module(_data)
from config import BASE, PROJECT, PREFIX, PLAN, BUILD, REPO, SOURCE_COMMIT, roster, refresh_header
from bootstrap import ensure_user
AUTHOR, REQ_SPECS, SUITES = _data.AUTHOR, _data.REQ_SPECS, _data.SUITES
TOP_SUITE, TOP_SUITE_DETAILS = _data.TOP_SUITE, _data.TOP_SUITE_DETAILS
refresh_header()

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(os.path.dirname(KIT), "project1", NAME)
COMPOSE_DIR = KIT
ADMIN_PW = "admin"
KEY = None
api = xmlrpc.client.ServerProxy(f"{BASE}/lib/api/xmlrpc/v1/xmlrpc.php", allow_none=True)


def call(method, **kw):
    kw["devKey"] = KEY
    res = getattr(api.tl, method)(kw)
    if isinstance(res, list) and res and isinstance(res[0], dict) and "code" in res[0] and "message" in res[0]:
        raise RuntimeError(f"{method}: {res[0]['message']}")
    return res


def sql(q):
    out = subprocess.run(
        ["docker", "compose", "exec", "-T", "db", "mariadb", "-uroot", "-proot", "-N", "testlink", "-e", q],
        cwd=COMPOSE_DIR, capture_output=True, text=True, check=True,
    ).stdout
    return [line.split("\t") for line in out.strip().splitlines() if line]


KEY = sql("SELECT script_key FROM users WHERE login='admin'")[0][0]
ensure_user(AUTHOR, getattr(_data, 'FULL_NAME', AUTHOR.capitalize()))


def p(text):
    # TestLink 1.9.20 uses MySQL utf8mb3; numeric HTML entities preserve emoji
    # losslessly in report content without changing the upstream schema.
    return f"<p>{html.escape(text).encode('ascii', 'xmlcharrefreplace').decode()}</p>"


# ---------------------------------------------------------------- project
proj = next((x for x in call("getProjects") if x["name"] == PROJECT), None)
if not proj:
    call("createTestProject", testprojectname=PROJECT, testcaseprefix=PREFIX,
         notes="TaskFlow - single-user React/Vite task manager. SECJ3343 Project 1 local preparation environment. Import exports into the lecturer's existing project.",
         options={"requirementsEnabled": 1, "testPriorityEnabled": 1, "automationEnabled": 1, "inventoryEnabled": 0})
    proj = next(x for x in call("getProjects") if x["name"] == PROJECT)
PID = int(proj["id"])
sql(f"UPDATE users SET default_testproject_id={PID} WHERE login IN ('admin','{AUTHOR}')")
call("setUserRoleOnProject", userid=int(sql(f"SELECT id FROM users WHERE login='{AUTHOR}'")[0][0]),
     rolename="senior tester", testprojectid=PID)
for member in roster():
    ensure_user(member['login'], member['name'])
    uid = int(sql(f"SELECT id FROM users WHERE login='{member['login']}'")[0][0])
    call('setUserRoleOnProject', userid=uid, rolename='senior tester', testprojectid=PID)
print("project", PID)

# ---------------------------------------------------------------- requirements XML (test basis)
os.makedirs(OUT_DIR, exist_ok=True)
x = ['<?xml version="1.0" encoding="UTF-8"?>', "<requirement-specification>"]
for order, spec in enumerate(REQ_SPECS, 1):
    x.append(f'<req_spec title="{html.escape(spec["title"])}" doc_id="{spec["doc_id"]}">')
    x.append(f"<type>2</type><node_order>{order}</node_order>")
    x.append(f"<total_req>{len(spec['reqs'])}</total_req>")
    x.append(f"<scope><![CDATA[{p(spec['scope'])}]]></scope>")
    for n, (doc, title, desc) in enumerate(spec["reqs"], 1):
        x.append("<requirement>")
        x.append(f"<docid><![CDATA[{doc}]]></docid><title><![CDATA[{title}]]></title>")
        x.append(f"<version>1</version><revision>1</revision><node_order>{n}</node_order>")
        x.append(f"<description><![CDATA[{p(desc)}]]></description>")
        x.append("<status><![CDATA[V]]></status><type><![CDATA[3]]></type>")
        x.append("<expected_coverage>1</expected_coverage>")
        x.append("</requirement>")
    x.append("</req_spec>")
x.append("</requirement-specification>")
req_xml = os.path.join(OUT_DIR, f"{NAME}-requirements.xml")
open(req_xml, "w").write("\n".join(x))

if True:  # Import on every run so corrected requirements update in place.
    jar = http.cookiejar.CookieJar()
    web = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    def hidden(page):
        return dict(re.findall(r"name='(CSRF\w+)' value='([^']+)'", page))

    page = web.open(f"{BASE}/login.php").read().decode()
    form = {**hidden(page), "reqURI": "", "destination": "", "tl_login": AUTHOR, "tl_password": AUTHOR}
    web.open(f"{BASE}/login.php?viewer=", urllib.parse.urlencode(form).encode()).read()
    web.open(f"{BASE}/lib/general/navBar.php?testproject={PID}").read()
    page = web.open(f"{BASE}/lib/requirements/reqImport.php?scope=tree&req_spec_id={PID}").read().decode()
    fields = {**hidden(page), "scope": "tree", "importType": "XML", "MAX_FILE_SIZE": "409600",
              "hitCriteria": "docid", "actionOnHit": "update_last_version", "uploadFile": "Upload file"}
    bnd = uuid.uuid4().hex
    body = b"".join(f"--{bnd}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
                    for k, v in fields.items())
    body += (f"--{bnd}\r\nContent-Disposition: form-data; name=\"uploadedFile\"; filename=\"reqs.xml\"\r\n"
             f"Content-Type: text/xml\r\n\r\n").encode() + open(req_xml, "rb").read() + f"\r\n--{bnd}--\r\n".encode()
    req = urllib.request.Request(f"{BASE}/lib/requirements/reqImport.php?req_spec_id={PID}", body,
                                 {"Content-Type": f"multipart/form-data; boundary={bnd}"})
    res = re.sub(r"<[^>]+>", " ", web.open(req).read().decode())
    print("req import:", " ".join(res.split())[-400:])

reqs = {r[0]: (int(r[1]), int(r[2])) for r in sql(f"SELECT r.req_doc_id, r.id, r.srs_id FROM requirements r JOIN req_specs s ON s.id=r.srs_id WHERE s.testproject_id={PID}")}
missing = [d for s in REQ_SPECS for d, _, _ in s["reqs"] if d not in reqs]
assert not missing, f"requirements not imported: {missing}"
# Metadata belongs to the actual designer; repair the first admin-assisted import.
author_id = int(sql(f"SELECT id FROM users WHERE login='{AUTHOR}'")[0][0])
for spec in REQ_SPECS:
    spec_id = int(sql(f"SELECT id FROM req_specs WHERE testproject_id={PID} AND doc_id='{spec['doc_id']}'")[0][0])
    sql(f"UPDATE req_specs_revisions SET author_id={author_id}, total_req={len(spec['reqs'])}, type='2' WHERE parent_id={spec_id}")
    sql(f'UPDATE req_versions v JOIN nodes_hierarchy n ON n.id=v.id JOIN requirements r ON r.id=n.parent_id SET v.author_id={author_id} WHERE r.srs_id={spec_id}')
print("requirements", len(reqs))

# ---------------------------------------------------------------- suites + test cases
suites = call("getFirstLevelTestSuitesForTestProject", testprojectid=PID) if call("getProjects") else []
if isinstance(suites, list) and any(isinstance(s, dict) and s.get("name") == TOP_SUITE for s in suites):
    top_id = int(next(s['id'] for s in suites if s.get('name') == TOP_SUITE))
    print(f'{NAME}: resuming existing top suite {top_id}; existing complete cases are reused')
else:
    top_id = int(call("createTestSuite", testprojectid=PID, testsuitename=TOP_SUITE, details=TOP_SUITE_DETAILS)[0]["id"])

created = []
for order, suite in enumerate(SUITES, 1):
    safe_name = suite['name'].replace("'", "''")
    found = sql(f"SELECT id FROM nodes_hierarchy WHERE parent_id={top_id} AND node_type_id=2 AND name='{safe_name}'")
    sid = int(found[0][0]) if found else int(call("createTestSuite", testprojectid=PID, testsuitename=suite["name"], details=p(suite["details"]),
                   parentid=top_id, order=order)[0]["id"])
    for corder, tc in enumerate(suite["cases"], 1):
        summary = p(tc["name"] + ".") + f"<p><b>Test design technique:</b> {html.escape(tc['technique'])}</p>" \
            + f"<p><b>Requirements:</b> {', '.join(tc['reqs'])}</p>"
        steps = [{"step_number": i, "actions": p(a), "expected_results": p(e), "execution_type": 1}
                 for i, (a, e) in enumerate(tc["steps"], 1)]
        safe_case = tc['name'].replace("'", "''")
        found_case = sql(f"SELECT n.id,v.tc_external_id FROM nodes_hierarchy n JOIN nodes_hierarchy ver ON ver.parent_id=n.id JOIN tcversions v ON v.id=ver.id WHERE n.parent_id={sid} AND n.node_type_id=3 AND n.name='{safe_case}' ORDER BY v.version DESC LIMIT 1")
        if found_case:
            ext = f'{PREFIX}-{found_case[0][1]}'
            # Repair interrupted imports and refresh only this member's case content.
            call('updateTestCase', testcaseexternalid=ext, version=1, user=AUTHOR, summary=summary,
                 preconditions=p(tc['pre']), steps=steps, importance=tc['importance'])
        else:
            r = call("createTestCase", testprojectid=PID, testsuiteid=sid, testcasename=tc["name"], authorlogin=AUTHOR,
                     summary=summary, preconditions=p(tc["pre"]), steps=steps, importance=tc["importance"],
                     executiontype=1, order=corder, checkduplicatedname=1, actiononduplicatedname="block")[0]
            ext = f"{PREFIX}-{r['additionalInfo']['external_id']}"
        by_spec = {}
        # Replace mappings for this version, avoiding stale links after a design edit.
        version_id = int(sql(f"SELECT v.id FROM tcversions v JOIN nodes_hierarchy vn ON vn.id=v.id JOIN nodes_hierarchy n ON n.id=vn.parent_id WHERE n.parent_id={sid} AND v.tc_external_id={int(ext.split('-')[-1])} ORDER BY v.version DESC LIMIT 1")[0][0])
        sql(f'DELETE FROM req_coverage WHERE tcversion_id={version_id}')
        for d in tc["reqs"]:
            rid, spec = reqs[d]
            by_spec.setdefault(spec, []).append(rid)
        call("assignRequirements", testcaseexternalid=ext, testprojectid=PID,
             requirements=[{"req_spec": s, "requirements": ids} for s, ids in by_spec.items()])
        created.append(ext)
        print(ext, tc["name"])

# ---------------------------------------------------------------- plan, build, assignment
plans = call("getProjectTestPlans", testprojectid=PID) or []
plan = next((t for t in plans if isinstance(t, dict) and t.get("name") == PLAN), None)
if not plan:
    call("createTestPlan", testplanname=PLAN, testprojectname=PROJECT, active=1, public=1,
         notes="SECJ3343 Project 1 - test case design for TaskFlow. Each tester authors their own suites.")
    plan = next(t for t in call("getProjectTestPlans", testprojectid=PID) if t["name"] == PLAN)
TPID = int(plan["id"])
builds = call("getBuildsForTestPlan", testplanid=TPID) or []
if not any(isinstance(b, dict) and b.get("name") == BUILD for b in builds):
    call("createBuild", testplanid=TPID, buildname=BUILD,
         buildnotes=p(f"{REPO} main branch, source baseline {SOURCE_COMMIT}. Test design only; no execution results claimed."))
for ext in created:
    tc = call("getTestCase", testcaseexternalid=ext)[0]
    linked = sql(f"SELECT 1 FROM testplan_tcversions p JOIN tcversions v ON v.id=p.tcversion_id WHERE p.testplan_id={TPID} AND v.tc_external_id={int(ext.split('-')[-1])}")
    if not linked:
        call("addTestCaseToTestPlan", testprojectid=PID, testplanid=TPID, testcaseexternalid=ext, version=int(tc["version"]))
    call("assignTestCaseExecutionTask", testplanid=TPID, testcaseexternalid=ext, user=AUTHOR, buildname=BUILD)
print(f"done: {len(created)} test cases, plan {TPID}")
