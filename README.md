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
  
  @PreAuthorize.has_role("ROLE_TEST_READ")
  @app.route("/test")
  def test():
    return "Ok"
  ```
