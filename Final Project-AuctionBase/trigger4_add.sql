--13. In every aution, the Number_of_Bids attribute corresponds to the actual number of bids for that particular item.
PRAGMA foreign_key = ON;
drop trigger if exists trigger4;
create trigger trigger4
after insert on Bids
for each row
begin
    update Items
    set number_of_bids = number_of_bids + 1
    where item_id = new.item_id;
end;
