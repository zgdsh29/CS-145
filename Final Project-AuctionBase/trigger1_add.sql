--8. The Current_Price of an item must always match the Amount of the most recent bid for that item.
PRAGMA foreign_keys= ON;
drop trigger if exists trigger1;
create trigger trigger1
after insert on bids
for each row
begin
    update items
    set currently = new.amount
    where new.item_id=item_id;
end;
