import os
import json
import re

def format_stats_markdown(stats):
    """
    Formats the LeetCode stats into a clean, modern native Markdown layout
    using a dynamic Mermaid pie chart.
    """
    total_solved = stats["total_solved"]
    last_updated = stats["last_updated"]
    distribution = stats["topic_distribution"]
    
    # Filter out categories with 0 solved problems for the chart
    filtered_dist = {k: v for k, v in distribution.items() if v > 0}
    
    # Generate table rows for topics
    topic_rows = ""
    for topic, count in distribution.items():
        # Humanize topic name for display (e.g. DynamicProgramming -> Dynamic Programming)
        display_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', topic)
        topic_rows += f"| {display_name} | `{count}` |\n"
        
    # Generate Mermaid slices
    mermaid_slices = ""
    for topic, count in filtered_dist.items():
        display_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', topic)
        mermaid_slices += f'    "{display_name}" : {count}\n'
        
    markdown_content = f"""<!-- START_LEETCODE_STATS -->
### 📊 LeetCode Progress & Stats

#### 🏆 Solved Problems Summary
- **Total Solved:** `{total_solved}`
- **Last Updated:** `{last_updated}`

#### 📈 Topic-wise Distribution Chart
```mermaid
pie title Topic-wise Distribution
{mermaid_slices}```

#### 📂 Topic-wise Breakdowns
| Topic | Solved Count |
| :--- | :---: |
{topic_rows}
<!-- END_LEETCODE_STATS -->"""

    return markdown_content

def update_readme(target_repo_path, stats):
    """
    Updates the README.md in the target repository.
    Supports README.template.md substitution first, then fallback modes.
    """
    stats_md = format_stats_markdown(stats)
    
    template_path = os.path.join(target_repo_path, "README.template.md")
    readme_path = os.path.join(target_repo_path, "README.md")
    
    # Mode 1: README.template.md exists
    if os.path.exists(template_path):
        print(f"Template found at {template_path}. Generating README.md from template...")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Replace template placeholders
        if "<!-- START_LEETCODE_STATS -->" in template_content and "<!-- END_LEETCODE_STATS -->" in template_content:
            # Replace between markers
            pattern = re.compile(
                r"<!--\s*START_LEETCODE_STATS\s*-->.*?<!--\s*END_LEETCODE_STATS\s*-->", 
                re.DOTALL
            )
            new_content = pattern.sub(stats_md, template_content)
        elif "{{LEETCODE_STATS}}" in template_content:
            new_content = template_content.replace("{{LEETCODE_STATS}}", stats_md)
        else:
            # If no placeholders, append to template content
            new_content = template_content + "\n\n" + stats_md
            
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated README.md from template.")
        return
        
    # Mode 2: README.md exists, update between markers
    if os.path.exists(readme_path):
        print(f"README.md found at {readme_path}. Looking for markers...")
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            
        if "<!-- START_LEETCODE_STATS -->" in readme_content and "<!-- END_LEETCODE_STATS -->" in readme_content:
            pattern = re.compile(
                r"<!--\s*START_LEETCODE_STATS\s*-->.*?<!--\s*END_LEETCODE_STATS\s*-->", 
                re.DOTALL
            )
            new_content = pattern.sub(stats_md, readme_content)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully updated LeetCode stats section in README.md.")
        else:
            # Markers not found, append to existing README
            print("Markers not found. Appending LeetCode stats to the end of README.md.")
            new_content = readme_content.strip() + "\n\n" + stats_md + "\n"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Appended LeetCode stats section.")
        return
        
    # Mode 3: No README files exist, create a new one from scratch
    print("No README.template.md or README.md found. Creating a new README.md from scratch...")
    default_readme = f"""# LeetCode Dashboard

My automated LeetCode statistics tracking dashboard.

{stats_md}
"""
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(default_readme)
    print("Created new README.md with LeetCode stats.")

if __name__ == "__main__":
    import sys
    
    source_dir = os.path.dirname(os.path.abspath(__file__))
    stats_json_path = os.path.join(source_dir, "stats.json")
    
    if not os.path.exists(stats_json_path):
        print(f"Error: {stats_json_path} does not exist. Run generate_stats.py first.")
        sys.exit(1)
        
    with open(stats_json_path, 'r', encoding='utf-8') as f:
        stats = json.load(f)
        
    # Get target repository path from arguments, fallback to parent directory/target-repo
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = os.path.join(os.path.dirname(source_dir), "target-repo")
        
    if not os.path.exists(target_path):
        print(f"Warning: Target path {target_path} does not exist. Creating it...")
        os.makedirs(target_path, exist_ok=True)
        
    update_readme(target_path, stats)
