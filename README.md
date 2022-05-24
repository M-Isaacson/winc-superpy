# superpy
Winc Academy assignment

Superpy is a command-line tool that keeps track of the inventory of a supermarket.

--- 
## How to use it?
This tool uses commands to utilize it's base functionality. Additional arguments narrows the outcome. There are 5 commands:

### 1. Advance
This sets the date of the application to a future date or back to the current day. 
0 sets the date to today.
1 sets the date 1 day from now.
etc. 
4 days in the future is the maximum.

_Example:_
```
$ python super.py advance 2
```

### 2. Purchase
A purchase has the following arguments:

- The product name (it's recommended to use the plural form for consistency, for example: 'oranges' in stead of 'orange' )
- The amount purchased from the product.
- The price per piece of the product.
- The expiration date of the batch purchased. This is a dat in ISO fromat ('YYYY-MM-DD')

_Example:_
```
$ python super.py purchase oranges 3000 0.023 2022-04-30
```

### 3. Sell
Sell takes the same arguments as 'purchase', however without the expiration date.

_Example:_
```
$ python super.py sell oranges 320 0.20
```

### 4. Inventory
An overview of the inventory can be narrowed down per product or an overview of all products and can be presented on screen, as csv file or as json file. 

_Example where all products is required:_
```
$ python super.py inventory screen
```
`screen` can be replaced by `csv` or `json`.

_Example where one product is required:_
```
$ python super.py inventory --product oranges screen
```
instead of `--product` one can use `-p`.

### 5. Report
A report gives an overview of purchases or sales. The first argument will be the subject. Will the report about `purchases` or `sales`. Next choose the date range: today, yesterday, a month, a quarter, a year or just a given date. Output can be directed to screen, csv file or json file.

Following examples show the use of all the date ranges.

_Sales of today to screen:_
```
$ python super.py report sales today screen
```

_Sales of yesterday to csv:_
```
$ python super.py report sales yesterday csv
```

_Purchases of february 2022 to json:_
```
$ python super.py report purchases 2022-02 json
```

__Purchases of 2nd quarter of 2021 to screen:_
```
$ python super.py report purchases 2021-2 screen
```

_Purchases of 2020 to csv:_
```
$ python super.py report purchases 2020 csv
```

_Sales of 2022-02-22 to json:_
```
$ python super.py report sales 2022-02-22 json
```

---
## So what about those expiration dates?
Everytime command is given from the command line to the app, the expiration date of all the product are being scanned. The products with overdue expiration dates will be removed from stock automatically.

---
## ID's
All products, purchases and sales have ID's. They are assigned on creation of a row in the application's csv files. Product ID's start with a `P`, purchased with a `B` and sales with a `S`.

---


