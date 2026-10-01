    SELECT DISTINCT
        {{
            dbt_utils.generate_surrogate_key(['transaction_type'])

        }} AS transaction_key_type,

        transaction_type

    FROM {{ ref('int_transactions')}}
    