import json


with open(
    "eval_results.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)


for experiment_id, experiment in data.items():

    print("\n" + "=" * 80)
    print(experiment["config_name"])
    print("=" * 80)

    summary = experiment["summary"]

    for category in [
        "policy",
        "out_of_scope",
        "adversarial"
    ]:

        values = summary[category]

        print(f"\n{category}")

        print(
            f"Keyword: "
            f"{values['keyword_passes']}/"
            f"{values['total']}"
        )

        print(
            f"Judge: "
            f"{values['judge_passes']}/"
            f"{values['total']}"
        )

        print(
            f"ROUGE-L: "
            f"{values['average_rouge_l']:.3f}"
        )

        print(
            f"Judge Score: "
            f"{values['average_judge_score']:.2f}/5"
        )