from app.default.models import Batch, Csv, Field, ProdData
from datetime import datetime
import csv
import os


def create_csv_from_data(batch_id):
    """ Create a CSV file outputting all of the data in the database for a batch
    ('data' does not include CSV logs that have been uploaded into the db)"""
    filename = 'data.csv'
    filepath = os.path.abspath(os.path.join('app', 'static', 'temp', filename))
    # Remove the old file
    with open(filepath, 'w+') as csv_file:
        batch = Batch.query.get_or_404(batch_id)

        # These are the names of the headings in the CSV file. The first one is Part ID. Get the rest programmatically
        csv_field_names = ['Part Number']

        # Get all of the field names for the data in the part and make them headers
        fields = []
        for prod_data in batch.parts[0].data:
            fields.append(Field.query.get_or_404(prod_data.field_id))
        for field in fields:
            csv_field_names.append(field.field_name)

        # This writer just creates a row at the top of the CSV file with information about the batch
        title_writer = csv.writer(csv_file)

        # Create a cell with batch information
        cell_batch = "Batch {batch_no} ({part_type})".format(
            batch_no=batch.batch_number,
            part_type=batch.part_type.part_name)

        # Create a cell with the users that worked on the batch
        cell_users = "User:"
        users = batch.users.all()
        for u in users:
            cell_users += " " + u.username

        # Create cells for the time started and finished for the batch
        created_time = datetime.fromtimestamp(batch.created_timestamp).strftime("%d-%b-%Y %H:%M")
        if batch.completed_timestamp is None:
            completed_time = "IN PROGRESS"
        else:
            completed_time = datetime.fromtimestamp(batch.completed_timestamp).strftime("%d-%b-%Y %H:%M")
        cell_started = "Time started: " + created_time
        cell_completed = "Time completed: " + completed_time

        # Write the top row, and a blank row beneath
        title_writer.writerow([cell_batch, cell_users, cell_started, cell_completed])
        title_writer.writerow("")

        # Use a dictwriter to write the actual data to the file
        writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)
        # Write the headers
        writer.writeheader()

        # Each part has one row in the CSV
        for part in batch.parts:
            d = {}
            for field in fields:
                prod_data = ProdData.query.filter_by(field_id=field.id, part_id=part.id).first()
                if prod_data is not None:
                    value = prod_data.field_data
                    # Write to the CSV using a dict in the format {field_name: data}
                    d.update({'Part Number': part.relative_id})
                    d.update({field.field_name: value})
            try:
                writer.writerow(d)
            except ValueError as ve:
                print(ve)

    return filepath


def recreate_csv_log(batch_id):
    """ Create a CSV from CSV logs that have been uploaded and stored in the database"""
    batch_csv_data = Csv.query.filter_by(batch_id=batch_id).all()
    filename = 'log.csv'
    filepath = os.path.abspath(os.path.join('app', 'static', 'temp', filename))
    with open(filepath, 'w+') as csv_file:
        for csv_data in batch_csv_data:
            csv_file.write(csv_data.body.decode('utf-8'))
    return filepath


if __name__ == '__main__':
    create_csv_from_data(1)
    recreate_csv_log(1)
