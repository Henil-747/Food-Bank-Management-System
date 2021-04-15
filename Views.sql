create view emp as select EMPLOYEE_ID, EMPLOYEE_NAME, EMAIL_ID, JOINING_DATE from employee; 
select * from emp;

create view vol as select VOLUNTEER_ID, VOLUNTEER_NAME, EMPLOYEE_ID, NO_OF_HRS from volunteer;
select * from vol;

create view dnr as select EMPLOYEE_ID, DONAR_ID, DONAR_NAME from donar;
select * from dnr;

create view dne as select VOLUNTEER_ID, DONEE_ID, DONEE_NAME from donee;
select * from dne;