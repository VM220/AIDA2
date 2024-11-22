:- use_module(library(http/http_server)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_files)).
:- use_module(library(csv)).

% Declare the dynamic predicate to store student data
:- dynamic student/3.

% Load CSV data at startup
:- initialization(load_student_data).

load_student_data :-
    csv_read_file('data.csv', Rows, [functor(student), arity(3)]),
    % Filter out the header row if it exists
    exclude(is_header, Rows, CleanRows),
    maplist(assert, CleanRows).

% Helper predicate to identify the header row
is_header(student('student_id', 'attendance_percentage', 'cgpa')).

% Define HTTP routes
:- http_handler(root(scholarship), handle_scholarship_check, []).
:- http_handler(root(exam), handle_exam_permission, []).

% Serve static files
:- http_handler(root(.), http_reply_from_files('./www', []), [prefix]).

% API endpoint to verify scholarship eligibility
handle_scholarship_check(Request) :-
    http_read_json_dict(Request, Dict),
    student_id(Dict, ID),
    ( scholarship_eligible(ID) ->
        Response = _{student_id: ID, scholarship_eligible: true}
    ; Response = _{student_id: ID, scholarship_eligible: false} ),
    reply_json_dict(Response).

% API endpoint to verify exam eligibility
handle_exam_permission(Request) :-
    http_read_json_dict(Request, Dict),
    student_id(Dict, ID),
    ( can_take_exam(ID) ->
        Response = _{student_id: ID, exam_permitted: true}
    ; Response = _{student_id: ID, exam_permitted: false} ),
    reply_json_dict(Response).

% Helper predicate to extract student_id from JSON dictionary
student_id(Dict, ID) :-
    get_dict(student_id, Dict, ID).


% Rule for scholarship eligibility
scholarship_eligible(ID) :-
    student(ID, Attendance, CGPA),
    number(Attendance), number(CGPA), % Validate as numeric
    Attendance >= 75,
    CGPA >= 9.0.

% Rule for exam eligibility
can_take_exam(ID) :-
    student(ID, Attendance, _),
    number(Attendance), % Validate as numeric
    Attendance >= 75.

% Start the HTTP server
:- initialization(http_server(http_dispatch, [port(8081)])).
