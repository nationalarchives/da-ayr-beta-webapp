from app.tests.assertions import assert_contains_html
from app.tests.conftest import mock_standard_user, mock_superuser
from app.tests.factories import FileFactory, FileMetadataFactory


def test_invalid_id_raises_404(client):
    """
    Given a UUID, `invalid_file_id`, not corresponding to the id
        of a file in the database
    When a GET request is made to `/record/invalid_file_id`
    Then a 404 http response is returned
    """
    response = client.get("/record/some-id")

    assert response.status_code == 404


def test_returns_record_page_for_user_with_access_to_files_transferring_body(
    client,
):
    """
    Given a File in the database
    When a standard user with access to the file's transferring body makes a
        request to view the record page
    Then the response status code should be 200
    And the HTML content should contain specific elements
        related to the record
    """
    file = FileFactory(
        FileName="test_file.txt",
        FilePath="data/content/folder_a/test_file.txt",
        FileType="file",
    )

    mock_standard_user(client, file.file_consignments.consignment_bodies.Name)

    metadata = {
        "date_last_modified": "2023-02-25T10:12:47",
        "closure_type": "Closed",
        "description": "Test description",
        "held_by": "Test holder",
        "legal_status": "Test legal status",
        "rights_copyright": "Test copyright",
        "language": "English",
    }

    [
        FileMetadataFactory(
            file_metadata=file,
            PropertyName=property_name,
            Value=value,
        )
        for property_name, value in metadata.items()
    ]

    response = client.get(f"/record/{file.FileId}")

    assert response.status_code == 200

    html = response.data.decode()

    expected_breadcrumbs_html = f"""
    <div class="govuk-grid-column-full govuk-grid-column-full__page-nav">
    <p class="govuk-body-m govuk-body-m__record-view">You are viewing</p>
    <div class="govuk-breadcrumbs govuk-breadcrumbs--record">
        <ol class="govuk-breadcrumbs__list">
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record" href="/browse">Everything</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record"
                href="/browse?transferring_body_id={file.file_consignments.consignment_bodies.BodyId}">{file.file_consignments.consignment_bodies.Name}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record"
                href="/browse?series_id={file.file_consignments.consignment_series.SeriesId}">{file.file_consignments.consignment_series.Name}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record"
                href="/browse?consignment_id={file.ConsignmentId}">{file.file_consignments.ConsignmentReference}</a>
            </li>
            <li class="govuk-breadcrumbs__list-item">
            <a class="govuk-breadcrumbs__link--record">test_file.txt</a>
            </li>
        </ol>
        </div>
    </div>
    """

    assert_contains_html(
        expected_breadcrumbs_html,
        html,
        "div",
        {"class": "govuk-grid-column-full govuk-grid-column-full__page-nav"},
    )

    expected_record_summary_html = f"""
    <dl class="govuk-summary-list govuk-summary-list-record--record">
        <div class="govuk-summary-list__row"></div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Filename</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">test_file.txt</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Status</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">
                <span class="govuk-tag govuk-tag--red">Closed</span>
            </dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Transferring body</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">
                {file.file_consignments.consignment_bodies.Name}
            </dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Consignment ID</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">
                {file.file_consignments.ConsignmentId}
            </dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Description</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">Test description</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Date last modified</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">2023-02-25T10:12:47</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Held by</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">Test holder</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Legal status</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">Test legal status</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Rights copyright</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">Test copyright</dd>
        </div>
        <div class="govuk-summary-list__row govuk-summary-list-record__row--record">
            <dt class="govuk-summary-list__key govuk-summary-list-record__key--record-table">Language</dt>
            <dd class="govuk-summary-list__value govuk-summary-list-record__value--record">English</dd>
        </div>
    </dl>
    """

    assert_contains_html(
        expected_record_summary_html,
        html,
        "dl",
        {"class": "govuk-summary-list govuk-summary-list-record--record"},
    )

    expected_arrangement_html = """
    <div class="record-container">
        <h3 class="govuk-heading-m govuk-heading-m__record-header">Record arrangement</h3>
        <ol>
            <li class="govuk-body govuk-body__record-arrangement-list">data</li>
            <li class=" govuk-body govuk-body__record-arrangement-list">content</li>
            <li class="govuk-body govuk-body__record-arrangement-list">folder_a</li>
            <li class="govuk-body govuk-body__record-arrangement-list">test_file.txt</li>
        </ol>
    </div>
    """

    assert_contains_html(
        expected_arrangement_html, html, "div", {"class": "record-container"}
    )

    expected_download_html = """
    <div class="rights-container">
        <h3 class="govuk-heading-m govuk-heading-m__rights-header">Rights to access</h3>
        <button class="govuk-button govuk-button__download--record" data-module="govuk-button">
            Download record
        </button>
        <p class="govuk-body govuk-body--terms-of-use">
            Refer to <a href="/terms-of-use" class="govuk-link">Terms of use.</a>
        </p>
    </div>
    """

    assert_contains_html(
        expected_download_html, html, "div", {"class": "rights-container"}
    )


def test_raises_404_for_user_without_access_to_files_transferring_body(client):
    """
    Given a File in the database
    When a standard user without access to the file's consignment body makes a
        request to view the record page
    Then the response status code should be 404
    """

    file = FileFactory(
        FileName="test_file.txt",
        FilePath="data/content/folder_a/test_file.txt",
        FileType="file",
    )

    metadata = {
        "date_last_modified": "2023-02-25T10:12:47",
        "closure_type": "Closed",
        "description": "Test description",
        "held_by": "Test holder",
        "legal_status": "Test legal status",
        "rights_copyright": "Test copyright",
        "language": "English",
    }

    [
        FileMetadataFactory(
            file_metadata=file,
            PropertyName=property_name,
            Value=value,
        )
        for property_name, value in metadata.items()
    ]

    mock_standard_user(client, "different_body")

    response = client.get(f"/record/{file.FileId}")

    assert response.status_code == 404


def test_returns_record_page_for_superuser(client):
    """
    Given a File in the database
    And a superuser
    When the superuser makes a request to view the record page
    Then the response status code should be 200
    """
    mock_superuser(client)

    file = FileFactory(
        FileName="test_file.txt",
        FilePath="data/content/folder_a/test_file.txt",
        FileType="file",
    )

    metadata = {
        "date_last_modified": "2023-02-25T10:12:47",
        "closure_type": "Closed",
        "description": "Test description",
        "held_by": "Test holder",
        "legal_status": "Test legal status",
        "rights_copyright": "Test copyright",
        "language": "English",
    }

    [
        FileMetadataFactory(
            file_metadata=file,
            PropertyName=property_name,
            Value=value,
        )
        for property_name, value in metadata.items()
    ]

    response = client.get(f"/record/{file.FileId}")

    assert response.status_code == 200
