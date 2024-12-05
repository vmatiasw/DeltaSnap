# Contributing to DeltaDB

We welcome contributions to the DeltaDB library! Before you begin, please ensure you follow these guidelines:

## Coding Standards

- **PEP 8**: Follow the Python style guide for clean and readable code.
- **PEP 257**: Use docstring conventions for documenting your code.
- **PEP 440**: Use semantic versioning for all releases.
- **PEP 345**: Ensure that your `setup.py` includes the proper metadata.
- **Black**: Use `black` to format the code automatically. Ensure that all code is formatted before committing.
- **Conventional Commits**: Follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages. Example of a commit message:
  - `feat(data_classes): add method to capture user data in the Change class`
  - `fix(SQLAlchemyMetadataAdapter): resolve issue with missing column in the SQLAlchemy adapter`
  
  Commit messages should be clear, concise, and use the imperative mood (e.g., "add", "fix", "update").

## How to Contribute

1. **Fork the repository**
2. **Clone your fork**
3. **Create a new branch**
   - Replace `feature/your-feature` with a descriptive name for the feature or fix you're working on.
4. **Make your changes**
   - Implement the feature or fix. Ensure that your changes follow the coding standards, including PEP 8, docstring conventions (PEP 257), and the use of **black** for formatting.
   - Run the tests to ensure your changes do not break existing functionality. If you are adding a new feature or fixing a bug, write tests as needed.
5. **Run tests**
   - Make sure all tests pass before committing your changes with `pytest`
   - If applicable, add new tests to ensure your changes are properly covered.
6. **Format your code**
   - Before committing, run `black` on your code to automatically format it according to the project's style.
7. **Commit your changes**
   - Once your changes are ready, commit them with a clear and concise message following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format.
8. **Push your changes**
   - Push your changes to your fork.
9. **Create a pull request**
   - Go to your forked repository on GitHub and click on "Compare & pull request".
   - Provide a detailed description of your changes in the pull request. Explain why the change is necessary and what problem it solves.
   - If applicable, reference any issues that the pull request addresses, using `Fixes #issue_number` or `Closes #issue_number`.
10. **Review and Merge**
    - Once your pull request is submitted, project maintainers will review it. Be prepared to discuss or make changes based on feedback.
    - If everything looks good, the maintainers will merge your pull request into the main repository.

We appreciate your contributions and thank you for helping make DeltaDB better!
