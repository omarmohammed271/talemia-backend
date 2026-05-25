"""
SQL queries — one per dashboard.
Each returns: { "cards": {...}, "charts": {...} }
"""

# ── Dashboard 1 — BD Executive ─────────────────────────────────
DASHBOARD_1 = """
SELECT
    JSON_BUILD_OBJECT(
        'open_ytd',               (SELECT open_ytd               FROM gold.d1_cards),
        'total_opportunities',    (SELECT total_opportunities    FROM gold.d1_cards),
        'closed',                 (SELECT closed                 FROM gold.d1_cards),
        'won_count',              (SELECT won_count              FROM gold.d1_cards),
        'lost_count',             (SELECT lost_count             FROM gold.d1_cards),
        'pipeline_value_sar',     (SELECT pipeline_value_sar     FROM gold.d1_cards),
        'weighted_pipeline_sar',  (SELECT weighted_pipeline_sar  FROM gold.d1_cards),
        'won_value_sar',          (SELECT won_value_sar          FROM gold.d1_cards),
        'lost_value_sar',         (SELECT lost_value_sar         FROM gold.d1_cards),
        'value_of_lost_bids_sar', (SELECT value_of_lost_bids_sar FROM gold.d1_cards),
        'win_rate_pct',           (SELECT win_rate_pct           FROM gold.d1_cards),
        'hit_rate_pct',           (SELECT hit_rate_pct           FROM gold.d1_cards),
        'total_meetings',         (SELECT total_meetings         FROM gold.d1_cards),
        'avg_sales_cycle_days',   (SELECT avg_sales_cycle_days   FROM gold.d1_cards),
        'high_likelihood_count',  (SELECT high_likelihood_count  FROM gold.d1_cards),
        'mid_likelihood_count',   (SELECT mid_likelihood_count   FROM gold.d1_cards),
        'low_likelihood_count',   (SELECT low_likelihood_count   FROM gold.d1_cards)
    ) AS cards,
    JSON_BUILD_OBJECT(
        'opportunities_stage', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count)
                            ORDER BY count DESC)
            FROM gold.d1_opportunities_stage
        ),
        'pipeline_by_value', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count, 'pct', pct)
                            ORDER BY count DESC)
            FROM gold.d1_pipeline_by_value
        ),
        'win_loss_ratio', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT(
                'label', label, 'count', count, 'value_sar', value_sar, 'pct', pct))
            FROM gold.d1_win_loss_ratio
        ),
        'opportunity_pipeline_breakdown', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count)
                            ORDER BY count DESC)
            FROM gold.d1_opportunity_pipeline_breakdown
        )
    ) AS charts
"""

# ── Dashboard 2 — Financials ───────────────────────────────────
DASHBOARD_2 = """
SELECT
    JSON_BUILD_OBJECT(
        'pipeline_value_sar',          (SELECT pipeline_value_sar          FROM gold.d2_cards),
        'weighted_pipeline_value_sar', (SELECT weighted_pipeline_value_sar FROM gold.d2_cards),
        'won_value_sar',               (SELECT won_value_sar               FROM gold.d2_cards),
        'lost_value_sar',              (SELECT lost_value_sar              FROM gold.d2_cards),
        'total_closed_value_sar',      (SELECT total_closed_value_sar      FROM gold.d2_cards),
        'win_rate_pct',                (SELECT win_rate_pct                FROM gold.d2_cards),
        'won_count',                   (SELECT won_count                   FROM gold.d2_cards),
        'lost_count',                  (SELECT lost_count                  FROM gold.d2_cards)
    ) AS cards,
    JSON_BUILD_OBJECT(
        'pipeline_funnel_by_business_line', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT(
                'label', label, 'won_count', won_count, 'total_value_sar', total_value_sar)
                ORDER BY total_value_sar DESC)
            FROM gold.d2_pipeline_funnel_by_business_line
        ),
        'top_opportunities_by_value', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT(
                'opportunity_id',    opportunity_id,
                'name_en',           name_en,
                'client_name_en',    client_name_en,
                'business_line_en',  business_line_en,
                'contract_value_sar',contract_value_sar,
                'bd_owner_en',       bd_owner_en)
                ORDER BY contract_value_sar DESC)
            FROM gold.d2_top_opportunities_by_value
        )
    ) AS charts
"""

# ── Dashboard 3 — Business Line ────────────────────────────────
DASHBOARD_3 = """
SELECT
    JSON_BUILD_OBJECT(
        'total_opportunities', (SELECT total_opportunities FROM gold.d3_cards),
        'new_opportunities',   (SELECT new_opportunities   FROM gold.d3_cards),
        'open_opportunities',  (SELECT open_opportunities  FROM gold.d3_cards),
        'won_count',           (SELECT won_count           FROM gold.d3_cards),
        'lost_count',          (SELECT lost_count          FROM gold.d3_cards),
        'win_rate_pct',        (SELECT win_rate_pct        FROM gold.d3_cards)
    ) AS cards,
    JSON_BUILD_OBJECT(
        'win_loss_ratio', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'pct', pct))
            FROM gold.d3_win_loss_ratio
        ),
        'number_of_opportunities_lost_by_business_line', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count)
                            ORDER BY count DESC)
            FROM gold.d3_number_of_opportunities_lost_by_business_line
        ),
        'win_loss_by_business_line', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'won', won, 'lost', lost)
                            ORDER BY won DESC)
            FROM gold.d3_win_loss_by_business_line
        ),
        'opportunity_status_distribution', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count, 'pct', pct)
                            ORDER BY count DESC)
            FROM gold.d3_opportunity_status_distribution
        )
    ) AS charts
"""

