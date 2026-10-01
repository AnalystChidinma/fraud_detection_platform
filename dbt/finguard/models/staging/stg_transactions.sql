SELECT
	STEP AS transaction_step,
	TYPE AS transaction_type,
	AMOUNT AS amount,
	NAMEORIG AS origin_account,
	OLDBALANCEORG AS old_balance_origin,
	NEWBALANCEORIG AS new_balance_origin,
	NAMEDEST AS destination_account,
	OLDBALANCEDEST AS old_balance_destination,
	NEWBALANCEDEST AS new_balance_destination,
	ISFRAUD AS is_fraud,
	ISFLAGGEDFRAUD AS is_flagged_fraud

FROM {{	source('raw', 'transactions') }} 
