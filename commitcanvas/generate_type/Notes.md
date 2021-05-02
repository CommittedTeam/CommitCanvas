### Does repository follow conventional commit style?

[conventional commits detector](https://github.com/conventional-changelog/conventional-commits-detector)

1. [angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
https://docs.google.com/document/d/1QrDFcIiPjSLDn3EL15IJygNPiHORgU1_OOAqWjiDU5Y/edit#heading=h.z8a3t6ehl060

2. [atom](https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages)

3. [ember](https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md#pull-requests)

4. [eslint](https://eslint.org/docs/developer-guide/contributing/pull-requests)

5. [jshint](https://github.com/jshint/jshint/blob/master/CONTRIBUTING.md#commit-message-guidelines)

[jquery](https://contribute.jquery.org/commits-and-pull-requests/#commit-guidelines)

### Select repositories and collect data

- Use this [file](data/all.csv), that has list of repositories, with criticality scores. The file is from [criticality_score](https://github.com/ossf/criticality_score) repo.

```

Total number of repos:  102507
Mean Criticality Score:  0.27
Median Criticality Score:  0.24

```
- Select repositories with criticality score higher than 0.60

```

Number of repos with criticality score > 0.60:  3400
Mean Criticality Score:  0.67
Median Criticality Score:  0.65
Ratio(top_repos/total_repos):  0.033

```

- Label repositories with conventional tags

```

Number of conventional repositories: 200

```

```
Number of repositories per language:
JavaScript     74
TypeScript     71
Python         16
Go              9
Java            8
C++             3
Shell           3
C#              2
Rust            2
C               2
Ruby            2
Vue             2
SCSS            1
HTML            1
PHP             1
Objective-C     1
Haskell         1
Groovy          1
Lua             1
OCaml           1
TeX             1
Starlark        1
Lean            1
Name: language, dtype: int64

```

- The full csv file for this repositories is [here](data/angular_repos.csv)

```

total number of conventional commits 458986


     conventional_commits                  name  ... criticality_score convention
0                   20267               angular  ...           0.87075    angular
1                   14347                sentry  ...           0.77036    angular
2                   13069  camunda-bpm-platform  ...           0.66856    angular
3                   10603                frappe  ...           0.82136    angular
4                    9522                gatsby  ...           0.88809    angular
..                    ...                   ...  ...               ...        ...
219                   146       cordova-android  ...           0.63819    angular
220                   111             fabric.js  ...           0.61575    angular
221                   103       sendgrid-nodejs  ...           0.65542    angular
222                    81                agenda  ...           0.63838    angular
223                    73       sendgrid-python  ...           0.61219    angular

[205 rows x 18 columns]

```

```

Top 20 conventional commit types:
fix         127815
chore       111597
feat         69825
docs         45512
refactor     22394
test         15840
build        14385
ci            4203
style         3596
ref           3027
perf          2538
doc           1964
tests         1596
wip           1169
release       1054
r              826
feature        740
browser        689
all            650
python         578

```

- [angular](https://github.com/angular/angular)

```

              precision    recall  f1-score   support

       chore       0.61      0.46      0.52       237
        docs       0.85      0.93      0.89       998
        feat       0.71      0.54      0.61       581
         fix       0.68      0.82      0.75      1258
    refactor       0.72      0.61      0.66       699
        test       0.75      0.68      0.71       269

    accuracy                           0.74      4042
   macro avg       0.72      0.67      0.69      4042
weighted avg       0.74      0.74      0.73      4042

```

- [serverless](https://github.com/serverless/serverless)

```

              precision    recall  f1-score   support

       chore       0.92      0.97      0.94        86
        docs       0.98      0.92      0.95        62
        feat       0.76      0.69      0.72        64
         fix       0.80      0.75      0.77       107
    refactor       0.74      0.81      0.77       117
        test       0.91      0.93      0.92        44

    accuracy                           0.83       480
   macro avg       0.85      0.84      0.85       480
weighted avg       0.83      0.83      0.83       480

```