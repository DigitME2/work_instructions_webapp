from app import db
from app.part_creation import bp
from app.part_creation.forms import NewPartTypeForm
from app.default.models import Batch, Step, Field, PartType
from flask import current_app, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required
import os


@bp.route('/createparttype', methods=['GET', 'POST'])
@login_required
def create_part_type():
    """The page to create a part type"""

    form = NewPartTypeForm()
    part_type_id = request.args.get("part_type_id")
    part_type = PartType.query.filter_by(id=part_type_id).first()
    # Create a list of steps for the part
    steps = Step.query.filter_by(part_type_id=part_type_id).all()
    steps.sort(key=lambda step: step.step_number)

    if form.validate_on_submit():
        part_type.part_name = form.part_name.data
        db.session.commit()

    # Fill in the part name form to the current part name
    form.part_name.data = part_type.part_name

    return render_template('createparttype.html',
                           part_type=part_type,
                           steps=steps,
                           form=form)


@bp.route('/newparttype', methods=['POST'])
@login_required
def new_part_type():
    part_type = PartType(part_name="New Part")
    db.session.add(part_type)
    db.session.commit()
    return redirect(url_for('part_creation.create_part_type', part_type_id=part_type.id))


@bp.route('/editstep', methods=['GET', 'POST'])
@login_required
def edit_step():
    """The page to edit a step for a part"""

    try:
        part_type_id = request.args.get("part_type_id")
        step_id = request.args.get("step_id")
    except:
        abort(400)
        return
    # Send the user back if the part is uneditable
    if step_id is None or part_type_id is None:
        abort(400)
        return

    part_type = PartType.query.get_or_404(part_type_id)

    if Batch.query.filter_by(part_type_id=part_type_id).first() is not None:
        flash("Parts already exist for this part type, and it can no longer be edited.", category="top")
        return redirect(request.referrer)
    step = Step.query.get_or_404(step_id)
    fields = Field.query.filter_by(step_id=step_id).all()
    # Form is an image upload
    if request.method == 'POST':
        # Save the step info
        step.step_title = request.form['stepTitle']
        step.step_instructions = request.form['stepInstructions']

        # Check if a CSV upload is required
        if 'importCsvCheckbox' in request.form:
            step.csv_upload = True
        else:
            step.csv_upload = False

        # Upload the image
        if 'image' in request.files:
            image = request.files['image']
            # Check the image has the correct file extension
            fn, file_extension = os.path.splitext(image.filename)
            if file_extension not in current_app.config['ALLOWED_EXTENSIONS']:
                flash("Incorrect file extension", category="top")
                return redirect(request.referrer)
            # Create the directory if it doesn't exist
            directory = '/'.join([current_app.config['UPLOAD_FOLDER'], part_type.part_name])
            if not os.path.exists(directory):
                os.mkdir(directory)
            filename = "step" + str(step.step_number) + file_extension
            # Delete the image if one already exists
            if os.path.isfile('/'.join([directory, filename])):
                try:
                    os.remove('/'.join([directory, filename]))
                except OSError:
                    pass
            # Save the image
            image.save('/'.join([directory, filename]))
            # Save the location of the image to the database for retrieval
            step.step_image = '/'.join(["/static/images", part_type.part_name, filename])

        db.session.commit()

    nav_bar_title = str(part_type.part_name) + " - " + "Step " + str(step.step_number)
    return render_template('step.html',
                           nav_bar_title=nav_bar_title,
                           part_type=part_type,
                           step=step,
                           fields=fields)


@bp.route('/addstep', methods=['POST'])
@login_required
def add_step():
    """Adds a new step for a part"""

    part_type_id = request.form["part_type_id"]

    # Check that a batch hasn't been created with this part type
    if Batch.query.filter_by(part_type_id=part_type_id).first() is not None:
        flash("Parts already exist for this part type, and it can no longer be edited.", category="top")
        return redirect(request.referrer)

    steps = Step.query.filter_by(part_type_id=part_type_id).all()

    # Find the next step number
    # = 1 if there are no steps
    if len(steps) == 0:
        new_step_number = 1
    else:
        new_step_number = max(s.step_number for s in steps) + 1
    # Create the default Step title
    step_title = "Step " + str(new_step_number)
    step_instructions = ""
    step = Step(part_type_id=part_type_id,
                step_number=new_step_number,
                step_title=step_title,
                step_instructions=step_instructions)
    db.session.add(step)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/deletestep', methods=['POST'])
@login_required
def delete_step():
    part_type_id = request.form["part_type_id"]
    steps = Step.query.filter_by(part_type_id=part_type_id).all()
    # Check that a batch hasn't been created with this part type
    if Batch.query.filter_by(part_type_id=part_type_id).first() is not None:
        flash("Parts already exist for this part type, and it can no longer be edited.", category="top")
        return redirect(request.referrer)

    if len(steps) == 0:
        return redirect(request.referrer)
    else:
        # Delete the final step
        steps.sort(key=lambda step: step.step_number)
        last_step = steps[-1]
        db.session.delete(last_step)
        db.session.commit()
        return redirect(request.referrer)


@bp.route('/savedatafield', methods=['POST'])
@login_required
def save_field():
    """ The POST request to add a data field when editing a step"""
    field_name = request.json.get("field_name")
    step_id = request.json.get("step_id")
    batch_wide = request.json.get("batch_wide")
    f = Field(field_name=field_name, step_id=step_id, batch_wide=batch_wide)
    db.session.add(f)
    db.session.commit()
    return '', 201


@bp.route('/deletedatafield', methods=['POST'])
@login_required
def delete_field():
    """ The POST request to delete a data field during creation of a step"""
    field_name = request.json.get("field_name")
    step_id = request.json.get("step_id")
    field = Field.query.filter_by(field_name=field_name, step_id=step_id).first()
    db.session.delete(field)
    db.session.commit()
    return '', 201
