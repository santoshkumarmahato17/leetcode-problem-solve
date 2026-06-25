import os
import json
import re

def format_stats_markdown(stats):
    """
    Formats the LeetCode stats and pie chart image into a clean, modern HTML/Markdown layout.
    """
    total_solved = stats["total_solved"]
    last_updated = stats["last_updated"]
    distribution = stats["topic_distribution"]
    
    # Generate table rows for topics
    topic_rows = ""
    for topic, count in distribution.items():
        # Humanize topic name for display if needed (e.g. DynamicProgramming -> Dynamic Programming)
        display_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', topic)
        topic_rows += f"            <tr><td><b>{display_name}</b></td><td align='center'><code>{count}</code></td></tr>\n"
        
    markdown_content = f"""<!-- START_LEETCODE_STATS -->
### 📊 LeetCode Progress & Stats

<div align="center">
  <table border="0" style="border-collapse: collapse; border: none; width: 100%;">
    <tr style="border: none;">
      <td width="50%" valign="top" style="border: none; padding-right: 15px;">
        <h4>🏆 Solved Problems Summary</h4>
        <ul>
          <li><b>Total Solved:</b> <code>{total_solved}</code></li>
          <li><b>Last Updated:</b> <code>{last_updated}</code></li>
        </ul>
        <h4>📂 Topic-wise Breakdowns</h4>
        <table style="width: 100%;">
          <thead>
            <tr>
              <th align="left">Topic</th>
              <th align="center">Solved Count</th>
            </tr>
          </thead>
          <tbody>
{topic_rows}          </tbody>
        </table>
      </td>
      <td width="50%" valign="top" align="center" style="border: none; padding-left: 15px;">
        <h4>📈 Topic Distribution Chart</h4>
        <img src="leetcode_stats.png" width="380px" alt="LeetCode Topic Distribution" />
      </td>
    </tr>
  </table>
</div>
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
    # In GitHub Actions, the script runs in the source repository folder
    # We will pass the target repository path as an argument or look for a default
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
        # Default fallback: check if target-repo directory exists in parent directory
        target_path = os.path.join(os.path.dirname(source_dir), "target-repo")
        
    if not os.path.exists(target_path):
        print(f"Warning: Target path {target_path} does not exist. Creating it...")
        os.makedirs(target_path, exist_ok=True)
        
    update_readme(target_path, stats)
