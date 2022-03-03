import typer
from typing import Optional
import zipfile
import os
import tempfile
import datetime

app = typer.Typer()


@app.command()
def zip_modifier(zip_file_name, phrase_change_version_file, optional_parameter: Optional[str]=typer.Argument(None)):

    filename = 'version.txt'

    if not '.zip' in zip_file_name:
        zip_file_name = zip_file_name + '.zip'

    temp_zip_file = updated_file_in_zip(zip_file_name=zip_file_name,
                                        filename=filename, phrase_change_file=phrase_change_version_file)

    if optional_parameter == 'u':
        optional_file_name = 'updated.txt'
        current_date = datetime.date.today()

        updated_file_in_zip(
             zip_file_name=temp_zip_file,
             filename=optional_file_name,
             phrase_change_file=str(current_date)
         )


def updated_file_in_zip(zip_file_name, filename, phrase_change_file):

    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zip_file_name))
    os.close(tmpfd)

    # create a temp copy of the archive without filename

    with zipfile.ZipFile(zip_file_name, 'a') as zin:
        with zipfile.ZipFile(tmpname, 'a') as zout:
            zout.comment = zin.comment  # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zip_file_name)
    os.rename(tmpname, zip_file_name)

    # now add filename with its new data
    with zipfile.ZipFile(zip_file_name, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, phrase_change_file)

    return zip_file_name


if __name__ == "__main__":
    app()
