import re

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


def post_process_opensearch_results(results):
    results = format_opensearch_results(results)
    results = filter_opensearch_highlight_results(results)
    return results


def remove_field(fields, field_name):
    return [field for field in fields if field_name != field]


def get_open_search_fields_to_search_on_and_sorting(
    search_area, sort="file_name"
):
    """Retrieve a list of fields depending on the search area (all fields, metadata, record, etc.) and sorting."""
    sort_order = "asc" if sort == "least_matches" else "desc"
    sorting = [{"_score": {"order": sort_order}}]

    fields = list(OPENSEARCH_FIELD_NAME_MAP.keys())
    fields_record = ["content"]

    if search_area == "metadata":
        fields = get_filtered_list(fields, ["file_name", "content"])
    elif search_area == "record":
        fields = fields_record

    if sort == "file_name":
        fields = remove_field(fields, "file_name")
        fields.append("file_name^3")
    elif sort == "description":
        fields = remove_field(fields, "file_name")
        fields = remove_field(fields, "description")
        fields.append("description^3")
        fields.append("file_name^2")
    elif sort == "metadata":
        # boost all fields to ^100 and then apply penalties to specific fields
        fields = [
            f"{field}^100" for field in fields
        ]  # boost all fields to ^100
        fields = remove_field(fields, "file_name")
        fields = remove_field(fields, "content")
        # penalize "file_name" and "content"
        fields.append("file_name^0.2")
        fields.append("content^0.1")
    elif sort == "content":
        fields = remove_field(fields, "file_name")
        fields = remove_field(fields, "content")
        fields.append("content^3")
        fields.append("file_name^2")

    return fields, sorting


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
    sorting_orders,
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
        # set as {} until sorting ticket is in done
        "sort": sorting,
        "_source": True,
    }


def build_search_results_summary_query(
    search_fields,
    sorting_orders,
    quoted_phrases,
    single_terms,
    sorting,
):
    filter_clauses = []
    dsl_query = build_dsl_search_query(
        search_fields,
        sorting_orders,
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
    sorting_orders,
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
        sorting_orders,
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
    Extracts quoted phrases and single terms from a search query string.

    Args:
        query (str): The search query string containing both quoted phrases and single terms.

    Returns:
        tuple: A tuple containing two lists:
            - quoted_phrases: A list of phrases enclosed in double quotes.
            - single_terms: A list of individual terms that are not in quotes.
    """
    # Extract quoted phrases
    quoted_phrases = re.findall(r'"([^"]*)"', query)

    # Remove quoted phrases and split remaining terms by spaces
    remaining_terms = re.sub(r'"[^"]*"', "", query).replace(",", " ")
    single_terms = [
        term.strip() for term in remaining_terms.split() if term.strip()
    ]

    return quoted_phrases, single_terms
