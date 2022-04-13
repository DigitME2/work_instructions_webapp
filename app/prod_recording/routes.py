from app.extensions import db
from app.prod_recording import bp
from app.prod_recording.export import recreate_csv_log, create_csv_from_data
from app.prod_recording.forms import NewBatchForm
from app.default.models import Batch, Part, Step, PartType, ProdData, Csv
from flask import render_template, request, flash, redirect, url_for, abort, send_file
from flask_login import current_user, login_required
import os
from time import time


def check_if_batch_wide(current_batch, field):
    """ Check if all of the parts in a certain batch are to have the same value for a certain field """

    # If the field isn't flagged as batch wide by default, return false
    if not field.batch_wide:
        return False
    # If some of this batch's parts have differing data for the same field,
    # data has been saved as non-batch-wide in the past so return false.
    parts_data = []
    for part in current_batch.parts:
        prod_data = ProdData.query.filter_by(part_id=part.id, field_id=field.id).first()
        if prod_data is not None:
            data = prod_data.field_data
        else:
            data = ""
        parts_data.append(data)
        if data != parts_data[0]:
            return False
    # If both these conditions fail, the field is batch wide
    return True


@bp.route('/production', methods=['GET', 'POST'])
@login_required
def production():
    """ The page that shows up during production, showing instructions and prompting for data that needs recording."""
    scroll_to = ""
    try:
        current_batch = Batch.query.get_or_404(request.args.get("batch_id"))
        steps = Step.query.filter_by(part_type_id=current_batch.part_type_id).all()

    except TypeError:
        flash("Bad step or batch selected", category="top")
        return redirect(url_for('default.home'))
    nav_bar_title = str(current_batch.part_type.part_name) + " - Batch " + str(current_batch.batch_number)

    if request.method == 'POST':
        try:
            action = request.form["action"]
        except Exception as e:
            print(e)
            abort(400)
            return

        if action == "completeBatch":
            # Mark the batch as completed
            completed_batch = Batch.query.get_or_404(request.form["batchId"])
            completed_batch.completed = True
            completed_batch.completed_timestamp = time()
            db.session.commit()
        elif action == "saveStep":
            current_batch.last_edit_timestamp = time()
            try:
                # Get the current step being saved
                step = Step.query.get_or_404(request.form['stepId'])
                # Loop through each part
                for part in current_batch.parts:
                    # For each field in the step, save the data in the database
                    for field in step.fields:
                        # Try and retrieve the old entry if one already exists
                        pd = ProdData.query.filter_by(part_id=part.id, field_id=field.id).first()
                        # Create it if it doesn't exist
                        if pd is None:
                            pd = ProdData(part_id=part.id, field_id=field.id, user_id=current_user.id)

                        # Check whether checkbox is checked and therefore all parts should share the same value
                        # The checkbox name is just the field id of the field it represents
                        all_parts_checkbox_name = str(field.id)
                        if all_parts_checkbox_name in request.form:
                            # Retrieve the entry from the form. The all parts element is named "0:field_id"
                            all_parts_html_field_name = "0:" + str(field.id)
                            field_data = request.form[all_parts_html_field_name]
                        else:
                            # Retrieve the entry from the form. Each html element is named "part_id:field_id"
                            html_field_name = str(part.id) + ":" + str(field.id)
                            field_data = request.form[html_field_name]

                        # Save the timestamp to the part
                        part.last_edit_timestamp = time()
                        db.session.add(part)
                        db.session.commit()

                        # Save the field data to the edit
                        pd.field_data = field_data

                        # Assign the current user to the edit
                        pd.user_id = current_user.id
                        db.session.add(pd)
                        db.session.commit()

                # Save a CSV if requested
                if 'csv_file' in request.files:
                    csv_file = request.files['csv_file']
                    # Check the file is a csv file
                    fn, file_extension = os.path.splitext(csv_file.filename)
                    if file_extension != '.csv':
                        # The category of the flash is used by Flask to display this warning on the correct step
                        flash_category = "step" + str(step.id)
                        flash("File not in csv format", category=flash_category)
                        return redirect(request.referrer)
                    csv_entry = Csv(body=csv_file.read(),
                                    batch_id=current_batch.id,
                                    step_id=step.id,
                                    uploaded_timestamp=time())
                    db.session.add(csv_entry)
                    db.session.commit()
                    print(csv_file.read())
                    flash_category = "step" + str(step.id)
                    flash("CSV file uploaded", category=flash_category)

                scroll_to = "step" + str(step.step_number)

            except:
                flash("Bad request", category="top")
    # Change the batch_wide status temporarily if the parts have been treated separately in the past
    for step in steps:
        for field in step.fields:
            field.temp_batch_wide = check_if_batch_wide(current_batch, field)

    return render_template('production.html',
                           nav_bar_title=nav_bar_title,
                           current_batch=current_batch,
                           steps=steps,
                           scroll_to=scroll_to)


@bp.route('/newbatch', methods=['GET', 'POST'])
@login_required
def new_batch():
    """The page to create a new batch"""
    form = NewBatchForm()
    # Create list of part names to fill the part-type selection box
    part_names = []
    for p in PartType.query.all():
        part_names.append((str(p.id), p.part_name))
    form.part_type.choices = part_names

    # Create a new batch, and new parts when form is submitted
    if form.validate_on_submit():
        batch = Batch(batch_number=form.batch_number.data,
                      part_type_id=form.part_type.data,
                      users=[current_user],
                      created_timestamp=time(),
                      last_edit_timestamp=time())
        db.session.add(batch)
        db.session.commit()  # Need to commit here so that the batch is assigned an id
        for i in range(0, form.amount.data):
            part = Part(batch_id=batch.id, relative_id=i + 1)
            db.session.add(part)
            # When a new part is created, create all the blank prodData entries for every field in every step
            for step in batch.part_type.steps:
                for field in step.fields:
                    pd = ProdData(part_id=part.id, field_id=field.id, field_data="")
                    db.session.add(pd)
        db.session.commit()
        return redirect(url_for('prod_recording.production', batch_id=batch.id))
    nav_bar_title = "Create new batch"
    return render_template('newbatch.html', form=form,
                           nav_bar_title=nav_bar_title)


@bp.route('/export', methods=['GET'])
@login_required
def export():
    """ Creates a file for the user to download."""
    batch_number = request.args.get('batchno')
    if request.args.get('target') == 'data':
        filepath = create_csv_from_data(batch_number)
        new_file_name = "batch_{batch}_data.csv".format(batch=batch_number)
    elif request.args.get('target') == 'log':
        filepath = recreate_csv_log(batch_number)
        new_file_name = "batch_{batch}_log.csv".format(batch=batch_number)
    else:
        abort(400)
        return
    return send_file(filename_or_fp=filepath, cache_timeout=-1, as_attachment=True, attachment_filename=new_file_name)


@bp.context_processor
def field_processor():
    """Functions available to jinja template"""
    def get_field_data(part_id, field_id):
        """ Gets the data for a field given the part id and field id"""
        pd = ProdData.query.filter_by(part_id=part_id, field_id=field_id).first()
        if pd is not None:
            return pd.field_data
        else:
            return ""

    return dict(get_field_data=get_field_data)
