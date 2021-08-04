from typing import List
from django.db import connection
from django.contrib.auth.models import User


def sort_user_resource_preferences(user: User) -> List:
    user_resource_preference = []
    with connection.cursor() as cursor:
        cursor.execute(f"""
with get_user_resource_preference as (
    select CMUQA.user_id as user_id
        , CMAMD.resource_type_id as resource_type_id
        , DCT.model as resource_model
        , sum(CMAMD.weight) as total_weight
    from climate_match_userquestionanswer CMUQA
    join climate_match_answer CMA on CMA.id = CMUQA.predefined_answer_id
    join climate_match_answer_answer_metadata CMAAMD on CMAAMD.answer_id = CMA.id
    join climate_match_answermetadata CMAMD on CMAMD.id = CMAAMD.answermetadata_id
    join django_content_type DCT on DCT.id = CMAMD.resource_type_id
    where CMUQA.predefined_answer_id is not null and CMUQA.user_id = {user.id}
    group by 1, 2, 3
    order by total_weight desc
), get_user_skill_preference as (
    select cmu.user_id
        , cma.weight
        , cma.reference_id
        , cma.resource_type_id
        , dct.model
    from climate_match_userquestionanswer cmu
    join climate_match_userquestionanswer_answers cmua on cmua.userquestionanswer_id = cmu.id
    join climate_match_answermetadata cma on cma.id = cmua.answermetadata_id
    join django_content_type dct on dct.id = cma.resource_type_id
    where dct.model = 'skill' and cmu.user_id = {user.id}
), get_user_hub_preference as (
    select cmu.user_id
        , cma.weight
        , cma.reference_id
        , cma.resource_type_id
        , dct.model
    from climate_match_userquestionanswer cmu
    join climate_match_userquestionanswer_answers cmua on cmua.userquestionanswer_id = cmu.id
    join climate_match_answermetadata cma on cma.id = cmua.answermetadata_id
    join django_content_type dct on dct.id = cma.resource_type_id
    where dct.model = 'hub' and cmu.user_id = {user.id}
), get_user_reference_table_relevancy_score_by_skills as (
    select reference_table.table_name, reference_table.id as table_id, sum(gusp.weight) as skill_weight
    from get_user_skill_preference as gusp
    join (
        select op.id, cs.id as skill_id, 'project' as table_name
        from organization_project op
        left join organization_project_skills ops on ops.project_id  = op.id
        left join climateconnect_skill cs on cs.id = ops.skill_id
    ) as reference_table on reference_table.skill_id = gusp.reference_id
    group by 1, 2
), get_user_reference_table_relevancy_score_by_hubs as (
    select reference_table.table_name, reference_table.id as table_id, sum(guhp.weight) as hub_weight
    from get_user_hub_preference as guhp
    join (
        (
            select op.id, hh.id as hub_id, 'project' as table_name
            from hubs_hub hh
            join hubs_hub_filter_parent_tags hhfpt on hhfpt.hub_id = hh.id
            join organization_projecttags optags on optags.id = hhfpt.projecttags_id
                or optags.parent_tag_id = hhfpt.projecttags_id
            join organization_projecttagging opt on opt.project_tag_id = optags.id
                or  opt.project_tag_id  = optags.parent_tag_id
            join organization_project op on op.id = opt.project_id
        ) union (
            select oo.id, hh.id as hub_id, 'organization' as table_name
            from hubs_hub hh
            join organization_organization_hubs ooh on ooh.hub_id = hh.id
            join organization_organization oo on oo.id = ooh.organization_id
        ) union (
            select ii.id, hh.id as hub_id, 'idea' as table_name
            from ideas_idea ii
            join hubs_hub hh on hh.id = ii.hub_id 
        )
    ) as reference_table on reference_table.hub_id = guhp.reference_id
    group by 1, 2
), get_user_reference_relevancy_score as (
    select (
        case when gurtrs.table_id is not null then gurtrs.table_id else gurtrh.table_id end
        ) as table_id
        , (
        case when gurtrs.table_id is not null then gurtrs.table_name else gurtrh.table_name end
        ) as table_name
        , sum(
            (
                case when gurtrs.skill_weight is not null and gurtrh.hub_weight is not null 
                    then gurtrs.skill_weight + gurtrh.hub_weight
                when gurtrs.skill_weight is null and gurtrh.hub_weight is not null
                    then gurtrh.hub_weight
                when gurtrs.skill_weight is not null and gurtrh.hub_weight is null
                    then gurtrs.skill_weight
                else 0
                end
            ) + 
            coalesce((
                select total_weight from get_user_resource_preference 
                where resource_model = gurtrs.table_name 
                    or resource_model = gurtrh.table_name
            ), 0)
        ) as total_score
    from get_user_reference_table_relevancy_score_by_skills as gurtrs
    full join get_user_reference_table_relevancy_score_by_hubs as gurtrh 
        on gurtrh.table_id = gurtrs.table_id 
            and gurtrh.table_name = gurtrs.table_name
    group by 1, 2
    order by total_score desc
)

select * from get_user_reference_relevancy_score;
        """)
        rows = cursor.fetchall()
        for row in rows:
            user_resource_preference.append(row[0])

    return user_resource_preference

