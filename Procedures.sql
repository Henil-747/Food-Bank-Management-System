DELIMITER //
create procedure name_search_donar(name varchar(45))
begin
	select * from donar where donar_name like concat('%', name,'%');
end //
DELIMITER ;
call name_search_donar('RAVEL');


DELIMITER //
create procedure name_search_donee(name varchar(45))
begin
	select * from donee where donee_name like concat('%', name,'%');
end //
DELIMITER ;
call name_search_donee('PATEL');

DELIMITER //
create procedure city_search_donar(city varchar(45))
begin
	select * from donar where address like concat('%', city,'%');
end //
DELIMITER ;
call city_search_donar('surat')

DELIMITER //
create procedure disp_volunteers_under_employee(name varchar(45))
begin
    select * from volunteer where employee_id in (select employee_id from employee where employee_name like concat('%', name ,'%'));
end // 
DELIMITER ;
call disp_volunteers_under_employee('shanaya')


DELIMITER //
create procedure donation_date_details(dt date)
begin
	select * from donation where entry_date = dt;
end ;
//
DELIMITER ;
call donation_date_details('2021-04-16');

DELIMITER //
CREATE PROCEDURE donated_date_details(dt date)
begin
	select * from donated where donation_date = dt;
end;
//
DELIMITER ;
call donated_date_details('2021-04-16');


DELIMITER //
CREATE PROCEDURE calc_new_salary()
BEGIN
	update employee set SALARY=SALARY+(0.1*SALARY) where TIMESTAMPDIFF(YEAR, JOINING_DATE, CURDATE())>10;
	select * from employee where TIMESTAMPDIFF(YEAR, JOINING_DATE, CURDATE())>10;
END;
//
DELIMITER ;
call calc_new_salary();

