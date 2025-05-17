import os
import pandas as pd
import openai


def create_summary(comparison_dir:str, new_date:str, old_date:str):
    new_path = os.path.join(comparison_dir, f"new_products_{new_date}_{old_date}.csv")
    removed_path = os.path.join(comparison_dir, f"removed_products_{new_date}_{old_date}.csv")
    changed_path = os.path.join(comparison_dir, f"changed_products_{new_date}_{old_date}.csv")

    summary_parts = []

    for label, path in [("New products", new_path), ("Removed products", removed_path), ("Changed products", changed_path)]:
        if os.path.exists(path):
            df = pd.read_csv(path)
            text = df.head(10).to_markdown()  # or .to_string() for plain text
            summary_parts.append(f"## {label}\n{text}\n")
        else:
            summary_parts.append(f"## {label}\nNo entries found.\n")

    prompt = (
        "The following tables show changes in products on a veterinary webshop. "
        "Write a concise summary describing what changed, focusing on notable additions, removals, and updates.\n\n" +
        "\n".join(summary_parts)
    )

    # Call the LLM
    openai.api_key = os.getenv("OPENAI_API_KEY")  # set as a GitHub Secret
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content.strip()

    summary_path = os.path.join(comparison_dir, f"summary_{new_date}.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    return summary_path