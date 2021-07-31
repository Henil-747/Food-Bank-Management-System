DELIMITER //
create function max_donation ()
returns varchar(45)
deterministic
begin
	set @name1 = (select donar_name from donar where donar_id = (select DONAR_ID from donation group by DONAR_ID order by sum(quantity) desc limit 1));
    return @name1;
end;
//
DELIMITER ;
select max_donation();


DELIMITER //
create function sum_quantity ()
returns int
deterministic
begin
	set @cnt := (select sum(quantity) from food_bank);
return @cnt;
end;
//
DELIMITER ;
select sum_quantity() total_quantity;



DELIMITER //
create function donated_count (dt date)
returns int
deterministic
begin
	set @cnt := (select count(*) from donated where DONATION_DATE=dt);
return @cnt;
end;
//
DELIMITER ;
select donated_count('2021-04-16');



DELIMITER //
create function donation_count (dt date)
returns int
deterministic
begin
	set @cnt := (select count(*) from donation where ENTRY_DATE=dt);
return @cnt;
end;
//
DELIMITER ;
select donation_count('2021-04-14');


DELIMITER //
create function donor_count (emp_id varchar(20))
returns int
deterministic
begin
	set @cnt := (select count(*) from donar where EMPLOYEE_ID=emp_id);
return @cnt;
end;
//
DELIMITER 
select donor_count('EMP0002');


DELIMITER //
create function max_time_donar ()
returns varchar(45)
deterministic
begin
	set @name1 = (select DONEE_NAME from donee where DONEE_ID = (select DONEE_ID from donated group by DONEE_ID order by count(DONEE_ID) desc limit 1));
    return @name1;
end;
//
DELIMITER ;
select max_time_donar();