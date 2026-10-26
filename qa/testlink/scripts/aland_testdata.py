"""Original TaskFlow test design by member 1, Aland Karwan. No execution results implied.

The tuples and dictionaries follow the reference toolkit's data format only.
All requirements and cases derive from TaskFlow README/code at main@5133a6c.
"""
from html import escape

AUTHOR = 'aland'
FULL_NAME = 'Aland Karwan'
LETTER = 'A'
TOP_SUITE = 'A - Aland Karwan - Creation and text validation'
TOP_SUITE_DETAILS = (
    '<p>Tester: Aland Karwan. SECJ3343 Project 1. Group TaskFlow. '
    'Baseline: TaskFlow main@5133a6c. Test basis: README.md TF-REQ-001/002/003/007/008 '
    'and the default-only portions of TF-REQ-004/005/006. '
    'Code: src/utils/validation.js, tasks.js; src/components/TaskFormModal.jsx, Modal.jsx; src/App.jsx.</p>'
    '<p>Scope: creation workflow, trimmed Unicode text limits, counters, inline errors, cancel and reopen. '
    'Member C owns enum/date validation and subsequent status changes; B owns editing/deletion; '
    'D owns querying; E owns storage failure/recovery and navigation. '
    'Techniques: EP, BVA, Decision Table, State Transition, Use Case, Error Guessing. '
    'All cases are designed manual tests, initially Not Run.</p>'
    '<p>Use a dedicated Chrome profile at http://localhost:5173. Before EACH independent case '
    'open DevTools Console, run localStorage.removeItem("taskflow_tasks"); '
    'localStorage.removeItem("taskflow_tasks_backup"); location.reload(); '
    'close DevTools. Leave Dashboard, empty search, All Statuses, All Priorities, Newest first. '
    'Unless overridden: title = Write Weekly Report; description empty; priority Medium; status To Do; '
    'due date empty. In literal repetition notation, a x N means exactly N copies of ASCII a, '
    'with no separators. Use the supplied Console copy expressions to put exact data on the clipboard. '
    'Observe toasts immediately (they disappear after 3000 ms). Never clear personal task data.</p>'
)

def requirement(rid, title, rule, source):
    return (rid, title, rule + ' Source: README.md (Requirements traceability / Exact messages / Behaviour notes); ' + source + '; baseline main@5133a6c.')

