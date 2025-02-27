import opensearchpy
from flask import abort, current_app
from opensearchpy import OpenSearch, RequestsHttpConnection

from app.main.util.date_validator import format_opensearch_date
from app.main.util.pagination import calculate_total_pages, get_pagination

OPENSEARCH_FIELD_NAME_MAP = {
    "file_name": "File name",
    "description": "Description",
    "transferring_body": "Transferring body",
    "foi_exemption_code": "FOI code",
    "content": "Content",
    "closure_start_date": "Closure start date",
    "end_date": "Record date",
    "date_last_modified": "Record date",
    "closure_start_date": "Closure start date",
    # might be useful to show in the future
    # "file_reference": "File reference",
    # "file_path": "File path",
    "citeable_reference": "Citeable reference",
    "series_name": "Series name",
    "transferring_body_description": "Transferring body description",
    "consignment_reference": "Consignment ref",
}


def format_opensearch_results(results):
    """Format date fields of the _source object inside results"""
    results_clone = results.copy()
    for result in results_clone:
        for key, value in result["_source"].items():
            if "date" in key:
                result["_source"][key] = format_opensearch_date(value or "")
    return results_clone


def filter_opensearch_highlight_results(results):
    """Filter highlight results for fields that are not needed"""
    results_clone = results.copy()
    for result in results_clone:
        if result.get("highlight", None):
            keys_to_remove = [
                key for key in result["highlight"].keys() if ".keyword" in key
            ]
            for key in keys_to_remove:
                del result["highlight"][key]
    return results_clone


def rearrange_opensearch_results_for_relevant_fields(results, sort):
    """
    Rearrange OpenSearch results to display relevant highlight fields based on the specified sort order.

    Args:
        results (list): A list of OpenSearch result dictionaries.
        sort (str): The field used for sorting ("file_name", "description", "metadata", or "content").

    Returns:
        list: The rearranged OpenSearch results with updated highlight fields.
    """
    results_clone = results.copy()

    for result in results_clone:
        if "highlight" not in result:
            continue
        highlight_fields = result["highlight"]

        if sort == "file_name":
            ordered_highlight = reorder_fields(highlight_fields, ["file_name"])
        elif sort == "description":
            ordered_highlight = reorder_fields(
                highlight_fields, ["description", "file_name"]
            )
        elif sort == "metadata":
            ordered_highlight = reorder_fields(
                highlight_fields, [], ["file_name", "content"]
            )
        elif sort == "content":
            ordered_highlight = reorder_fields(
                highlight_fields, ["content", "file_name"]
            )
        else:
            ordered_highlight = highlight_fields

        result["highlight"] = ordered_highlight

    return results_clone


def reorder_fields(fields, priority_fields=[], last_fields=[]):
    """
    Rearranges a dictionary's fields based on priority and last field rules.

    Args:
        fields (dict): Dictionary of fields to reorder.
        priority_fields (list): Fields to move to the top in order.
        last_fields (list): Fields to move to the bottom in order.

    Returns:
        dict: Reordered dictionary of fields.
    """
    fields_at_top = {k: fields[k] for k in priority_fields if k in fields}
    fields_at_bottom = {k: fields[k] for k in last_fields if k in fields}
    middle_fields = {
        k: v
        for k, v in fields.items()
        if k not in fields_at_top and k not in fields_at_bottom
    }
    ordered_fields = {**fields_at_top, **middle_fields, **fields_at_bottom}

    return ordered_fields


def post_process_opensearch_results(results, sort):
    results = format_opensearch_results(results)
    results = filter_opensearch_highlight_results(results)
    results = rearrange_opensearch_results_for_relevant_fields(results, sort)
    return results


def remove_field(fields, field_name):
    return [field for field in fields if field_name != field]


def get_open_search_fields_to_search_on_and_sorting(
    search_area, sort="file_name"
):
    """
    Retrieve fields and sorting configuration for an OpenSearch query based on the search area
    (all fields, metadata, record, etc.) and sorting preference.
    """
    # Sort option configuration
    sort_option_map = {
        "file_name": {
            "boosts": {"file_name": 3},
            "order": "desc",
        },
        "description": {
            "boosts": {"description": 3, "file_name": 2},
            "order": "desc",
        },
        "metadata": {
            "boosts": {"file_name": 0.2, "content": 0.1},
            "order": "desc",
        },
        "record": {
            "boosts": {"content": 3, "file_name": 2},
            "order": "desc",
        },
        "least_matches": {
            "boosts": {},
            "order": "asc",
        },
        "most_matches": {
            "boosts": {},  # No boosting
            "order": "desc",  # Descending order for most matches
        },
    }

    fields = determine_fields_by_search_area(search_area)
    fields = apply_boosts_for_sorting(fields, sort, sort_option_map)
    sorting = get_sorting_config(sort, sort_option_map)
    return fields, sorting


def determine_fields_by_search_area(search_area):
    """
    Determine the base fields to use based on the search area.
    """
    all_fields = list(OPENSEARCH_FIELD_NAME_MAP.keys())
    if search_area == "metadata":
        return get_filtered_list(all_fields, ["file_name", "content"])
    elif search_area == "record":
        return ["file_name", "content"]
    return all_fields


def apply_boosts_for_sorting(fields, sort, sort_option_map):
    """
    Adjust fields by applying boosts or penalties based on the sorting preference.
    """
    sort_config = sort_option_map.get(sort, {})
    boost_map = sort_config.get("boosts", {})

    # Apply boosts to the boosted fields
    return apply_field_boosts(fields, boost_map)


