--11.No aution may have a bid before its start time or after its end time.
PRAGMA foreign_key = ON;
drop trigger if exists trigger3;
create trigger trigger3
before insert on Bids
for each row
when exists (
     SELECT *
     FROM Items
     WHERE Items.item_id = new.item_id
           AND  (Items.started > new.time OR Items.ends<new.time)
    )
begin
    SELECT raise(rollback, 'No action may have a bid before its start time or after its end time.');
end;
