""" Detect the conventional style.

    guidelines:

    angular: https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
    atom: https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
    ember: https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md#pull-requests
    eslint: https://eslint.org/docs/developer-guide/contributing/pull-requests
    jshint: https://github.com/jshint/jshint/blob/master/CONTRIBUTING.md#commit-message-guidelines

    NOTE: jquery commit guidelines don't mention anything about the syntax for conventioanl commit
    types. Please see https://contribute.jquery.org/commits-and-pull-requests/#commit-guidelines.
    However commit message styles in jquery repository(https://github.com/jquery/jquery) seem to be following eslint
    conventional commit styles

"""

import re
from statistics import mode
from github import Github
import time
import urllib
import calendar
import json
import pandas as pd
import giturlparse
import collections
import statistics

def match(commit_msg):
    """Detremine which convention commit message is follwing"""
    # The regular expressions are adapted from https://github.com/conventional-changelog/conventional-commits-detector
    # Angular and eslint specify that commit tags must be one of the following
    commit_types = {

        "angular": "build|ci|docs|feat|fix|perf|refactor|test|chore|style",
        "eslint": "Fix|Update|New|Breaking|Docs|Build|Upgrade|Chore",

    }
    conventions = {

        "angular": r'^({})(?:\((.*)\))?: (.*)$'.format(commit_types["angular"]),
        "atom": r'^(:.*?:) (.*)$',
        "ember": r'^\[(.*) (.*)] (.*)$',
        "eslint": r'^({}): (.*?)(?:\((.*)\))?$'.format(commit_types["eslint"]),
        "jshint": r'^\[\[(.*)]] (.*)$',

    }
    
    temp_key = ""
    for key in conventions.keys():
        # Take subject line from the multiline commit messages
        if (re.match(conventions[key],commit_msg.split('\n')[0])):
            temp_key = key
            break
        else:
            # If commit message doesn't match any of the conventions return undefined
            temp_key = "undefined"

    return temp_key

def get_ratio(commit_messages):
    """Get frequency of the most common convention in the given commits"""
    #NOTE bug in case equal amounts
    conventions = [match(message) for message in commit_messages]
    convention = collections.Counter(conventions).most_common(1)
    ratio = (convention[0][0],convention[0][1]/len(conventions))

    return ratio

def wait(seconds):
    print("Waiting for {} seconds ...".format(seconds))
    time.sleep(seconds)
    print("Done waiting - resume!")

def api_wait(githb):
    rl = githb.get_rate_limit()
    current_time = calendar.timegm(time.gmtime())
    if  rl.core.remaining <= 10:  # extra margin of safety
        reset_time = calendar.timegm(rl.core.reset.timetuple())
        wait(reset_time - current_time + 10.0)
    elif rl.search.remaining <= 2:
        reset_time = calendar.timegm(rl.search.reset.timetuple())
        wait(reset_time - current_time + 10.0)

def get_repo_path(url):
    """Get full repository name from the url"""
    # The list of repositories that criticality_score gives has repository name but pygithub needs full path for repo
    parsed = giturlparse.parse(url)
    path = parsed.pathname[1:]
    return path

def is_conventional(urls):
    github = Github("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")
    
    i = 0
    conventions = []
    ratios = []
    while i < len(urls):
        path = get_repo_path(urls[i])
        repo = github.get_repo(path)
        commits = repo.get_commits()
        commit_messages = []

        try:
            for commit in commits[:100]:
                commit_messages.append(commit.commit.message)
            i+=1
        except:
            api_wait(github)
            continue

        convention = get_ratio(commit_messages)
        print(urls[i-1],convention[0],convention[1])
        conventions.append(convention[0])
        ratios.append(convention[1])

    return (conventions,ratios)

def select_repos():   
    """Select repositories for data collection"""
    # top 30 for Javascript and Typescript based on the conventional commit ratio
    # top 8 for Python and Go based on the conventional commit ratio
    repos = pd.read_csv("data/sorted_angular.csv",index_col=0)
    javascript = repos[repos.language == "JavaScript"].head(30)
    typescript = repos[repos.language == "TypeScript"].head(30)
    python = repos[repos.language == "Python"].head(8)
    go = repos[repos.language == "Go"].head(8)

    result = pd.concat([javascript,typescript,python,go])
    result.to_csv("data/selected_angular.csv")





# repos = repos[repos.convention == "angular"]
# sorted_repos = repos.sort_values(by ='ratio',ascending=False,kind='quicksort')
# print(sorted_repos.ratio)
# sorted_repos.to_csv("data/sorted_angular.csv")


# conventional = repos[repos.convention == "angular"]
# python = conventional[conventional.language == "JavaScript"]
# print(python[["url","ratio"]])



# #NOTE: function to select repositories

# grouped = data.groupby('language').head(20)

# selected_repos = grouped[grouped.language.isin(["JavaScript","TypeScript","Python"])]
# selected_repos.to_csv("data/selected_repos.csv")



# #NOTE: function to clone repositories
# # With gitpython
import git
# data = pd.read_csv("data/selected_repos.csv")
# for url in data.url:
#     print(url)
#     git.Git("./data/repositories").clone(url)



# NOTE: function to label repositories with conventions
# all_data = pd.read_csv("data/all.csv")
# top_data = all_data[all_data["criticality_score"] > 0.60]
# print(top_data)
# second_half = top_data[1000:]
# print(second_half)

# urls = second_half.url.tolist()
# i = 0
# conventions = []
# while i < len(urls):

#     path = giturlparse.parse(urls[i]).pathname[1:]
#     g = Github("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")
#     print(i,path)
    
#     repo = g.get_repo(path)

#     commits = repo.get_commits()

#     commit_messages = []
#     try:
#         for commit in commits[:50]:
#             commit_messages.append(commit.commit.message)
#         i+=1
#     except:
#          api_wait(g)
#          continue       

#     convention = detect(match(commit_messages))
#     print(convention)
#     print("---------------------------")
#     conventions.append(convention)

# second_half["convention"] = conventions
# second_half.to_csv("data/conventions_second_half.csv")

# def is_conventional(urls):
#     github = Github("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")
    
#     i = 0
#     conventional_repos = []
#     while i < len(urls):
#         try:
#             path = get_repo_path(urls[i])
#             l = github.search_code("\"commit message convention\" repo:{} language:Markdown".format(path))
#             if (l.totalCount > 0):
#                 conventional_repos.append(True)
                
#             else:
#                 conventional_repos.append(False)
#             i+=1
#         except:
#             api_wait(github)
#             continue
#     conventional["Markdown"] = conventional_repos
#     conventional.to_csv("data/angular.csv")

