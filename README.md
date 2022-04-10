# bearrobotics_simpleATM

* I created a simple ATM deposit/withdrawal program based on sqlite DB.


## DB table details
* first Table : Table of user's card number and encrypted pin number
* second table : A table with accounts and balances linked to card numbers
* third table : A table storing deposit and withdrawal details of the account

## Usage
```python
#Run user controller
python main_controller.py

**************** test ouput ******************

(Press 'c' to exit the program)
Pleas insert your card: 6258400034823441

Please enter the pin number: 12341234

Please select an account to trade
0: {'account': '65270204311367', 'balance': 5606}
1: {'account': '30380204351424', 'balance': 9999}
'p': previous step
Enter the desired account index: 0

seleced account: 65270204311367
(3, 20220410173631.844, 'withdrawal', 15394, None, 5606)
(2, 20220410173627.27, 'deposit', None, 20000, 21000)
(1, 20220410173623.6, 'deposit', None, 1000, 1000)
(0, 20220410172932.54, 'deposit', None, None, 0)
balance : 5606
1 : withdrawal, 2 : deposit
'p': previous step
1

withdrawal amount: 10000

insufficient balance
seleced account: 65270204311367
(3, 20220410173631.844, 'withdrawal', 15394, None, 5606)
(2, 20220410173627.27, 'deposit', None, 20000, 21000)
(1, 20220410173623.6, 'deposit', None, 1000, 1000)
(0, 20220410172932.54, 'deposit', None, None, 0)
balance : 5606
1 : withdrawal, 2 : deposit
'p': previous step
1

withdrawal amount: 5000

transaction success
seleced account: 65270204311367
(4, 20220410091623.81, 'withdrawal', 5000, None, 606)
(3, 20220410173631.844, 'withdrawal', 15394, None, 5606)
(2, 20220410173627.27, 'deposit', None, 20000, 21000)
(1, 20220410173623.6, 'deposit', None, 1000, 1000)
(0, 20220410172932.54, 'deposit', None, None, 0)
balance : 606
1 : withdrawal, 2 : deposit
'p': previous step
2

deposit amount: 20000

transaction success
seleced account: 65270204311367
(5, 20220410091633.855, 'deposit', None, 20000, 20606)
(4, 20220410091623.81, 'withdrawal', 5000, None, 606)
(3, 20220410173631.844, 'withdrawal', 15394, None, 5606)
(2, 20220410173627.27, 'deposit', None, 20000, 21000)
(1, 20220410173623.6, 'deposit', None, 1000, 1000)
(0, 20220410172932.54, 'deposit', None, None, 0)
balance : 20606
1 : withdrawal, 2 : deposit
'p': previous step
p

Please select an account to trade
0: {'account': '65270204311367', 'balance': 20606}
1: {'account': '30380204351424', 'balance': 9999}
'p': previous step
Enter the desired account index: p

(Press 'c' to exit the program)
Pleas insert your card: c

*************************************************
```
```python
#Add user information(already stored in DB)
python create_usr_account.py --card '6258400034823441' --pin '12345678' --name 'Taeho_Jung' --year 29

#Add account information(already stored in DB)
python create_usr_account.py --card '6258400034823441' --account '65270204331637'

#Add user and account information(already stored in DB)
python create_usr_account.py --card '6258400034823441' --pin '12345678' --name 'Taeho_Jung' --year 29 --account '65270204331637'
```

