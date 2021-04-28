import pandas as pd

# TODO: Get conventional commits count per repo and create separate file: name, url, language, conentional commits count

data = pd.read_feather("data/collected_data.ftr")
angular_data = data[["name", "language"]]
commit_types = data.name.value_counts()
df = commit_types.to_frame(name="conventional_commits")
df['name']=df.index
df = df.reset_index(drop=True)
repos = pd.read_csv("data/labeled_repos.csv",index_col=0)
repos = repos.drop(["ratio"],axis=1)
merged = pd.merge(df, repos, on='name')
merged = merged.drop_duplicates("name")
#merged.to_csv("data/angular_repos.csv")
print("total number of commits ", len(data))
print(data.commit_type.value_counts().head(20))

# NOTE: Repositories with high criticality score
# data = pd.read_csv("data/all.csv")
# print("Total number of repos: ",len(data.criticality_score))
# print("Mean Criticality Score: ",round(data.criticality_score.mean(),2))
# print("Median Criticality Score: ",round(data.criticality_score.median(),2))
# print("------------------------")
# top_data = data[data["criticality_score"] > 0.60]
# print("Number of repos with criticality score > 0.60: ",len(top_data.criticality_score))
# print("Mean Criticality Score: ",round(top_data.criticality_score.mean(),2))
# print("Median Criticality Score: ",round(top_data.criticality_score.median(),2))
# print("Ratio: ", round(len(top_data.criticality_score)/len(data.criticality_score),3))

# NOTE: Conventional repositories

data = pd.read_csv("data/angular_repos.csv")

print("Number of conventional repositories: ",len(data))
print("Number of repositories per convention:\n ", data.convention.value_counts())
print("Number of repositories per language:\n ", data.language.value_counts())


# NOTE: Conventional commits

# data = pd.read_feather("data/collected_data.ftr")
# print("Top 20 conventional commit types:\n ", data.commit_type.value_counts().head(20))

# import detect_type as dp

# all_data = pd.read_csv("data/all.csv")
# conventional = all_data[all_data["criticality_score"] > 0.60]
# ratios = dp.is_conventional(conventional.url.tolist())
# conventional["convention"] = ratios[0]
# conventional["ratio"] = ratios[1]
# conventional.to_csv("data/angular.csv")

# data = pd.read_csv("data/angular.csv")
# angular = data[data.convention == "angular"]
# print(angular.language.value_counts())
# print(angular.ratio.mean())
# print(angular.ratio.median())