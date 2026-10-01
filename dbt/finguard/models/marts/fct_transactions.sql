{{
    config(
       materialized='table',
       schema='marts'
    )
}}

SELECT
    i.transaction_key,

    d.transaction_key_type,

    i.transaction_step,
    
    i.origin_account,
    i.destination_account,
    i.amount,

    i.old_balance_origin,
    i.new_balance_origin,
    i.change_in_balance_origin,

    i.old_balance_destination,
    i.new_balance_destination,
    i.change_in_balance_destination,

    i.is_fraud,
    i.is_flagged_fraud,
    i.fraud_amount

    from {{ ref("int_transactions") }} AS i
    left join {{ ref("dim_transaction_type") }} AS d
    on i.transaction_type = d.transaction_type