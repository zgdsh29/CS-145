--14.Any new bid for a particular item must have a higher amount than any of the previous bid for that particular item.
PRAGMA foreign_key = ON;
drop trigger if exists trigger5;
create trigger trigger5
before insert on Bids
for each row
    when exists(
         SELECT *
         FROM Items
         WHERE Items.item_id = new.item_id
            AND new.amount < Items.currently
)
begin
        SELECT raise (rollback, 'Any new bid for a particular item must have a higher amount than any of the previous bid for that particular item.');
end;