REQ_SPECS = [{
    'doc_id':'SRS-A-CREATE', 'title':'Task creation and text validation',
    'scope':'README.md TF-REQ-001,002,003,007,008; creation defaults from TF-REQ-004/005/006. '
            'Derived acceptance requirements from implemented behavior; no separate customer SRS exists. '
            'src/components/TaskFormModal.jsx, Modal.jsx; src/utils/validation.js, tasks.js; src/App.jsx.',
    'reqs':[
        requirement('REQ-A-001','Required trimmed title','A blank or whitespace-only title shall show "Title is required." and prevent creation.', 'src/utils/validation.js validateTask; src/components/TaskFormModal.jsx handleSubmit'),
        requirement('REQ-A-002','Title inclusive length boundaries','Trimmed title length shall be 3 through 80 Unicode code points inclusive. Below 3 shows "Title must be at least 3 characters." Above 80 shows "Title must be 80 characters or fewer." Inputs have no maxLength.', 'src/utils/validation.js TITLE_MIN/TITLE_MAX/countChars; src/components/TaskFormModal.jsx'),
        requirement('REQ-A-003','Trim and Unicode normalization','Leading/trailing title and description whitespace shall be removed before counting and saving. Each Unicode code point, including a single emoji, counts as one. Combining sequences consist of multiple code points; no Unicode canonical normalization occurs.', 'src/utils/validation.js countChars/validateTask; src/utils/tasks.js normalizeValues'),
        requirement('REQ-A-004','Optional description maximum','Description may be empty and shall accept up to 500 trimmed Unicode code points. At 501 it shall show "Description must be 500 characters or fewer." and prevent creation.', 'src/utils/validation.js DESCRIPTION_MAX/validateTask; src/components/TaskFormModal.jsx'),
        requirement('REQ-A-005','Live trimmed counters','The title and description counters shall display "n / 80" and "n / 500" using trimmed code point counts. counter-over/red shall apply only when n exceeds the maximum.', 'src/components/TaskFormModal.jsx titleLength/descriptionLength; src/App.css .counter-over'),
        requirement('REQ-A-006','Creation form defaults','Opening "+ New Task" shall show "New Task", blank title/description/date, priority "Medium", status "To Do", "Cancel" and "Create Task". Empty date saves as an empty string.', 'src/components/TaskFormModal.jsx EMPTY_FORM; src/utils/tasks.js normalizeValues'),
        requirement('REQ-A-007','Successful creation and persistence','A valid submission shall close the form, add exactly one task, save it to taskflow_tasks and immediately show "Task created successfully." The saved object has a nonempty generated id and identical valid ISO createdAt/updatedAt on creation.', 'src/App.jsx createTask/commit; src/utils/tasks.js buildTask; src/utils/storage.js saveTasks'),
        requirement('REQ-A-008','All creation values retained','A valid creation shall preserve selected priority/status/date and save trimmed title/description without altering internal spaces or line breaks. Duplicate task titles are allowed and receive distinct ids.', 'src/components/TaskFormModal.jsx handleSubmit; src/utils/tasks.js buildTask/normalizeValues; src/App.jsx createTask'),
        requirement('REQ-A-009','Cancel creation through every close path','Cancel, Close (X), Escape and pressing the dark backdrop shall close New Task and discard unsaved values, without creating or persisting a task or showing a success toast.', 'src/components/TaskFormModal.jsx; src/components/Modal.jsx onKeyDown/onMouseDown/onClose'),
        requirement('REQ-A-010','Fresh creation form on reopen','After dismissal or successful creation, opening New Task again shall use EMPTY_FORM and clear previously displayed validation errors.', 'src/App.jsx conditional TaskFormModal mounting; src/components/TaskFormModal.jsx useState'),
        requirement('REQ-A-011','Error timing and focus','Before the first submit validation errors shall stay hidden. Invalid submit shall keep the modal open, show all relevant field errors, set aria-invalid and focus the first invalid field (title before description).', 'src/components/TaskFormModal.jsx submitted/errors/handleSubmit/invalid'),
        requirement('REQ-A-012','Live recovery after failed submit','After the first failed submit, errors shall update on each edit. Correcting every invalid field shall permit one successful creation on the next submit.', 'src/components/TaskFormModal.jsx handleChange/submitted/handleSubmit'),
        requirement('REQ-A-013','Creation entry points','With no tasks the page shall show "No tasks yet", "Tasks you create will appear here." and "Create your first task". That button shall open the same New Task form as "+ New Task".', 'src/components/TaskList.jsx empty state; src/App.jsx onCreate; src/components/EmptyState.jsx'),
        requirement('REQ-A-014','Safe literal text rendering','Task title and description shall render as literal React text, including HTML-like content, without creating injected markup or executing scripts.', 'src/components/TaskCard.jsx task.title/task.description; src/components/TaskFormModal.jsx controlled values'),
    ]
}]

COMMON = ('Use dedicated Chrome profile; TaskFlow at http://localhost:5173 from main@5133a6c. '
          'Before this case clear only that profile\'s taskflow_tasks and taskflow_tasks_backup keys and reload. '
          'Dashboard; no search/filters; Newest first. Browser storage writable. '
          'Unless specified: Write Weekly Report, empty description/date, Medium, To Do. '
          'Observe toast within 3 seconds. ')

def case(n, title, technique, reqs, steps, pre='', importance=2):
    cid = f'TC-A-{n:03d}'
    return {'id':cid, 'name':cid+' - '+title, 'technique':technique,
            'reqs':reqs.split(), 'pre':COMMON+pre, 'steps':steps, 'importance':importance}

