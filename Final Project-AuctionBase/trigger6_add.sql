--15. All new bids must be placed at the time which matches the current time of your AutionBase system.
PRAGMA foreign_key = ON;
drop trigger if exists trigger6;
create trigger trigger6
before insert on Bids
for each row
    when exists (
        SELECT *
        FROM CurrentTime
        WHERE new.time <> CurrentTime.time
)
begin
    SELECT raise(rollback,'All new bids must be placed at the time which matches the current time of the AutionBase system.');
end;
