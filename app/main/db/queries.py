import uuid

from sqlalchemy import Text, and_, exc, func, or_

from app.main.authorize.keycloak_manager import (
    decode_token,
    get_user_transferring_body_keycloak_groups,
)
from app.main.db.models import Body, Consignment, File, FileMetadata, Series, db


def fuzzy_search(query: str, page: int, per_page: int):
    if len(query) > 0:
        fuzzy_search_query = _build_fuzzy_search_query(query)
        return fuzzy_search_query.paginate(page=page, per_page=per_page)


def browse_data(
    page,
    per_page,
    transferring_body_id=None,
    series_id=None,
    consignment_id=None,
):
    if transferring_body_id:
        browse_query = _build_transferring_body_filter_query(
            transferring_body_id
        )
    elif series_id:
        browse_query = _build_series_filter_query(series_id)
    elif consignment_id:
        browse_query = _build_consignment_filter_query(consignment_id)
    else:
        browse_query = _build_browse_everything_query()

    return browse_query.paginate(page=page, per_page=per_page)


def get_user_accessible_transferring_bodies(access_token):
    if not access_token:
        return []
    decoded_token = decode_token(access_token)
    if not decoded_token["active"]:
        return []

    user_groups = decoded_token["groups"]

    user_transferring_body_keycloak_groups = (
        get_user_transferring_body_keycloak_groups(user_groups)
    )

    if not user_transferring_body_keycloak_groups:
        return []

    try:
        query = db.session.query(Body.Name)
        bodies = db.session.execute(query)
    except exc.SQLAlchemyError as e:
        print("Failed to return results from database with error : " + str(e))
        return []

    user_accessible_transferring_bodies = []

    for body in bodies:
        body_name = body.Name
        if _body_in_users_groups(
            body_name, user_transferring_body_keycloak_groups
        ):
            user_accessible_transferring_bodies.append(body_name)

    return user_accessible_transferring_bodies


def _body_in_users_groups(body, user_transferring_body_keycloak_groups):
    for user_group in user_transferring_body_keycloak_groups:
        if (
            user_group.strip().replace(" ", "").lower()
            == body.strip().replace(" ", "").lower()
        ):
            return True

    return False


def get_file_metadata(file_id):
    results = []
    query = (
        db.select(
            FileMetadata.PropertyName.label("property_name"),
            FileMetadata.Value.label("property_value"),
        )
        .join(File, FileMetadata.FileId == File.FileId)
        .where((func.lower(File.FileType) == "file") & (File.FileId == file_id))
    )
    query_results = None
    try:
        query_results = db.session.execute(query)
    except exc.SQLAlchemyError as e:
        print("Failed to return results from database with error : " + str(e))

    if query_results is not None:
        for r in query_results:
            record = {
                "property_name": r.property_name,
                "property_value": r.property_value,
            }
            results.append(record)
    return results


def _build_fuzzy_search_query(query_string: str):
    filter_value = str(f"%{query_string}%").lower()

    query = (
        db.session.query(
            Body.Name.label("transferring_body"),
            Series.Name.label("series"),
            Consignment.ConsignmentReference.label("consignment_reference"),
            File.FileName.label("file_name"),
            Body.BodyId.label("body_id"),
            Series.SeriesId.label("series_id"),
        )
        .join(Series, Series.BodyId == Body.BodyId)
        .join(
            Consignment,
            and_(
                Consignment.BodyId == Body.BodyId,
                Consignment.SeriesId == Series.SeriesId,
            ),
        )
        .join(File, File.ConsignmentId == Consignment.ConsignmentId)
        .join(FileMetadata, FileMetadata.FileId == File.FileId)
        .where(
            and_(
                func.lower(File.FileType) == "file",
                or_(
                    func.lower(Consignment.ConsignmentReference).like(
                        filter_value
                    ),
                    func.lower(Consignment.ConsignmentType).like(filter_value),
                    func.lower(Consignment.ContactName).like(filter_value),
                    func.lower(Consignment.ContactEmail).like(filter_value),
                    func.cast(Consignment.TransferStartDatetime, Text).like(
                        filter_value
                    ),
                    func.cast(Consignment.TransferCompleteDatetime, Text).like(
                        filter_value
                    ),
                    func.cast(Consignment.ExportDatetime, Text).like(
                        filter_value
                    ),
                    func.lower(Body.Name).like(filter_value),
                    func.lower(Body.Description).like(filter_value),
                    func.lower(Series.Name).like(filter_value),
                    func.lower(Series.Description).like(filter_value),
                    func.lower(File.FileName).like(filter_value),
                    func.lower(File.FileReference).like(filter_value),
                    func.lower(FileMetadata.Value).like(filter_value),
                ),
            )
        )
        .distinct()
        .order_by(Body.Name, Series.Name)
    )

    return query