def text_case(n, field, value, count, valid, title, technique, reqs, error=None, clipboard=None):
    label = 'Task Title' if field == 'title' else 'Description'
    maximum = 80 if field == 'title' else 500
    data = repr(value)
    instruction = f'Enter exactly {data} in {label}.'
    if clipboard:
        instruction = f'In Chrome DevTools Console run {clipboard}; close DevTools and paste into {label}.'
    steps = [('+ New Task: click the button.', 'Dialog "New Task" opens with "Create Task" and "Cancel".'),
             ('Set Task Title to Write Weekly Report, then '+instruction, f'{label} counter is "{count} / {maximum}"; '+('counter is red.' if count>maximum else 'counter is not red.'))]
    if valid:
        steps += [('Click Create Task.', 'Dialog closes. Exactly one card appears; toast "Task created successfully." appears.'),
                  ('Reload; inspect taskflow_tasks in DevTools Application > Local Storage.',
                   f'Exactly one task remains. Saved {field} equals {repr(value.strip())}; no surrounding whitespace remains.')]
    else:
        steps += [('Click Create Task.', f'"{error}" appears under {label}; "New Task" stays open.'),
                  ('Inspect localStorage taskflow_tasks and the list after Cancel.', 'No task was saved. "No tasks yet" is shown; no success toast.')]
    return case(n,title,technique,reqs,steps,importance=3)

title_cases=[]
for n, length in enumerate((0,1,2,3,4,79,80,81),1):
    error = 'Title is required.' if length==0 else ('Title must be at least 3 characters.' if length<3 else 'Title must be 80 characters or fewer.')
    title_cases.append(text_case(n,'title','a'*length,length,3<=length<=80,
        f'Title length {length}', ('EP - empty required-title partition' if length==0 else 'EP - below-minimum invalid partition' if length==1 else f'BVA - title length {length}; inclusive bounds 3 and 80'),
        'REQ-A-001 REQ-A-005' if length==0 else 'REQ-A-002 REQ-A-005', error,
        f'copy("a".repeat({length}))'))
title_cases += [text_case(9,'title','     ',0,False,'Whitespace-only title','EP - whitespace-only invalid partition',
    'REQ-A-001 REQ-A-003','Title is required.'),
    text_case(10,'title','  abc  ',3,True,'Trim title before counting and saving','EP - padded valid partition','REQ-A-002 REQ-A-003'),
    text_case(11,'title','  ab  ',2,False,'Padding cannot bypass minimum','BVA - trimmed min-1','REQ-A-002 REQ-A-003','Title must be at least 3 characters.'),
    text_case(12,'title','  '+'a'*80+'  ',80,True,'Padded maximum title','BVA - trimmed max despite 84 raw characters','REQ-A-002 REQ-A-003 REQ-A-005',clipboard='copy("  " + "a".repeat(80) + "  ")')]
for n,length in enumerate((2,3,80,81),13):
    title_cases.append(text_case(n,'title','😀'*length,length,3<=length<=80,
        f'Emoji title {length} code points','BVA - Unicode code points at min-1/min/max/max+1',
        'REQ-A-002 REQ-A-003 REQ-A-005', 'Title must be at least 3 characters.' if length<3 else 'Title must be 80 characters or fewer.',
        f'copy("😀".repeat({length}))'))

description_cases=[]
for n,length in enumerate((0,1,499,500,501),17):
    description_cases.append(text_case(n,'description','d'*length,length,length<=500,
        f'Description length {length}','BVA - optional min 0, min+1, max-1/max/max+1',
        'REQ-A-004 REQ-A-005','Description must be 500 characters or fewer.',f'copy("d".repeat({length}))'))
description_cases += [
    text_case(22,'description','  '+'d'*500+'  ',500,True,'Trim padded description maximum','BVA - trimmed max','REQ-A-003 REQ-A-004 REQ-A-005',clipboard='copy("  " + "d".repeat(500) + "  ")'),
    text_case(23,'description','   \n\t  ',0,True,'Whitespace-only optional description','EP - optional whitespace partition','REQ-A-003 REQ-A-004'),
    text_case(24,'description','😀'*500,500,True,'Emoji description maximum','BVA - 500 code points / 1000 UTF-16 units','REQ-A-003 REQ-A-004 REQ-A-005',clipboard='copy("😀".repeat(500))'),
    text_case(25,'description','😀'*501,501,False,'Emoji description above maximum','BVA - max+1 code points','REQ-A-003 REQ-A-004 REQ-A-005','Description must be 500 characters or fewer.',clipboard='copy("😀".repeat(501))'),
]

