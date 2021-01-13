# pylint: disable = import-error
import rules

class Check:
    def check_rules(self):
        targets = rules.Commit.__subclasses__()
        for target in targets:
            commitcanvas_rules = (target.__subclasses__())
            for rule in commitcanvas_rules:
                commit_rule = rule()
                error = commit_rule.check()
                if error is not None:
                    print(error)

c = Check()
c.check_rules()