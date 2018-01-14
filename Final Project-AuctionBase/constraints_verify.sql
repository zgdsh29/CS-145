PRAGMA foreign_keys = ON;
--2. All seller and bidders must already exist as users.
SELECT seller_id
FROM   Items
WHERE  seller_id NOT IN
(
         SELECT user_id
         FROM Users
);

SELECT user_id
FROM   Bids
WHERE  user_id NOT IN
(
        SELECT user_id
        FROM   Users
);

--4. Every bid must correspond to an actual item.
SELECT item_id
FROM   Bids
WHERE  item_id NOT IN
(
    SELECT i.item_id
    FROM Items i
);

--5. The items for a given category must all exist.
SELECT item_id
FROM Categories
WHERE item_id NOT IN
(
    SELECT i.item_id
    From Items i
);








