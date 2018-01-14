--9. A user may not bid on an item he or she is also selling.
PRAGMA foreign_key= ON;
drop trigger if exists trigger2;
create trigger trigger2
before insert on bids
for each row
    when exists(
         SELECT *
         FROM Items
         WHERE Items.seller_id = new.user_id
            AND Items.item_id  = new.item_id
         )
begin
    SELECT raise(rollback,'A user may not bid on an item he or she is also selling.');
end;
