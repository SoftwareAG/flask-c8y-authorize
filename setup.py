from setuptools import setup, find_packages
setup(
	name = "flask_c8y_authorize",
	version = "1.3.0",
	description = "A library that helps to add RBAC for cumulocity in a flask based application.",
	author = "Nirmal Borah",
	author_email = "nirmal.borah@softwareag.com",
	url = "https://github.com/softwareag/flask-c8y-authorize",
	license = "Apache Software License",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Intended Audience :: Developers"
	],
	packages = find_packages(),
	python_requires= '>= 3.6',
	install_requires = [
		"flask==1.1.1",
    	"requests==2.22.0",
		"PyJWT==2.3.0"
	]
)