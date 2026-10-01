SELECT
    transaction_key_type,
    transaction_step,

    count(*) as total_transactions,
    sum(is_fraud) as fraudulent_transactions,
    sum(amount) as total_transaction_amount,
    sum(fraud_amount) as total_fraud_amount,

    round(
        sum(is_fraud) * 100.0 /NULLIF(count(*),0),
        2
    ) as fraud_rate

FROM {{ ref("fct_transactions")}}

GROUP BY transaction_key_type, transaction_step