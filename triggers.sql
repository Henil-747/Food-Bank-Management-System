DELIMITER //
create trigger grain_pulses_produced after insert on food_bank
for each row
begin
	if new.ITEM_TYPE='GRAIN' then
		insert into grain values(new.ITEM_NAME,new.QUANTITY);
	end if;
    if new.ITEM_TYPE='PULSES' then
		insert into pulses values(new.ITEM_NAME,new.QUANTITY);
	end if;
    
    if new.ITEM_TYPE='PRODUCED' then
		insert into produced values(new.ITEM_NAME,new.QUANTITY);
	end if;
end;
//
DELIMITER ;


DELIMITER //
create trigger food_bank_update_insert after insert on donation
for each row
begin 
	declare done int;
    declare temp int;
    declare c_food_bank cursor for select QUANTITY from food_bank where ITEM_TYPE=new.ITEM_TYPE and ITEM_NAME=new.ITEM_NAME;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    open c_food_bank;
    fetch c_food_bank into temp;
    if done then
		insert into food_bank values(new.ITEM_TYPE,new.ITEM_NAME,new.QUANTITY);
    else
		update food_bank set QUANTITY=new.QUANTITY+temp where ITEM_TYPE=new.ITEM_TYPE and ITEM_NAME=new.ITEM_NAME;
		if(new.Item_TYPE='GRAIN') then
			update grain set QUANTITY=new.QUANTITY+temp where ITEM_NAME=new.ITEM_NAME;
		end if;
        if(new.Item_TYPE='PULSES') then
			update pulses set QUANTITY=new.QUANTITY+temp where ITEM_NAME=new.ITEM_NAME;
		end if;
        if(new.Item_TYPE='PRODUCED') then
			update produced set QUANTITY=new.QUANTITY+temp where ITEM_NAME=new.ITEM_NAME;
        end if;
    end if;
    close c_food_bank;
end;
//
DELIMITER ;


DELIMITER //
create trigger food_bank_update_delete after insert on donated
for each row
begin 
	declare done int default false;
    declare temp int;
    declare c_food_bank cursor for select QUANTITY from food_bank where ITEM_TYPE=new.ITEM_TYPE and ITEM_NAME=new.ITEM_NAME;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = true;
    open c_food_bank;
    fetch c_food_bank into temp;
    if not done then
		update food_bank set QUANTITY=temp-new.QUANTITY where ITEM_TYPE=new.ITEM_TYPE and ITEM_NAME=new.ITEM_NAME;
		if(new.Item_TYPE='GRAIN') then
			update grain set QUANTITY=temp-new.QUANTITY where ITEM_NAME=new.ITEM_NAME;
		end if;
        if(new.Item_TYPE='PULSES') then
			update pulses set QUANTITY=temp-new.QUANTITY where ITEM_NAME=new.ITEM_NAME;
		end if;
        if(new.Item_TYPE='PRODUCED') then
			update produced set QUANTITY=temp-new.QUANTITY where ITEM_NAME=new.ITEM_NAME;
        end if;
    end if;
    close c_food_bank;
end;
//
DELIMITER ;


delimiter //
create trigger validate_volunteer before insert on volunteer
for each row
begin
	if new.CONTACT_NO < 0 then
		SIGNAL SQLSTATE
		'45020' SET MESSAGE_TEXT = 'Contact Number can''t be negative';
	end if;
    
    if new.NO_OF_HRS < 0 then
		SIGNAL SQLSTATE
		'45050' SET MESSAGE_TEXT = 'Number of Hours worked can''t be negative';
	end if;
end;
//
delimiter ;


delimiter //
create trigger validate_employee before insert on employee
for each row
begin
	if new.CONTACT_NO < 0 then
		SIGNAL SQLSTATE
		'45020' SET MESSAGE_TEXT = 'Contact Number can''t be negative';
	end if;
    
    if new.CONTACT_NO>0 then
		if length(new.CONTACT_NO) <> 10 then
			SIGNAL SQLSTATE
			'45025' SET MESSAGE_TEXT = 'Contact Number can''t be less than 10 digits';
		end if;
	end if;
    
    if new.SALARY < 0 then
		SIGNAL SQLSTATE
		'45030' SET MESSAGE_TEXT = 'Salary can''t be negative';
	end if;
    
    if new.AADHAR_ID < 0 then
		SIGNAL SQLSTATE
		'45035' SET MESSAGE_TEXT = 'Aadhar ID can''t be negative';
	end if;
    
    if TIMESTAMPDIFF(YEAR, new.JOINING_DATE, new.DOB)<18 then
		SIGNAL SQLSTATE
			'45040' SET MESSAGE_TEXT = 'Employee is under aged to work';
	end if;
end;
//
delimiter ;


delimiter //
create trigger validate_donar before insert on donar
for each row
begin
	if new.CONTACT_NO < 0 then
		SIGNAL SQLSTATE
		'45020' SET MESSAGE_TEXT = 'Contact Number can''t be negative';
	end if;
    if new.AADHAR_ID < 0 then
		SIGNAL SQLSTATE
		'45035' SET MESSAGE_TEXT = 'Aadhar ID can''t be negative';
	end if;
end;
//
delimiter ;


delimiter //
create trigger validate_donee before insert on donee
for each row
begin
	if new.CONTACT_NO < 0 then
		SIGNAL SQLSTATE
		'45020' SET MESSAGE_TEXT = 'Contact Number can''t be negative';
	end if;
    if new.AADHAR_ID < 0 then
		SIGNAL SQLSTATE
		'45035' SET MESSAGE_TEXT = 'Aadhar ID can''t be negative';
	end if;
end;
//
delimiter ;


delimiter //
create trigger qty_check before insert on donated
for each row
begin
	set @qty := (select QUANTITY from food_bank where ITEM_NAME=new.ITEM_NAME and ITEM_TYPE=new.ITEM_TYPE); 
	if new.QUANTITY>0.1*@qty then
		SIGNAL SQLSTATE
		'45000' SET MESSAGE_TEXT = 'You cannot take out more than 10% from the food bank';
	end if;
    if new.QUANTITY<0 then
		SIGNAL SQLSTATE
		'45010' SET MESSAGE_TEXT = 'Quantity cannot be negative';
	end if;
end;
//
delimiter ;


delimiter //
create trigger qty_chk before insert on donation
for each row
begin
    if new.QUANTITY < 0 then
		SIGNAL SQLSTATE
		'45010' SET MESSAGE_TEXT = 'Quantity cannot be negative';
	end if;
end;
//
delimiter ;


delimiter //
create trigger date_donee_contraint before insert on donated
for each row
begin
	set @var_date:=(select DONEE_ID from donated where DONEE_ID = new.DONEE_ID and DONATION_DATE=new.DONATION_DATE);
    if new.DONEE_ID = @var_date then
		SIGNAL SQLSTATE
		'45020' SET MESSAGE_TEXT = 'Same Donee cannot take donation more than once';
	end if;
end;
//
delimiter ;
