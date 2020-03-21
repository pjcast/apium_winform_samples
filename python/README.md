

### Definitions


 - **Selenium**: Automation API for Web Applications
 - **Appium**: Selenium integration for testing Mobile / Desktop Apps
 - **Win App Driver**: Microsoft (closed source) appium driver for interacting with WPF, Winform applications. You do not need to install Appium/Selenium tools (outside of python support libs) - Win App Driver works standalone. Although, it can work through the other tools if needed.

**Required Installs**

 - Windows 10 - With developer mode enabled
 - Win App Driver - [Get from here](https://github.com/Microsoft/WinAppDriver/releases) - WindowsApplicationDriver.msi
 - Python 3.7 or newer - [Get from here](https://www.python.org/) - With following PIP modules
	 - python –m pip install Appium-Python-Client
	 - python –m pip install selenium
 - Visual Studio Code - [Get from here](https://code.visualstudio.com/)
	 - Python Extension (Install within IDE)
 - git
 - [Inspect.exe](https://docs.microsoft.com/en-us/windows/win32/winauto/inspect-objects)  and/or [UI  Recorder](https://github.com/Microsoft/WinAppDriver/releases)


**Required Windows Setting**
You must enable developer mode. Enable it through Settings and restart Windows Application Driver. Windows Settings / App Store - set to developer mode.

 
**Running from command line**

Start in a command prompt (and leave open) Win App Driver:
<pre><code>
C:\Program Files (x86)\Windows Application Driver>WinAppDriver.exe
Windows Application Driver listening for requests at: http://127.0.0.1:4723/
Press ENTER to exit.
</code></pre>


Information from WebAppDriver repository (check https://github.com/microsoft/WinAppDriver/blob/master/Docs/AuthoringTestScripts.md for latest)

| Client API                   	| Locator Strategy 	| Matched Attribute in inspect.exe       	| Example      	|
|------------------------------	|------------------	|----------------------------------------	|--------------	|
| FindElementByAccessibilityId 	| accessibility id 	| AutomationId                           	| AppNameTitle 	|
| FindElementByClassName       	| class name       	| ClassName                              	| TextBlock    	|
| FindElementById              	| id               	| RuntimeId (decimal)                    	| 42.333896.3.1	|
| FindElementByName            	| name             	| Name                                   	| Calculator   	|
| FindElementByTagName         	| tag name         	| LocalizedControlType (upper camel case)	| Text         	|
| FindElementByXPath           	| xpath            	| Any                                    	| //Button[0]  	|

## Supported Capabilities

Below are the capabilities that can be used to create Windows Application Driver session.

| Capabilities       	| Descriptions                                          	| Example                                               	|
|--------------------	|-------------------------------------------------------	|-------------------------------------------------------	|
| app                	| Application identifier or executable full path        	| Microsoft.MicrosoftEdge_8wekyb3d8bbwe!MicrosoftEdge   	|
| appArguments       	| Application launch arguments                          	| https://github.com/Microsoft/WinAppDriver             	|
| appTopLevelWindow  	| Existing application top level window to attach to    	| `0xB822E2`                                            	|
| appWorkingDir      	| Application working directory (Classic apps only)     	| `C:\Temp`                                             	|
| platformName       	| Target platform name                                  	| Windows                                               	|
| platformVersion    	| Target platform version                               	| 1.0                                                       |

