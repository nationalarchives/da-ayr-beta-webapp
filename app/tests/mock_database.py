import uuid

from app.main.db.models import Body, Consignment, File, FileMetadata, Series, db


def create_test_file():
    new_body = Body(
        BodyId=uuid.uuid4(), Name="test body1", Description="test body1"
    )
    db.session.add(new_body)
    db.session.commit()

    new_series = Series(
        SeriesId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        Name="test series1",
        Description="test series1",
    )
    db.session.add(new_series)
    db.session.commit()

    new_consignment = Consignment(
        ConsignmentId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        SeriesId=new_series.SeriesId,
        ConsignmentReference="test consignment1",
        ContactName="test young",
        ContactEmail="test1@test.com",
        ConsignmentType="standard",
        TransferStartDatetime="2023-01-01",
        TransferCompleteDatetime="2023-01-01",
    )
    db.session.add(new_consignment)
    db.session.commit()

    file_1 = File(
        FileId=uuid.uuid4(),
        ConsignmentId=new_consignment.ConsignmentId,
        FileName="test_file1.pdf",
        FileType="file",
        FileReference="test_file1.pdf",
        FilePath="/data/test_file1.pdf",
    )
    db.session.add(file_1)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="file_name",
        Value="test_file1.pdf",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="closure_type",
        Value="open",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="file_type",
        Value="pdf",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    return file_1


def create_two_test_files():
    # first record
    new_body = Body(
        BodyId=uuid.uuid4(), Name="test body1", Description="test body1"
    )
    db.session.add(new_body)
    db.session.commit()

    new_series = Series(
        SeriesId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        Name="test series1",
        Description="test series1",
    )
    db.session.add(new_series)
    db.session.commit()

    new_consignment = Consignment(
        ConsignmentId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        SeriesId=new_series.SeriesId,
        ConsignmentReference="test consignment1",
        ContactName="test young",
        ContactEmail="test1@test.com",
        ConsignmentType="standard",
        TransferStartDatetime="2023-01-01",
        TransferCompleteDatetime="2023-01-01",
    )
    db.session.add(new_consignment)
    db.session.commit()

    file_1 = File(
        FileId=uuid.uuid4(),
        ConsignmentId=new_consignment.ConsignmentId,
        FileName="test_file1.pdf",
        FileType="file",
        FileReference="test_file1.pdf",
        FilePath="/data/test_file1.pdf",
    )
    db.session.add(file_1)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="file_name",
        Value="test_file1.pdf",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="closure_type",
        Value="open",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    file_1_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_1.FileId,
        PropertyName="file_type",
        Value="pdf",
    )
    db.session.add(file_1_metadata)
    db.session.commit()

    # second record
    new_body = Body(
        BodyId=uuid.uuid4(), Name="test body2", Description="test body2"
    )
    db.session.add(new_body)
    db.session.commit()

    new_series = Series(
        SeriesId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        Name="test series2",
        Description="test series2",
    )
    db.session.add(new_series)
    db.session.commit()

    new_consignment = Consignment(
        ConsignmentId=uuid.uuid4(),
        BodyId=new_body.BodyId,
        SeriesId=new_series.SeriesId,
        ConsignmentReference="test consignment2",
        ContactName="test young",
        ContactEmail="test2@test.com",
        ConsignmentType="standard",
        TransferStartDatetime="2023-01-01",
        TransferCompleteDatetime="2023-01-01",
    )
    db.session.add(new_consignment)
    db.session.commit()

    file_2 = File(
        FileId=uuid.uuid4(),
        ConsignmentId=new_consignment.ConsignmentId,
        FileName="test_file2.txt",
        FileType="file",
        FileReference="test_file2.txt",
        FilePath="/data/test_file2.txt",
    )
    db.session.add(file_2)
    db.session.commit()

    file_2_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_2.FileId,
        PropertyName="file_name",
        Value="test_file2.pdf",
    )
    db.session.add(file_2_metadata)
    db.session.commit()

    file_2_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_2.FileId,
        PropertyName="closure_type",
        Value="closed",
    )
    db.session.add(file_2_metadata)
    db.session.commit()

    file_2_metadata = FileMetadata(
        MetadataId=uuid.uuid4(),
        FileId=file_2.FileId,
        PropertyName="file_type",
        Value="txt",
    )
    db.session.add(file_2_metadata)
    db.session.commit()

    return [file_1, file_2]
