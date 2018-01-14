rm -f "./category.dat"
rm -f "./users.dat"
rm -f "./bids.dat"
rm -f "./items.dat"

#python my_parser.py /Users/Chris/Desktop/cs145/project3/items-p3.json
#python ./my_parser.py /Users/Chris/Desktop/cs145/project/ebay_data/items-*.json
python my_parser.py /usr/class/cs145/bin/items-p3.json

sort -u "./category.dat" -o "./category.dat"
sort -u "./users.dat" -o "./users.dat"
sort -u "./bids.dat" -o "./bids.dat"
sort -u "./items.dat" -o "./items.dat"