def _build_browse_everything_query():
    query = (
        db.session.query(
            Body.BodyId.label("transferring_body_id"),
            Body.Name.label("transferring_body"),
            Series.SeriesId.label("series_id"),
            Series.Name.label("series"),
            func.max(Consignment.TransferCompleteDatetime).label(
                "last_record_transferred"
            ),
            func.count(func.distinct(Consignment.ConsignmentReference)).label(
                "consignment_in_series"
            ),
            func.count(func.distinct(File.FileId)).label("records_held"),
        )
        .join(Consignment, Consignment.ConsignmentId == File.ConsignmentId)
        .join(Body, Body.BodyId == Consignment.BodyId)
        .join(Series, Series.SeriesId == Consignment.SeriesId)
        .where(func.lower(File.FileType) == "file")
        .group_by(Body.BodyId, Series.SeriesId)
        .order_by(Body.Name, Series.Name)
    )

    return query


def _build_transferring_body_filter_query(transferring_body_id):
    query = (
        db.session.query(
            Body.BodyId.label("transferring_body_id"),
            Body.Name.label("transferring_body"),
            Series.SeriesId.label("series_id"),
            Series.Name.label("series"),
            func.max(Consignment.TransferCompleteDatetime).label(
                "last_record_transferred"
            ),
            func.count(func.distinct(Consignment.ConsignmentReference)).label(
                "consignment_in_series"
            ),
            func.count(func.distinct(File.FileId)).label("records_held"),
        )
        .join(Consignment, Consignment.ConsignmentId == File.ConsignmentId)
        .join(Body, Body.BodyId == Consignment.BodyId)
        .join(Series, Series.SeriesId == Consignment.SeriesId)
        .where(
            (func.lower(File.FileType) == "file")
            & (Body.BodyId == transferring_body_id)
        )
        .group_by(Body.BodyId, Series.SeriesId)
        .order_by(Body.Name, Series.Name)
    )

    return query


def _build_series_filter_query(series_id):
    query = (
        db.session.query(
            Body.BodyId.label("transferring_body_id"),
            Body.Name.label("transferring_body"),
            Series.SeriesId.label("series_id"),
            Series.Name.label("series"),
            func.max(Consignment.TransferCompleteDatetime).label(
                "last_record_transferred"
            ),
            func.count(func.distinct(File.FileId)).label("records_held"),
            Consignment.ConsignmentId.label("consignment_id"),
            Consignment.ConsignmentReference.label("consignment_reference"),
        )
        .join(Consignment, Consignment.ConsignmentId == File.ConsignmentId)
        .join(Body, Body.BodyId == Consignment.BodyId)
        .join(Series, Series.SeriesId == Consignment.SeriesId)
        .where(
            (func.lower(File.FileType) == "file")
            & (Series.SeriesId == series_id)
        )
        .group_by(Body.BodyId, Series.SeriesId, Consignment.ConsignmentId)
        .order_by(Body.Name, Series.Name)
    )

    return query


def _build_consignment_filter_query(consignment_id: uuid.UUID):
    select = db.session.query(
        File.FileId,
        File.FileName,
        func.max(
            db.case(
                (
                    FileMetadata.PropertyName == "Last Modified",
                    FileMetadata.Value,
                ),
                else_=None,
            )
        ).label("last_modified"),
        func.max(
            db.case(
                (FileMetadata.PropertyName == "Status", FileMetadata.Value),
                else_=None,
            )
        ).label("status"),
        func.max(
            db.case(
                (
                    FileMetadata.PropertyName == "Closure Period",
                    FileMetadata.Value,
                ),
                else_=None,
            )
        ).label("closure_period"),
    )

    filters = [File.ConsignmentId == consignment_id]

    query = (
        select.join(FileMetadata, File.FileId == FileMetadata.FileId)
        .filter(*filters)
        .group_by(File.FileId)
        .order_by(File.FileName)
    )

    return query
