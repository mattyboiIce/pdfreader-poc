DISCLAIMER:
This is a proof of concept tool. All of its output should be double checked by and individual with the expertise on what the expected outcomes should be.

To run the tool:
1. add pdf files to the pdfs-to-convert directory*
2. run `python3 pdfc.py`
3. access the newly created csvs from the converted-pdfs directory

NOTE:
*   I have not tested the limits of this script. I would start with 100 at a time and move up from there in 20-50 increments. until you reach a script execution timeout error and then go back 100 or so to be safe. 
* This system will convert ALL pdfs in the pdfs-to-convert directory, once you have converted all the pdfs in the directory REMOVE THEM FROM THE DIRECTORY.