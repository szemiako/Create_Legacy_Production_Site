*What's it For?*
* Helps in quickly creating production sites on any legacy server.

*What do I need to Run it?*
You need the following prerequisites:
* python.exe needs to be added to the PATH environment variable.
* You will need to install chromedriver.
* This script uses non-built in packages: argparse, selenium

*How do I do it?*
* You can create one site on one server, or one site on many servers.
  ** In both cases, you need to first create a configuration file. Look at userguids.json for an example.
  ** Using this JSON, you can also create the same site on multiple servers (so long as the administrative user is created on each server).
* You can pass along arguments like command-line arguments. It takes the following arguments:
  * CompanyName
  * Configurations File
  * FirstName (Optional)
  * LastName (Optional)
* Then, execute it as: python create.py -cn "CompanyName" -cf "Configurations.JSON"
  ** See sample_usage.bat for some examples.
