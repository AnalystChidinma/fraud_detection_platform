{{
    config(
        materialized='view',
        schema='INTERMEDIATE'
    )
}}

SELECT

    {{
        dbt_utils.generate_surrogate_key([
            'transaction_step',
            'origin_account',
            'destination_account',
            'amount'
        ])
    }} AS transaction_key,

    transaction_step,
    transaction_type,
    origin_account,
    destination_account,
    amount,

    old_balance_origin,
    new_balance_origin,
    new_balance_origin - old_balance_origin AS change_in_balance_origin,

    old_balance_destination,
    new_balance_destination,
    new_balance_destination - old_balance_destination AS change_in_balance_destination,

    is_fraud,
    is_flagged_fraud,

    CASE
        WHEN is_fraud = 1 THEN amount
        ELSE 0
    END AS fraud_amount

FROM {{ ref('stg_transactions') }}