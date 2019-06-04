# Sublime_Environment
Environment to be synced with ..\AppData\Roaming\Sublime Text 3\Packages\User for use of Sublime as a consistent Python IDE



1. Set the default settings as stored in:
	https://drive.google.com/drive/folders/1T0D2_ZzdRLHAZZpQfBPQZmVRZUFJlMHH?usp=sharing
	(See default_settings_summary.json for details of the necessary changes to the default settings for this IDE)

2. Set the system Environment Variables as required:
{
	"HOME": "%USERPROFILE%\AppData\Local\Programs\Python\Python36",
	"Path": [
		"%USERPROFILE%\AppData\Local\Programs\Python\Python36\",
		"%USERPROFILE%\AppData\Local\Programs\Python\Python36\Scripts\",
		"C:\xampp\php\php.exe"
	]
	"PYTHON_HOME": "%USERPROFILE%\AppData\Local\Programs\Python\Python36"
}

3. Ensure that the Build system is set to Python-REPL
