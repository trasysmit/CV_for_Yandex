with GOOD_DEALS as (
     select /*+materialize */ *
     from fct_deal deal
     where 1=1
           and deal.dealtype in (5, 7, 51, 71,  52, 72) --Кредиты, транши, оведрафты, кредитные линии 
           and lower(deal.code) not like '%#тех%'
           and lower(deal.code) not like '%#тex%' -- Используются латинские буквы 'ex'
           and lower(deal.code) not like '%#теx%' -- Используется латинская буква 'x'
           and not exists ( 
               select *
               from ass_fct_deal ass_deal
               inner join det_type_deal_rel deal_rel
                     on ass_deal.id_type_deal_rel = deal_rel.id_type_deal_rel --Не накладываем условие на актуальность связи, так как есть связи из будущего (dt_open > sysdate)
               join set_dwh_dic_val dic
                     on dic.src_val = deal_rel.code
                     and dic.src_table = 'DET_TYPE_DEAl_REL'
                     and dic.src_column = 'CODE'
               where 1=1
                     and dic.target_val in ('Version', 'FANTOM', 'Prolongation')
                     and ass_deal.id_child = deal.id_deal
                )
),

DATE_CLOSE as (
     select /*+materialize */
          i.id_deal,
          i.date_value AS FACT_END_DT
     from fct_deal_indicator i
     join det_deal_typeattr t
          on i.id_deal_attr = t.id_deal_typeattr
     join set_dwh_dic_val dic
          on dic.src_val = regexp_substr(t.code, '[^#]+', 1, 4)
          and dic.src_table = 'DET_DEAL_TYPEATTR'
          and dic.src_column = 'CODE'
     where 1=1
          and dic.target_val = 'Дата фактического закрытия договора'
          and %DWH_LOAD_DATE% between i.dt_open and i.dt_close
          and %DWH_LOAD_DATE% between t.dt_open and t.dt_close
),

GOOD_DEALS_WITH_CD as (
    select /*+materialize use_hash(a b) */ *
    from good_deals a
    left join date_close b
        on a.id_deal = b.id_deal
    where a.begindate < b.fact_end_dt
        or b.fact_end_dt is null
),

ASS_DEAL as (
     select /*+materialize use_hash(ass_deal deal_rel) */
            ass_deal.id_parent,
            ass_deal.id_child,
            dic.target_val as code,
            deal_rel.name,
            ass_deal.dt_open,
            ass_deal.dt_close,
            row_number() over (partition by ass_deal.id_parent, ass_deal.id_child, dic.src_val order by ass_deal.dt_open desc) as rn --На всякий случай
     from ass_fct_deal ass_deal
     left join det_type_deal_rel deal_rel
          on 1=1 
            and ass_deal.id_type_deal_rel = deal_rel.id_type_deal_rel
            and %DWH_LOAD_DATE% between deal_rel.dt_open and deal_rel.dt_close
     left join set_dwh_dic_val dic
         on dic.src_val = deal_rel.code
         and dic.src_table = ‘DET_TYPE_DEAl_REL’
         and dic.src_column = ‘CODE’
     where 1=1
            and %DWH_LOAD_DATE% between ass_deal.dt_open and ass_deal.dt_close
),

CRED_PARENT as (
     select /*+materialize use_hash(deal ass_deal_cred_line) */
          deal.*,
          ass_deal_cred_line.id_parent as cred_line_parent_id
     from good_deals_with_cd deal
     left join ass_deal ass_deal_cred_line
          on 1=1
             and deal.id_deal = ass_deal_cred_line.id_child
             and ass_deal_cred_line.code = 'CreditLine'
             and ass_deal_cred_line.rn = 1
),

PROLONG_DEALS as (
     select /*+materialize use_hash(ass_deal deal) */
          ass_deal.id_parent as id_deal,
          deal.enddate as plan_end_dt,
          row_number() over(partition by ass_deal.id_parent order by ass_deal.dt_open desc) as rn
     from ass_deal
     join fct_deal deal
          on 1=1 
             and ass_deal.id_child = deal.id_deal
             and ass_deal.rn = 1
             and ass_deal.target_val = 'Prolongation'
),

CRED_CARD_LIST as (
     select
          distinct ass_deal.id_child
     from ass_deal ass_deal
     where 1=1
          and ass_deal.target_val = 'CreditPlastic'
          and ass_deal.rn = 1
)


select /*+use_hash(deal s_ass s_ass_par plong_deal migrat_initial cred_card) */
  deal.id_deal as dwh_agreem_id,
  s_ass.row_id as siebel_agreem_id,
  deal.id_subject as dwh_subject_id,
  deal.code as src_stm_agreem_cd,
  deal.begindate as start_dt,
  nvl(plong_deal.plan_end_dt, deal.enddate) as plan_end_dt,
  good_deals_with_cd.fact_end_dt as fact_end_dt,
  deal.dealtype as dealtype,
  deal.docnum as docnum,
  deal.cred_line_parent_id as parent_id,
  s_ass_par.row_id as siebel_parent_id,
  migrat_initial.dt_open as migrate_dt,
  migrat_initial.id_deal_cur as migrate_next_id,
  nvl(migrat_initial.parent_id_deal, deal.id_deal) as migrate_initial_id
from cred_parent deal
left join s_asset s_ass --Идентификатор из Siebel
     on deal.id_deal = s_ass.integration_id
left join s_asset s_ass_par --Идентификатор  из Siebel для родительского договора
     on deal.cred_line_parent_id = a_ass_par.integration_id
left join prolong_deals plong_deal --Пролонгации 
     on 1=1
        and deal.id_deal = plong_deal.id_deal
        and plong_deal.rn = 1
left join agg_deal_migration migrat_initial --Миграции, первоначальная сделка
     on deal.id_deal = migrat_initial.src_id_deal
left join cred_card_list cred_card --Кредитные карты
     on cred_card.id_child = deal.id_deal