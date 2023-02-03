create table student
(
    student_id integer primary key autoincrement,
    name       text not null,
    program    text
);

INSERT INTO student (student_id, name, program)
VALUES (1, 'Denis', 'CS');
INSERT INTO student (student_id, name, program)
VALUES (2, 'Alice', 'Science');
INSERT INTO student (student_id, name, program)
VALUES (3, 'Bob', 'Engineering');
INSERT INTO student (student_id, name, program)
VALUES (4, 'Sarah', 'Education');
