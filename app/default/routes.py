from app.extensions import db
from app.prod_recording.export import recreate_csv_log, create_csv_from_data
from app.default import bp
from app.default.models import User, Batch, PartType
from datetime import datetime
from time import time
from flask import render_template, request, redirect, url_for, abort, send_file
from flask_login import current_user, login_required


@bp.route('/')
def default():
    return redirect(url_for('login.login'))


@bp.route('/index')
@login_required
def index():
    """ The default page """
    if current_user.is_authenticated:
        user = {'username': current_user.username, 'id': current_user.id}
    else:
        user = {'username': "nobody"}
    return render_template('index.html', title='Home', user=user)


@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    """ The default page for a logged-in user

    This will show the user the batches they are currently working on, as well as the option to start a new batch
    """

    if request.method == "POST":
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

    batches = current_user.batches
    batches_in_progress = []
    for b in batches:
        if not b.completed:
            batches_in_progress.append(b)
    admin = current_user.admin
    nav_bar_title = "Home - " + current_user.username
    return render_template('home.html',
                           nav_bar_title=nav_bar_title,
                           batches=batches_in_progress,
                           admin=admin)


@bp.route('/admin-home', methods=['GET', 'POST'])
@login_required
def admin_home():
    """The home page for a logged-in admin"""
    if not current_user.admin:
        return redirect(url_for('default.home'))

    # By default, get batches from the current month
    # This is overwritten if the user provides dates in a post request
    now = datetime.now()
    requested_month = now.month
    requested_year = now.year

    if request.method == "POST":
        try:
            action = request.form["action"]
        except Exception as e:
            print(e)
            abort(400)
            return

        if action == "alterDates":
            # Changes the month for which batches to show
            requested_month = int(request.form["month"])
            requested_year = int(request.form["year"])

        if action == "newPartType":
            # Create a new part type
            part_type = PartType()
            db.session.add(part_type)
            db.session.commit()
            return redirect(url_for("part_creation.create_part_type", part_type_id=part_type.id))
        if action == "copyPartType":
            # Create a new part type using an older part type as template
            part_type = PartType.query.get_or_404(request.form["partTypeId"])
            part_type_copy = part_type.clone_part_type()
            return redirect(url_for("part_creation.create_part_type", part_type_id=part_type_copy.id))

        if action == "deletePartType":
            # Delete a part type
            delete_part_type = PartType.query.get_or_404(request.form["partTypeId"])
            db.session.delete(delete_part_type)
            db.session.commit()
        if action == "deleteBatch":
            # Delete a batch
            delete_batch = Batch.query.get_or_404(request.form["batchId"])
            db.session.delete(delete_batch)
            db.session.commit()

        if action == "downloadData":
            # Download a batch's data in the form of a CSV file
            batch_id = request.form["batchId"]
            filepath = create_csv_from_data(batch_id)
            new_file_name = "batch_{batch}_data.csv".format(batch=batch_id)
            return send_file(filename_or_fp=filepath, cache_timeout=-1, as_attachment=True,
                             attachment_filename=new_file_name)

        if action == "downloadCsv":
            # Download any CSV data that has been uploaded for a batch
            batch_id = request.form["batchId"]
            filepath = recreate_csv_log(batch_id)
            new_file_name = "batch_{batch}_log.csv".format(batch=batch_id)
            return send_file(filename_or_fp=filepath, cache_timeout=-1, as_attachment=True,
                             attachment_filename=new_file_name)

    requested_batches_start = datetime(year=requested_year, month=requested_month, day=1, hour=0).timestamp()
    requested_batches_end = datetime(year=requested_year, month=requested_month + 1, day=1, hour=0).timestamp()
    batches = Batch.query.filter(Batch.created_timestamp.between(requested_batches_start, requested_batches_end))

    # Send all of the parts to the page
    part_types = PartType.query.all()
    users = User.query.all()

    nav_bar_title = "Admin Home"

    return render_template('admin-home.html',
                           requested_year=requested_year,
                           requested_month=requested_month,
                           current_year=now.year,
                           nav_bar_title=nav_bar_title,
                           part_types=part_types,
                           users=users,
                           batches=batches)