# ── Dashboard 4 — Account Manager ─────────────────────────────
DASHBOARD_4 = """
SELECT
    JSON_BUILD_OBJECT(
        'account_managers',      (SELECT account_managers      FROM gold.d4_cards),
        'total_clients_managed', (SELECT total_clients_managed FROM gold.d4_cards),
        'total_opportunities',   (SELECT total_opportunities   FROM gold.d4_cards),
        'qualified_value_sar',   (SELECT qualified_value_sar   FROM gold.d4_cards),
        'meetings',              (SELECT meetings              FROM gold.d4_cards),
        'total_proposals',       (SELECT total_proposals       FROM gold.d4_cards),
        'win_rate_pct',          (SELECT win_rate_pct          FROM gold.d4_cards)
    ) AS cards,
    JSON_BUILD_OBJECT(
        'live_opportunities', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count, 'pct', pct))
            FROM gold.d4_live_opportunities
        ),
        'win_ratio_by_account_manager', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT(
                'bd_owner', bd_owner, 'won_count', won_count,
                'lost_count', lost_count, 'total_count', total_count,
                'win_rate_pct', win_rate_pct, 'total_value_won', total_value_won)
                ORDER BY win_rate_pct DESC)
            FROM gold.d4_win_ratio_by_account_manager
        ),
        'top_clients_by_value', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'total_won_value_sar', total_won_value_sar)
                            ORDER BY total_won_value_sar DESC)
            FROM gold.d4_top_clients_by_value
        ),
        'winning_likelihood', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count))
            FROM gold.d4_winning_likelihood
        ),
        'current_vs_new_client', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count, 'pct', pct))
            FROM gold.d4_current_vs_new_client
        )
    ) AS charts
"""

# ── Dashboard 5 — Commercial ───────────────────────────────────
# ── Dashboard 5 — Commercial ───────────────────────────────────
DASHBOARD_5 = """
SELECT
    JSON_BUILD_OBJECT(
        'opportunities',           (SELECT opportunities           FROM gold.d5_cards),
        'total_clients',           (SELECT total_clients           FROM gold.d5_cards),
        'winning_pct',             (SELECT winning_pct             FROM gold.d5_cards),
        'current_clients',         (SELECT current_clients         FROM gold.d5_cards),
        'next_30_days_deadlines',  (SELECT next_30_days_deadlines  FROM gold.d5_cards),
        'avg_sales_cycle_days',    (SELECT avg_sales_cycle_days    FROM gold.d5_cards)
    ) AS cards,
    JSON_BUILD_OBJECT(
        'top_client_by_value', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'won_value_sar', won_value_sar)
                            ORDER BY won_value_sar DESC)
            FROM gold.d5_top_client_by_value
        ),
        'opportunity_stage', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count)
                            ORDER BY count DESC)
            FROM gold.d5_opportunity_stage
        ),
        'expected_award_date', (
            SELECT COALESCE(
                JSON_AGG(JSON_BUILD_OBJECT(
                    'label', t.label::text,
                    'count', t.count::int
                ) ORDER BY t.label),
                '[]'::json
            )
            FROM (
                SELECT col.column_name
                FROM information_schema.columns col
                WHERE col.table_schema = 'gold'
                  AND col.table_name = 'd5_expected_award_date'
                  AND col.column_name = 'label'
            ) has_label
            CROSS JOIN gold.d5_expected_award_date t
        ),
        'opportunity_business_line', (
            SELECT JSON_AGG(JSON_BUILD_OBJECT('label', label, 'count', count)
                            ORDER BY count DESC)
            FROM gold.d5_opportunity_business_line
        )
    ) AS charts
"""

# ── Dashboard 6 — Opportunity Details ─────────────────────────
DASHBOARD_6_ALL = """
SELECT
    opportunity_id, name_en, name_ar, status,
    client_name_en, business_line_en, bd_owner_en, bl_owner_en,
    stage, winning_likelihood, win_lose,
    deal_type, horizon, priority, sector,
    client_type, go_no_go, period_years,
    contract_value_actual, contract_value_plan,
    sales_cycle_days, meetings_count,
    tier, gate, checkpoint,
    expected_award_date, year, weekly_update_en
FROM gold.d6_opportunity_details
{where_clause}
ORDER BY contract_value_actual DESC NULLS LAST
"""

DASHBOARD_6_SINGLE = """
SELECT
    opportunity_id, name_en, name_ar, status,
    client_name_en, business_line_en, bd_owner_en, bl_owner_en,
    stage, winning_likelihood, win_lose,
    deal_type, horizon, priority, sector,
    client_type, go_no_go, period_years,
    contract_value_actual, contract_value_plan,
    sales_cycle_days, meetings_count,
    tier, gate, checkpoint,
    expected_award_date, year, weekly_update_en
FROM gold.d6_opportunity_details
WHERE opportunity_id = %(opportunity_id)s
"""