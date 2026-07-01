import os
import json
import re
import math
from datetime import datetime, timezone

# Target topics to track
TARGET_TOPICS = [
    "Arrays",
    "Strings",
    "Trees",
    "Graphs",
    "DynamicProgramming",
    "LinkedList",
    "Stack",
    "Queue",
    "HashMap"
]

# Mapping from README headers/tags to target topics
TOPIC_MAPPING = {
    "Array": "Arrays",
    "String": "Strings",
    "Tree": "Trees",
    "Binary Tree": "Trees",
    "Binary Search Tree": "Trees",
    "Graph": "Graphs",
    "Depth-First Search": "Graphs",
    "Breadth-First Search": "Graphs",
    "Dynamic Programming": "DynamicProgramming",
    "Linked List": "LinkedList",
    "Stack": "Stack",
    "Monotonic Stack": "Stack",
    "Queue": "Queue",
    "Heap (Priority Queue)": "Queue",
    "Monotonic Queue": "Queue",
    "Hash Table": "HashMap",
    "HashMap": "HashMap",
    "Hash Map": "HashMap"
}

def count_all_solved_problems(repo_path):
    """
    Counts unique directories matching the LeetCode problem pattern (e.g. 0011-container-with-most-water)
    anywhere in the repository.
    """
    solved = set()
    for root, dirs, _ in os.walk(repo_path):
        # Don't descend into hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for d in dirs:
            if re.match(r'^\d{4}-', d):
                solved.add(d)
    return len(solved)

def get_problems_in_folder(folder_path):
    """
    Returns unique problem directories or solutions in a given folder.
    """
    problems = set()
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return problems
    
    for item in os.listdir(folder_path):
        if item.startswith('.'):
            continue
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path) and re.match(r'^\d{4}-', item):
            problems.add(item)
        elif os.path.isfile(full_path):
            name, ext = os.path.splitext(item)
            # Exclude standard files
            if name.lower() not in ['readme', 'stats', 'generate_stats', 'generate_readme', 'requirements'] and ext in ['.py', '.cpp', '.java', '.c', '.js', '.ts', '.go', '.rs']:
                problems.add(name)
    return problems

def parse_readme_topics(readme_path):
    """
    Parses the main README.md to extract problem lists and their links under topic headings.
    """
    topic_problems = {}
    if not os.path.exists(readme_path):
        return topic_problems
        
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract topics between LeetCode Topics Start and End comments if present
    start_tag = "<!---LeetCode Topics Start-->"
    end_tag = "<!---LeetCode Topics End-->"
    if start_tag in content and end_tag in content:
        content = content.split(start_tag)[1].split(end_tag)[0]
        
    lines = content.split('\n')
    current_topic = None
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            current_topic = line[3:].strip()
            topic_problems[current_topic] = {}
        elif current_topic and line.startswith('| [') and '](http' in line:
            match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                problem_name = match.group(1)
                problem_url = match.group(2).replace("/tree/master/", "/tree/main/").replace("/blob/master/", "/blob/main/")
                topic_problems[current_topic][problem_name] = problem_url
                
    return topic_problems

def generate_stats_data(repo_path):
    """
    Compiles problem counts for all target topics and overall total.
    """
    solved_by_topic = {topic: {} for topic in TARGET_TOPICS}
    
    # 1. Attempt to count from folder structure (nested under target topic folders)
    folder_exists_and_not_empty = False
    for topic in TARGET_TOPICS:
        topic_path = os.path.join(repo_path, topic)
        if os.path.isdir(topic_path):
            probs = get_problems_in_folder(topic_path)
            if probs:
                for p in probs:
                    url = f"https://github.com/santoshkumarmahato17/leetcode-problem-solve/tree/main/{topic}/{p}"
                    solved_by_topic[topic][p] = url
                folder_exists_and_not_empty = True
                
    # 2. Fallback: Parse README.md topic-wise markdown mapping
    if not folder_exists_and_not_empty:
        print("Folder structure not found or empty. Falling back to parsing README.md...")
        readme_path = os.path.join(repo_path, "README.md")
        parsed_topics = parse_readme_topics(readme_path)
        for parsed_topic, problems in parsed_topics.items():
            mapped_topic = TOPIC_MAPPING.get(parsed_topic)
            if mapped_topic in solved_by_topic:
                for p, url in problems.items():
                    solved_by_topic[mapped_topic][p] = url
                    
    # Format counts and total
    distribution = {topic: len(solved_by_topic[topic]) for topic in TARGET_TOPICS}
    total_solved = count_all_solved_problems(repo_path)
    
    # In case total_solved is 0 but we found topics in README
    readme_total = len(set().union(*(solved_by_topic[t].keys() for t in TARGET_TOPICS)))
    if total_solved == 0 and readme_total > 0:
        total_solved = readme_total

    # Format problems list for JSON
    problems_json = {}
    for topic in TARGET_TOPICS:
        problems_json[topic] = []
        sorted_probs = sorted(solved_by_topic[topic].keys())
        for p in sorted_probs:
            problems_json[topic].append({
                "name": p,
                "url": solved_by_topic[topic][p]
            })

    # Current local time formatted nicely
    now = datetime.now(timezone.utc).astimezone()
    last_updated = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    return {
        "total_solved": total_solved,
        "topic_distribution": distribution,
        "problems_by_topic": problems_json,
        "last_updated": last_updated
    }

