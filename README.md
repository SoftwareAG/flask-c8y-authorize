# flask-c8y-authorize
## How to use
1. Install it from github using pip
  ```bash
  pip install git+https://github.com/SoftwareAG/flask-c8y-authorize
  ```
2. Import it to your script
  ```python
  from flask_c8y_authorize import PreAuthorize
  ```
3. Use the decorator with the API route
  ```python
  from flask import Flask
  from flask_c8y_authorize import PreAuthorize
  
  app = Flask(__name__)
  
  @app.route('/test')
  @PreAuthorize.has_role('ROLE_TEST_READ')
  def test():
    return "Ok"
  ```
**Note** - The decorator can be turned on/off using app configuration. See the below example -
```python
from flask import Flask
from flask_c8y_authorize import PreAuthorize

app = Flask(__name__)
app.config["flask_c8y_pre_authorize_enabled"] = False #True or False. Default value is True
    
@app.route('/test')
@PreAuthorize.has_role('ROLE_TEST_READ')
def test():
    return "Ok"
```
## There are total three decorators
* ```@PreAuthorize.has_role("ROLE_TEST_READ")``` - Validates for a specific role
* ```@PreAuthorize.has_all_roles(["ROLE_TEST_READ", "ROLE_TEST_WRITE"])``` - Validates for all the roles
* ```@PreAuthorize.has_any_role(["ROLE_TEST_READ", "ROLE_TEST_WRITE"])``` - Validates for any of the roles

## **Note - Currently, it supports only basic auth.**

______________________
These tools are provided as-is and without warranty or support. They do not constitute part of the Software AG product suite. Users are free to use, fork and modify them, subject to the license agreement. While Software AG welcomes contributions, we cannot guarantee to include every contribution in the master project.

Contact us at [TECHcommunity](mailto:technologycommunity@softwareag.com?subject=Github/SoftwareAG) if you have any questions.
