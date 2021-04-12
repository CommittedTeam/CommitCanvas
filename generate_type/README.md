# How to run the experimentation

The current experimentation lets you train and validate the model on specified dataset.
User can run the experiment for all the repositories, specified repository, specified programming language, and get classification report for cross-project validation.

### Commands to run

- `poetry install`
- `poetry run commitcanvas classify [OPTIONS]`

    Available options:

    --name TEXT

    --language TEXT

    --cross / --no-cross  [default: False]

    --help                        Show this message and exit.

- name: repository name(String). Please see the list of available [repositories](data/repositories.txt)

- language: programming language(String). Please see the list of available [languages](data/languages.txt). By specifing the programming language `commitcanvas` will select all the repositories where dominant programming language is the one that user provided. If you select the programming language make sure to leave `name` option empty

- cross: (Boolean). If user selects True commitcanvas will run cross project validation and return classification report for each of the repositories. If you select `cross` option as True, then `name` option must be empty

### Sample commands and expected outputs

- `poetry run commitcanvas classify`

    Runs for all the repositories

    ```

                  precision    recall  f1-score   support

       chore       0.85      0.86      0.85       398
        docs       0.91      0.92      0.91       283
        feat       0.69      0.70      0.69       224
         fix       0.66      0.69      0.68       275
    refactor       0.70      0.63      0.66       179
       style       0.72      0.42      0.53        50
        test       0.87      0.97      0.92       113

    accuracy                           0.78      1522
   macro avg       0.77      0.74      0.75      1522
   weighted avg       0.78      0.78      0.78      1522

    ```

- `poetry run commitcanvas classify --language Python --cross`

    Cross project validation report for Python repositories

    ```
                                    name  precision    recall    fscore
    0         GatorEducator/gatorgrader   0.661952  0.593846  0.582896
    1             KeNaCo/auto-changelog   0.706639  0.668966  0.651500
    2       commitizen-tools/commitizen   0.697305  0.625000  0.628828
    3  relekang/python-semantic-release   0.672474  0.643243  0.648814
    4    tomtom-international/commisery   0.648548  0.582278  0.587164

    ```

- `poetry run commitcanvas classify --name GatorEducator/gatorgrader`

    Classifier trained and tested on one specified repository

    ```

                  precision    recall  f1-score   support

       chore       0.93      0.87      0.90        15
        docs       0.93      0.93      0.93        14
        feat       0.64      0.64      0.64        25
         fix       0.82      0.74      0.78        19
    refactor       0.55      0.61      0.58        18
       style       0.88      0.70      0.78        10
        test       0.84      0.93      0.89        29

    accuracy                           0.78       130
   macro avg       0.80      0.77      0.78       130
  weighted avg       0.78      0.78      0.78       130

    ```

### Sample invalid options

- `poetry run commitcanvas classify --name GatorEducator/gatorgrader --language Python`

    Error message:

    ```
    Error: Invalid value: If value for language is not empty, value for name must be empty
    ```

- `poetry run commitcanvas classify --name GatorEducator/gatorgrader --cross`

    Error message:

    ```
    Error: Invalid value: If value for cross is True, value for name must be empty
    ```








