"""Various metrics from Pydriller."""
# pylint: disable = import-error
from pydriller import RepositoryMining

REPO = RepositoryMining("https://github.com/GatorEducator/gatorgrader")
for commit in REPO.traverse_commits():
    print(
        "| {} | {} | {} | {} |".format(
            commit.msg,
            commit.dmm_unit_size,
            commit.dmm_unit_complexity,
            commit.dmm_unit_interfacing,
        )
    )

    for modif in commit.modifications:
        print("| {} | {} |".format(modif.complexity, modif.change_type.name,))
        for method in modif.changed_methods:
            print("| {} |".format(method.name))