def get_sorting_config(sort, sort_option_map):
    """
    Get the sorting configuration based on the sort preference.
    """
    sort_config = sort_option_map.get(sort, {})
    sort_order = sort_config.get("order", "desc")
    return [{"_score": {"order": sort_order}}]


def apply_field_boosts(fields, boost_map):
    """
    Apply boost values to fields as per the boost map.
    """
    return [f"{field}^{boost_map.get(field, 1)}" for field in fields]


def get_param(param, request):
    """Get a specific param from either form or args"""
    return request.form.get(param, "") or request.args.get(param, "")


def get_query_and_search_area(request):
    """Fetch query and search_area from form or request args"""
    query = get_param("query", request)
    search_area = get_param("search_area", request)
    return query.strip(), search_area


def setup_opensearch():
    """Setup and return an OpenSearch client"""
    return OpenSearch(
        hosts=current_app.config.get("OPEN_SEARCH_HOST"),
        http_auth=current_app.config.get("OPEN_SEARCH_HTTP_AUTH"),
        use_ssl=True,
        verify_certs=True,
        ca_certs=current_app.config.get("OPEN_SEARCH_CA_CERTS"),
        connection_class=RequestsHttpConnection,
    )


def execute_search(open_search, dsl_query, page, per_page):
    """Execute the search query using OpenSearch"""
    from_ = per_page * (page - 1)
    try:
        return open_search.search(
            dsl_query,
            from_=from_,
            size=per_page,
            timeout=current_app.config["OPEN_SEARCH_TIMEOUT"],
        )
    except opensearchpy.exceptions.ConnectionTimeout:
        abort(504)


def get_pagination_info(results, page, per_page):
    """Calculate pagination information"""
    total_records = (
        results["hits"]["total"]["value"] if "hits" in results else 0
    )
    page_count = calculate_total_pages(total_records, per_page)
    pagination = get_pagination(page, page_count)
    return total_records, pagination


def get_filtered_list(to_filter, filter):
    """Filters a list based on the contents of another list"""
    return [field for field in to_filter if field not in filter or []]


def get_all_fields_excluding(open_search, index_name, exclude_fields=None):
    """Retrieve all fields from the index and exclude certain fields"""
    mappings = open_search.indices.get_mapping(index=index_name)
    all_fields = list(mappings[index_name]["mappings"]["properties"].keys())
    filtered_fields = get_filtered_list(all_fields, exclude_fields)

    return filtered_fields


def build_must_clauses(search_fields, quoted_phrases, single_terms):
    """Helper function to build must_clauses for OpenSearch with AND"""
    must_clauses = []

    for phrase in quoted_phrases:
        must_clauses.append(
            {
                "multi_match": {
                    "query": phrase,
                    "fields": search_fields,
                    "type": "phrase",
                    "lenient": True,
                }
            }
        )

    for term in single_terms:
        must_clauses.append(
            {
                "multi_match": {
                    "query": term,
                    "fields": search_fields,
                    "fuzziness": "AUTO",
                    "lenient": True,
                }
            }
        )

    return must_clauses


def build_dsl_search_query(
    search_fields,
    filter_clauses,
    quoted_phrases,
    single_terms,
    sorting,
):
    """Constructs the base DSL query for OpenSearch with AND"""
    must_clauses = build_must_clauses(
        search_fields, quoted_phrases, single_terms
    )

    return {
        "query": {
            "bool": {
                "must": must_clauses,
                "filter": filter_clauses,
            }
        },
        "sort": sorting,
        "_source": True,
    }


def build_search_results_summary_query(
    search_fields,
    quoted_phrases,
    single_terms,
    sorting,
):
    filter_clauses = []
    dsl_query = build_dsl_search_query(
        search_fields,
        filter_clauses,
        quoted_phrases,
        single_terms,
        sorting,
    )
    aggregations = {
        "aggs": {
            "aggregate_by_transferring_body": {
                "terms": {"field": "transferring_body_id.keyword"},
                "aggs": {
                    "top_transferring_body_hits": {
                        "top_hits": {
                            "size": 1,
                            "_source": ["transferring_body"],
                        }
                    }
                },
            }
        },
    }
    return {**dsl_query, **aggregations}


def build_search_transferring_body_query(
    search_fields,
    transferring_body_id,
    highlight_tag,
    quoted_phrases,
    single_terms,
    sorting,
):
    filter_clauses = [
        {"term": {"transferring_body_id.keyword": transferring_body_id}}
    ]
    dsl_query = build_dsl_search_query(
        search_fields,
        filter_clauses,
        quoted_phrases,
        single_terms,
        sorting,
    )
    highlighting = {
        "highlight": {
            "pre_tags": [f"<{highlight_tag}>"],
            "post_tags": [f"</{highlight_tag}>"],
            "fields": {
                "*": {},
            },
        },
    }
    return {**dsl_query, **highlighting}


def extract_search_terms(query):
    """
    Extract search terms from the query string, handling both quoted phrases and single terms.
    Multiple search terms are separated by '&'.

    Args:
        query (str): The search query string

    Returns:
        tuple: A tuple containing two lists:
            - quoted_phrases: A list of phrases enclosed in double quotes.
            - single_terms: A list of individual terms that are not in quotes.
    """
    quoted_phrases = []
    single_terms = []

    query_parts = query.split("&")

    for part in query_parts:
        part = part.strip()
        if not part:
            continue

        if part.startswith('"') and part.endswith('"') and len(part) > 2:
            quoted_phrases.append(part[1:-1])
        else:
            single_terms.append(part)

    return quoted_phrases, single_terms
