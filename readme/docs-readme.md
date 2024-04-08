# Installation for documentation
The documentation of the whole project is done by using the `sphinx` library in python.

## To start the docs
1. install the necessary documentation libraries required which are inside the `./requirements/docs-requirements.txt`.
2. enter the command 
    ```bash
    <projectdir> > sphinx-quickstart docs
    ```
    you'll be prompted to a series of question relating to the project and provide the relevant information.
3. now you have a folder docs, navigate inside the directory then enter the following command.
    ```bash
    <projectdir>\docs > make.bat html
    ```
    This will create a directory `html` inside of build. Open up the `index.html` in a browser, you'll be provided with a basic documentation page. 
4. To build `.rst` files of your modules and files, execute the following command 
    ```bash
    <projectdir>> sphinx-apidoc -o docs <specific-modules-to-build>

    OR
    <projectdir>> sphinx-apidoc -o docs . # to build all
    ```
    reStructuredText(.rst) is the default plaintext markup language used by Sphinx. 

5. Add the following code snippet to the `conf.py` present inside docs.
    ```python
    import os 
    import sys
    sys.path.insert(0, os.path.abspath('..')) # sets the file path in root directory of the project
    ```

6. After executing the command in the 4th point, you'll get `.rst` files of your modules, along with a `modules.rst` file. Inside of the `index.rst` file add the follwoing snippet.
    ```
    .. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules # add this as it contains all the modules in the project
    ```

7. Again build the document with the following command. First navigate inside of the `docs` directory. And run the `make html` 
    ```bash
    <projectdir>\docs > make.bat html
    ```

## to document your modules, class or methods use the following docstring style.

```python
def method(*args, **kwargs):
    """[Summary]

    :param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
    :type [ParamName]: [ParamType](, optional)
    ...
    :raises [ErrorType]: [ErrorDescription]
    ...
    :return: [ReturnDescription]
    :rtype: [ReturnType]
    """
    # code statements
    ... 
```