from flask import flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_admin import BaseView, expose
from werkzeug.utils import secure_filename
import os


# Define a generic form for file upload
class FileUploadForm(FlaskForm):
    file = FileField("Upload file")
    submit = SubmitField("Submit")


class BaseImporterView(BaseView):
    """
    Base class for file upload views in Flask-Admin.
    """

    form_class = FileUploadForm  # Default form class for file uploads
    template = "admin/upload_template.html"  # Default template

    def get_processing_function(self):
        """
        Override this method in child classes to define the specific processing function.
        """
        raise NotImplementedError("Child classes must implement a processing function.")

    def get_file_extension(self):
        """
        Override this method in child classes to define accepted file extension.
        """
        raise NotImplementedError(
            "Child classes must implement accepted file extension check."
        )

    @expose("/", methods=["GET", "POST"])
    def upload(self):
        form = self.form_class()

        if form.validate_on_submit():
            file = form.file.data

            # Check file extension
            file_ext = self.get_file_extension()
            if file.filename.endswith(file_ext):
                # Ensure the 'uploads' directory exists
                upload_dir = "uploads"
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                # Save the file to a temporary location
                file_path = os.path.join(upload_dir, secure_filename(file.filename))
                file.save(file_path)

                # Call the processing function
                self.get_processing_function()(file_path)

                # Display success message
                flash(
                    f"{file_ext.upper()} file uploaded and processed successfully!",
                    "success",
                )
                return redirect(
                    url_for(".upload")
                )  # Redirect to the same page after success
            else:
                flash(
                    f"Invalid file format. Expected a {file_ext.upper()} file.",
                    "danger",
                )

        return self.render(self.template, form=form)
