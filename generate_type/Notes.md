### Does repository follow conventional commit style?

[conventional commits detector](https://github.com/conventional-changelog/conventional-commits-detector)

1. [angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)

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

Number of conventional repositories:  510

Number of repositories per convention:
angular    473
eslint      27
ember        7
atom         2
jshint       1

```

```

Number of repositories per language:
JavaScript     129
TypeScript     112
C               72
Python          37
Go              35
C++             26
Java            22
Rust            10
Shell            9
PHP              7
Ruby             6
C#               5
Lua              4
HTML             4
Vue              3
Haskell          3
Groovy           2
PowerShell       2
Kotlin           2
Makefile         2
Lean             1
Scala            1
Starlark         1
TeX              1
Tcl              1
Objective-J      1
Erlang           1
SCSS             1
Dart             1
Nix              1
HCL              1
Objective-C      1
Stylus           1
Zig              1
Swift            1
V                1

```

- To test out the machine learning model. Select top 7 or 8 from JavaScript, TypeScript, Python. The full csv file for this repositories is [here](new_repositories.csv)

```

Total number of commits:  95901

```

```

                      name  criticality_score convention  conventional_commits
0                   gatsby            0.88809    angular                  9489
1               ant-design            0.87709    angular                  7255
2                 three.js            0.87063     eslint                  7822
3                   frappe            0.82136    angular                 11498
4               serverless            0.80944    angular                  2684
5                  vue-cli            0.77915    angular                  2855
6                  vuetify            0.75811    angular                  7049
7                 renovate            0.75585    angular                  8284
8              webpack-cli            0.75338    angular                  2021
9                sequelize            0.75117    angular                  1864
10              docusaurus            0.74669    angular                  2413
11                  quasar            0.74328    angular                  7133
12      webpack-dev-server            0.73795    angular                   647
13                    rxjs            0.72545    angular                  3921
14        electron-builder            0.72006    angular                  2003
15  graphql-code-generator            0.71901    angular                  1184
16                 typeorm            0.71463    angular                   691
17                     dvc            0.71078    angular                  3628
18             pyinstaller            0.67869    angular                  2181
19                 freeipa            0.67675    angular                  3265
20            ceph-ansible            0.66828    angular                  2136
21         trezor-firmware            0.65661    angular                  4890
22           sentry-python            0.64791    angular                   988

```

```

Top 20 conventional commit types:
fix              24827
chore            13814
feat             11067
docs              9096
refactor          4610
test              2586
tests             2023
build             1198
editor            1009
style              878
examples           878
ci                 766
dvc                755
webglrenderer      572
ipatests           525
doc                436
core               429
perf               411
site               394
webui              381

```

### Results from running the machine learning model

```

              precision    recall  f1-score   support

       chore       0.77      0.59      0.67      2350
        docs       0.71      0.76      0.73      1811
        feat       0.62      0.59      0.61      2206
         fix       0.69      0.82      0.75      4771
    refactor       0.67      0.36      0.47       917
        test       0.72      0.71      0.72       515

    accuracy                           0.69     12570
   macro avg       0.70      0.64      0.66     12570
weighted avg       0.69      0.69      0.69     12570

```