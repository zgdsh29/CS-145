--16. The current time of your AuctionBase system can only advance forward in time, not backward in time.
PRAGMA foreign_key = ON;
drop trigger if exists trigger7;
create trigger trigger7
before update on CurrentTime
for each row
    WHEN old.time > new.time
begin
    SELECT raise(rollback, 'The current time of AuctionBase system can only advance forward in time');
end;
