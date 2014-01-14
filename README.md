# Guardian Film experiments

This project defines experimental components and functionality for use in the Guardian Film section.

## Creating configuration data

You can use the Configuration model to store private details such as API keys.

To do this you also need to enable the remote shell feature by adding the following to your app.yaml:

	builtins:
	- remote_api: on

You can then connect to your shell and create the first piece of config:

	from models import Configuration
	config = Configuration(id="<your lookup key>" key="<your lookup key>", value="<your value>")
	config.put()

Once this value has been created you can then create other configuration via the Data Viewer.