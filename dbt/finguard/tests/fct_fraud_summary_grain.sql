SELECT
    transaction_step,
    transaction_key_type,
    COUNT(*) AS row_count

FROM {{ ref('fct_fraud_summary') }}

GROUP BY
    transaction_step,
    transaction_key_type

HAVING COUNT(*) > 1