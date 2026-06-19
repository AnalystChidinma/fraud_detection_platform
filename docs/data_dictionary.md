# Data Dictionary

| Column Name    | Description                                                | Data Type |
| -------------- | ---------------------------------------------------------- | --------- |
| step           | Represents a unit of time in the simulation                | Integer   |
| type           | Transaction type                                           | String    |
| amount         | Transaction amount                                         | Decimal   |
| nameOrig       | Sender account identifier                                  | String    |
| oldbalanceOrg  | Sender balance before transaction                          | Decimal   |
| newbalanceOrig | Sender balance after transaction                           | Decimal   |
| nameDest       | Receiver account identifier                                | String    |
| oldbalanceDest | Receiver balance before transaction                        | Decimal   |
| newbalanceDest | Receiver balance after transaction                         | Decimal   |
| isFraud        | Indicates whether transaction is fraudulent (1) or not (0) | Integer   |
| isFlaggedFraud | Indicates whether transaction was flagged by the system    | Integer   |
