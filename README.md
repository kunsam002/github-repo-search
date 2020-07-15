Github Repo Search
====================

## About

Github Repo Search retrieves information on repositories matching a provided search query and sorts the data according to the repository stars.

It is a mobile friendly application which also allows for further retrieval on details of individual repositories like recent commits, fork and fork user's bio.

## Bootstrapping Steps

Attached in this repository:
> python flask application file (app.py)

> html template files in the directory (templates)

> static web assets in form of css and js in the directory (static)

> notes, explanation and bootstrapping steps (cover.txt)

The application has two external dependencies
> virtual environment
> flask (micro framework)
> requests (simple HTTP library)
> python-dotenv

To Authenticate against Github providing more repositories to view (**Optional)
> Update the .env environment variable file in the project's root (**Optional)

```shell script
GitHub_USERNAME=<Your_Personal_GitHub_Username>
GitHub_PASSWORD=<Your_Personal_GitHub_password>
```

To run application, do the following:
``` git clone https://github.com/kunsam002/github-repo-search.git ```

> change directory to folder github-repo-search

> *One time execution (optional)* - Setup a virtualenv by running the command within the application directory
```shell script
virtualenv venv
```
> run the command line command; ``` source venv/bin/activate ```  to activate the virtual environment with the dependencies pre-installed

> *One time execution* - Install the dependencies and requirements 
```shell script
pip install -r requirements.txt
```
> run `python app.py` to start the application

> open a browser and do a search request to e.g. http://localhost:5000/

To run the test scripts:
> run the command within the active virtual environment

```shell script
python -s test_app.py
```

## Stack Used
Python (Flask),
Jinja2,
HTML,
CSS,
Javascript,
ReactJs

## Notes

There's a limit on the number of requests to the github API for unauthenticated requests.

## Contact

Mail me at kunsam002@gmail.com for more information
@github: kunsam002
@twitter: kunsam002
