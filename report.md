# SuperPy - report

_( Winc Academy assignment )_

During the work on this assignment, a few problems occurred. In this report I will highlight 3 of them.

---
## The case of the unique ID's
To create an unique id, one could count the amount of rows in a csv file and add an 1 to it. But what if a row is removed? Then there is a possibility for the presents of two ID's who aren't unique. Another thing is that I also wanted the ID's to be unique in relation with all the csv files, to give some info on when they where created and a standard format. So for example: A product has an ID starting with the character P followed by a dot, followed by the date it was created without dashes, followed by a number 1 higher then the highest number of that month. Every month the count starts over. _Example: P.20210407.00001_  (Module: app-data.py Class: ReadWriteCSV method: create_record_id )

---
## The case of the expiration dates
When selling a product, it is legally not allowed to sell products which are expired. So before we even have the ability to sell the product it must be removed from the supermarkets stock, rather then telling the customer, when buying an expired product, you can't sell it because of the expiration date. So every time before receiving the commands from the CLI, the stock will be cleared from expired products. (Module: actions.py Function: update_stock) 

---
## The case of the valuta notation
To convert a floating point number to a valuta notation is simply done by using a f-string. But what if we gonna sell this awesome app to another country and what about we purchase beans for 0.00001 per piece.
So i made a function where one can choose the valuta type and amount of decimals whit a minimum of 2. (Module: helpers.py Function: valuta_notation)
