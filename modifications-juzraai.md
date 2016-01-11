According to K-Monitor's needs I made some modifications on this lil' kool tool:

**v1.1**

`service.py`:
* Added regex testing of "tax_nr" and "org_id" before addition, to ensure the result XML will not contain empty or invalid values.
* Added searching for "tender" blocks without "org_id"/"tax_nr" to extend the tool's functionality.
* Modified it to preserve original filename.

`templates/process.html`:
* Made some code formatting to increase readibilty.
* Moved `<form>` tag to fix HTML validity issue.
* Added fields "county", "region", "palyazo" to extend the tool's functionality.
* Enclosed all field blocks in if-s to print only what is existing.
* Moved "zip_code" to the first place.

`templates/base.html`:
* Version number :-)

Also I added `start.sh` and `stop.sh` to make it easier to run this thing in background.

All modifications were tested.

*Zsolt Jurányi, Petabyte Research Ltd.*