workflow_cases = [
    case(26,'Create using default values','Use Case - minimum valid creation','REQ-A-006 REQ-A-007',[
        ('Click + New Task.', '"New Task" has blank text/date, "Medium", "To Do", "0 / 80", "0 / 500", "Cancel" and "Create Task".'),
        ('Enter Write Weekly Report as Task Title; click Create Task.', 'Form closes; card "Write Weekly Report" has "Medium" and "To Do"; toast "Task created successfully.".'),
        ('Inspect saved JSON and reload.', 'One object in taskflow_tasks has title Write Weekly Report, description "", priority Medium, status To Do, dueDate "", nonempty id, valid ISO createdAt equal to updatedAt. Same card remains after reload.')],importance=3),
    case(27,'Create with every field supplied','Use Case - complete valid creation','REQ-A-007 REQ-A-008',[
        ('Open New Task; enter title "  Plan sprint  ", description "  Agenda\n  keep two spaces  ", choose High, In Progress, due date 2028-02-29.', 'Form displays entered values and "High", "In Progress".'),
        ('Click Create Task and inspect stored JSON.', 'Toast "Task created successfully."; one task has title "Plan sprint", description "Agenda\n  keep two spaces", High, In Progress and "2028-02-29".'),
        ('Reload.', 'Card "Plan sprint" remains with "High", "In Progress" and "Due: Feb 29, 2028".')]),
]
for n,(action,label) in enumerate((('Click Cancel.','Cancel'),('Click the X button labelled Close.','Close X'),('Press Escape.','Escape'),('Press and release on the dark backdrop outside the white dialog.','Backdrop')),28):
    workflow_cases.append(case(n,'Discard creation via '+label,'State Transition - draft to discarded','REQ-A-009 REQ-A-010',[
        ('Open New Task; enter Unsaved draft and description Must disappear.', 'Draft is visible in "New Task"; no task saved yet.'),
        (action, 'Dialog closes; "No tasks yet" remains; no "Task created successfully." toast.'),
        ('Open New Task again and inspect localStorage.', 'Title, description and date are blank; Medium, To Do; no errors; no saved task.')]))
