# Contributing

Before contributing, please discuss your changes with others by either taking care of an existing unassigned issue, creating a new issue or discussing your changes in our Discord server.

Please keep in mind that you must respect the code of conduct at all times when contributing to the project.

## Version control branching
- Always make a new branch for your work. You will then be able to create a pull request that will have to be reviewed by other contributors in order to merge your work.
- New features and bugfixes should branch off of the  `main` branch.
- Include your issue number in your commits (e.g. `#16 - Added validation for strategy starting data`)
- Each pull request/branch should only include changes from **one** issue, otherwise it may be rejected.

## Coding practices
- Follow the [PEP-8 guidelines](https://www.python.org/dev/peps/pep-0008/) and the general style found in existing code.    
- Do not include any API tokens or any other kind of sensitive information in your code.
    - You can use the `.env` file to retrieve this kind of information in your tests. You should then add the required key in the `.env.sample` file.

## Documentation
This project follows [Google's docstrings style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html). 

Document as much as you can new features and existing features that you are modifying. A lack of documentation may result in your pull request being rejected.

## Testing
We encourage you to make tests for any new features and update existing tests when modifying features.

A test-driven development approach allows us to quickly make sure that any changes made to the code do not break existing features.