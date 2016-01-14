According to K-Monitor's needs I made some modifications on this lil' kool tool:

**v1.1**

`service.py`:
* Added regex testing of "tax_nr" and "org_id" before addition, to ensure the result XML will not contain empty or invalid values.
* Added searching for "tender" blocks without "org_id"/"tax_nr" to extend the tool's functionality.
* Modified it to preserve original filename by storing it in the id.
* Saves also the timestamp of upload to inform the user.
* Also added a bunch of values to the rendered pages to provide more information for the user.

`templates/*.html`:
* Redesigned the whole thing using Bootstrap and Bootswatch Simplex theme.
* I changed nearly the whole HTML structure.

`templates/base.html`:
* Version number :-)
* Page title now shows filename.
* Header is followed by a breadcrumb thing to show the 3 main steps and the current filename to the user.
* Added a footer with links to the original and the forked repo.

`templates/download.html`:
* Added a sentence containing a link to the front page.

`templates/index.html`:
* Added a new panel below upload function where previously uploaded files are listed with upload time and action button (edit/download).

`templates/process.html`:
* Made some code formatting to increase readibilty.
* Moved `<form>` tag to fix HTML validity issue.
* Added fields "county", "region", "palyazo" to extend the tool's functionality.
* Enclosed all field blocks in if-s to print only what is existing.
* Moved "zip_code" to the first place.
* Save button tells the user how many blocks are waiting for input.
* I added a hint with a front page link.

Also I added `start.sh` and `stop.sh` to make it easier to run this thing in background.

All modifications were tested.

*Zsolt Jurányi, Petabyte Research Ltd.*