workflow_cases += [
    case(32,'Validation appears only after submit','State Transition - pristine to submitted invalid','REQ-A-011',[
        ('Open New Task; type ab in Task Title without submitting.', 'Counter "2 / 80"; no "Title must be at least 3 characters." message yet; title aria-invalid="false".'),
        ('Click Create Task.', '"Title must be at least 3 characters." appears; title aria-invalid="true"; focus returns to Task Title; modal remains; no task saved.')]),
    case(33,'Correct invalid title without resubmitting','State Transition - invalid to corrected to saved','REQ-A-011 REQ-A-012',[
        ('Open New Task; submit empty form.', '"Title is required." appears, title focused; no task saved.'),
        ('Type ab, then abc without clicking Create Task.', 'At ab: "Title must be at least 3 characters.". At abc: title error disappears immediately and aria-invalid="false".'),
        ('Click Create Task.', 'Exactly one abc card saved; "Task created successfully."; modal closes.')]),
    case(34,'Simultaneous text errors and first-invalid focus','Decision Table - title invalid AND description invalid','REQ-A-002 REQ-A-004 REQ-A-011 REQ-A-012',[
        ('Open New Task; title ab; paste 501 d characters using Console copy("d".repeat(501)); click Create Task.', 'Both "Title must be at least 3 characters." and "Description must be 500 characters or fewer." appear; focus is Task Title; no save.'),
        ('Change title to abc and click Create Task.', 'Title error clears; description error remains; focus is Description; no save.'),
        ('Remove one d (500 remain); click Create Task.', 'Description error clears; "Task created successfully."; exactly one abc task saved.')],importance=3),
    case(35,'Fresh form after successful creation','State Transition - saved to fresh draft','REQ-A-007 REQ-A-010',[
        ('Create Write Weekly Report with default fields.', '"Task created successfully." and one Write Weekly Report card.'),
        ('Open + New Task.', '"New Task" shows blank title/description/date, Medium and To Do; counters "0 / 80" and "0 / 500"; no errors.'),
        ('Cancel.', 'Exactly the original card remains; no second task.')]),
    case(36,'Duplicate titles have separate identities','EP - duplicate title allowed','REQ-A-007 REQ-A-008',[
        ('Create Write Weekly Report twice, reopening + New Task each time.', 'Each submit closes its dialog with "Task created successfully."; two cards share title Write Weekly Report.'),
        ('Inspect taskflow_tasks and reload.', 'Two objects have distinct nonempty ids; both title values equal Write Weekly Report; both cards remain.')]),
    case(37,'Empty-state creation entry point','Use Case - first-task entry','REQ-A-013 REQ-A-006',[
        ('Load clean app.', '"No tasks yet", "Tasks you create will appear here." and "Create your first task" appear.'),
        ('Click Create your first task.', 'Same "New Task" form with blank fields, Medium, To Do and "Create Task".'),
        ('Enter First task; click Create Task.', '"First task" card replaces empty state; "Task created successfully.".')]),
    case(38,'Markup-like text stays literal','Error Guessing - HTML/script text injection','REQ-A-014 REQ-A-007',[
        ('Open New Task; title <b>Report</b>; description <img src=x onerror=alert(1)>; submit.', 'Toast "Task created successfully."; card visibly displays literal "<b>Report</b>" and "<img src=x onerror=alert(1)>"; no alert.'),
        ('Inspect the card DOM and reload.', 'No b or img child element from those strings; content remains literal after reload; no script runs.')]),
    case(39,'Internal spaces and newlines preserved','EP - internal whitespace valid partition','REQ-A-003 REQ-A-008',[
        ('Create title "  Plan  sprint  " and description "  Line one\nLine two  ".', '"Task created successfully."; card title "Plan  sprint".'),
        ('Inspect saved JSON.', 'title equals "Plan  sprint" with two internal spaces. description equals "Line one\nLine two". Surrounding spaces removed; newline retained.')]),
    case(40,'Clicks inside dialog do not cancel draft','Error Guessing - backdrop target discrimination','REQ-A-009',[
        ('Open New Task; type Keep draft; click the New Task heading and empty padding inside the white dialog.', 'Dialog remains open with Keep draft; no save or toast.'),
        ('Click Create Task.', '"Task created successfully."; exactly one Keep draft card.')]),
    case(41,'Fresh validation state after cancelling errors','State Transition - invalid to dismissed to pristine','REQ-A-010 REQ-A-011',[
        ('Open New Task; submit empty title; click Cancel.', '"Title is required." appears before Cancel; then dialog closes without saving.'),
        ('Reopen New Task.', 'Blank title; "0 / 80"; no "Title is required." message and aria-invalid="false".'),
        ('Cancel.', '"No tasks yet" remains.')]),
    case(42,'Counter returns from over-limit state','BVA - max+1 to max for both text fields','REQ-A-005 REQ-A-012',[
        ('Open New Task; paste 81 a characters and 501 d characters using copy("a".repeat(81)) and copy("d".repeat(501)); submit.', 'Counters "81 / 80", "501 / 500" are red; both length errors appear; no save.'),
        ('Remove one character from each field.', 'Counters "80 / 80", "500 / 500" are not red; both errors disappear immediately.'),
        ('Click Create Task.', '"Task created successfully."; one saved task has 80-character title and 500-character description.')]),
    case(43,'Combining sequence is counted as code points','BVA - Unicode min-1 and min without canonical normalization','REQ-A-002 REQ-A-003 REQ-A-005',[
        ('Open New Task; use DevTools copy("e\\u0301") and paste as title; submit.', 'Title visually resembles accented e but counter is "2 / 80"; "Title must be at least 3 characters."; no save.'),
        ('Append x to title.', 'Counter "3 / 80"; error clears live.'),
        ('Click Create Task; inspect JSON.', '"Task created successfully."; stored title is e + U+0301 + x, three code points with no canonical normalization.')]),
]

SUITES = [
    {'name':'TS-A1 - Required title and Unicode boundaries','details':'Title EP and BVA: 0,1,2,3,4,79,80,81; padding and emoji.','cases':title_cases},
    {'name':'TS-A2 - Description limits and live counters','details':'Optional description EP and BVA: 0,1,499,500,501; padded and emoji data.','cases':description_cases},
    {'name':'TS-A3 - Creation, cancellation and error recovery','details':'Creation use cases, draft state transitions, decision table and error guessing.','cases':workflow_cases},
]