def generate_svg_file(stats_data, output_path, is_dark_mode=False):
    """
    Generates a beautifully styled SVG file with specific color mapping depending on theme mode.
    """
    distribution = stats_data["topic_distribution"]
    filtered_dist = {k: v for k, v in distribution.items() if v > 0}
    total_val = sum(filtered_dist.values())
    
    width = 480
    height = 280
    cx = 150
    cy = 140
    R = 90
    r = 50
    
    # Static theme settings
    if is_dark_mode:
        bg_color = "none"
        stroke_color = "#0d1117"
        text_color = "#c9d1d9"
        border_color = "none"
        title_color = "#f0f6fc"
    else:
        bg_color = "none"
        stroke_color = "#ffffff"
        text_color = "#24292f"
        border_color = "none"
        title_color = "#1f2328"
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    rect.card-bg {{
      fill: {bg_color};
      stroke: {border_color};
      stroke-width: 0;
      rx: 8px;
    }}
    text {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }}
    text.title {{
      fill: {title_color};
      font-size: 16px;
      font-weight: 600;
      text-anchor: middle;
    }}
    text.label {{
      fill: {text_color};
      font-size: 11px;
      font-weight: 600;
    }}
    text.percentage {{
      fill: #ffffff;
      font-size: 10px;
      font-weight: 700;
      text-anchor: middle;
      dominant-baseline: central;
    }}
  </style>
  <rect class="card-bg" width="100%" height="100%" />
  <text class="title" x="{width//2}" y="35">Topic-wise Distribution</text>
  <g>
"""

    COLORS = {
        "Arrays": "#58a6ff",
        "Strings": "#bc8cff",
        "Trees": "#3fb950",
        "Graphs": "#1f6feb",
        "DynamicProgramming": "#ff7b72",
        "LinkedList": "#d29922",
        "Stack": "#f0883e",
        "Queue": "#7ee787",
        "HashMap": "#db61a2"
    }

    if total_val == 0:
        svg_content += f'    <circle cx="{cx}" cy="{cy}" r="{(R+r)/2}" fill="none" stroke="#8b949e" stroke-width="{R-r}" opacity="0.3" />\n'
    else:
        current_angle = 0
        for topic, val in filtered_dist.items():
            color = COLORS.get(topic, "#8b949e")
            slice_angle = (val / total_val) * 2 * math.pi
            
            start_angle = current_angle
            end_angle = current_angle + slice_angle
            current_angle = end_angle
            
            theta1 = start_angle - math.pi / 2
            theta2 = end_angle - math.pi / 2
            large_arc = 1 if slice_angle > math.pi else 0
            
            if slice_angle >= 2 * math.pi * 0.999:
                svg_content += f'    <circle cx="{cx}" cy="{cy}" r="{(R+r)/2}" fill="none" stroke="{color}" stroke-width="{R-r}" />\n'
                svg_content += f'    <text class="percentage" x="{cx}" y="{cy}">100%</text>\n'
                continue
                
            x1o = cx + R * math.cos(theta1)
            y1o = cy + R * math.sin(theta1)
            x2o = cx + R * math.cos(theta2)
            y2o = cy + R * math.sin(theta2)
            
            x1i = cx + r * math.cos(theta1)
            y1i = cy + r * math.sin(theta1)
            x2i = cx + r * math.cos(theta2)
            y2i = cy + r * math.sin(theta2)
            
            path_d = f"M {x1o:.2f} {y1o:.2f} "
            path_d += f"A {R:.2f} {R:.2f} 0 {large_arc} 1 {x2o:.2f} {y2o:.2f} "
            path_d += f"L {x2i:.2f} {y2i:.2f} "
            path_d += f"A {r:.2f} {r:.2f} 0 {large_arc} 0 {x1i:.2f} {y1i:.2f} Z"
            
            svg_content += f'    <path d="{path_d}" fill="{color}" stroke="{stroke_color}" stroke-width="1.5" />\n'
            
            # Label
            percentage = (val / total_val) * 100
            if percentage >= 5:
                mid_angle = (start_angle + end_angle) / 2 - math.pi / 2
                r_mid = r + (R - r) / 2
                lx = cx + r_mid * math.cos(mid_angle)
                ly = cy + r_mid * math.sin(mid_angle)
                svg_content += f'    <text class="percentage" x="{lx:.2f}" y="{ly:.2f}">{round(percentage)}%</text>\n'
                
        # Draw legend on the right side of the card
        y_start = 80
        for i, (topic, val) in enumerate(filtered_dist.items()):
            color = COLORS.get(topic, "#8b949e")
            y_pos = y_start + i * 22
            display_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', topic)
            percentage = (val / total_val) * 100
            
            # Color indicator box
            svg_content += f'    <rect x="280" y="{y_pos - 8}" width="12" height="12" rx="2" fill="{color}" />\n'
            # Legend label
            svg_content += f'    <text class="label" x="300" y="{y_pos}">{display_name} ({round(percentage)}%)</text>\n'

    svg_content += "  </g>\n</svg>"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"SVG chart ({'dark' if is_dark_mode else 'light'}) saved to {output_path}")

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    print("Analyzing repository solved problems...")
    stats = generate_stats_data(repo_root)
    
    # Save stats.json
    stats_json_path = os.path.join(repo_root, "stats.json")
    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Stats written to {stats_json_path}")
    
    # Save light SVG chart
    light_chart_path = os.path.join(repo_root, "leetcode_stats_light.svg")
    generate_svg_file(stats, light_chart_path, is_dark_mode=False)
    
    # Save dark SVG chart
    dark_chart_path = os.path.join(repo_root, "leetcode_stats_dark.svg")
    generate_svg_file(stats, dark_chart_path, is_dark_mode=True)
