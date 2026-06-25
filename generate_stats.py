import os
import json
import re
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
    Parses the main README.md to extract problem lists under topic headings.
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
            topic_problems[current_topic] = set()
        elif current_topic and line.startswith('| [') and '](http' in line:
            match = re.search(r'\[([^\]]+)\]', line)
            if match:
                problem_name = match.group(1)
                topic_problems[current_topic].add(problem_name)
                
    return topic_problems

def generate_stats_data(repo_path):
    """
    Compiles problem counts for all target topics and overall total.
    """
    solved_by_topic = {topic: set() for topic in TARGET_TOPICS}
    
    # 1. Attempt to count from folder structure (nested under target topic folders)
    folder_exists_and_not_empty = False
    for topic in TARGET_TOPICS:
        topic_path = os.path.join(repo_path, topic)
        if os.path.isdir(topic_path):
            probs = get_problems_in_folder(topic_path)
            if probs:
                solved_by_topic[topic] = probs
                folder_exists_and_not_empty = True
                
    # 2. Fallback: Parse README.md topic-wise markdown mapping
    if not folder_exists_and_not_empty:
        print("Folder structure not found or empty. Falling back to parsing README.md...")
        readme_path = os.path.join(repo_path, "README.md")
        parsed_topics = parse_readme_topics(readme_path)
        for parsed_topic, problems in parsed_topics.items():
            mapped_topic = TOPIC_MAPPING.get(parsed_topic)
            if mapped_topic in solved_by_topic:
                for p in problems:
                    solved_by_topic[mapped_topic].add(p)
                    
    # Format counts and total
    distribution = {topic: len(solved_by_topic[topic]) for topic in TARGET_TOPICS}
    total_solved = count_all_solved_problems(repo_path)
    
    # In case total_solved is 0 but we found topics in README
    readme_total = len(set().union(*solved_by_topic.values()))
    if total_solved == 0 and readme_total > 0:
        total_solved = readme_total

    # Current local time formatted nicely
    now = datetime.now(timezone.utc).astimezone() # Local time of execution
    last_updated = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    
    return {
        "total_solved": total_solved,
        "topic_distribution": distribution,
        "last_updated": last_updated
    }

def generate_pie_chart(stats_data, output_path):
    """
    Generates a beautifully styled pie chart showing the topic-wise distribution.
    """
    try:
        import matplotlib
        matplotlib.use('Agg') # Non-interactive backend
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib not installed. Skipping pie chart generation.")
        return False
        
    distribution = stats_data["topic_distribution"]
    
    # Filter out categories with 0 solved problems
    filtered_dist = {k: v for k, v in distribution.items() if v > 0}
    
    if not filtered_dist:
        print("No problems found in any categories. Skipping pie chart generation.")
        return False
        
    labels = list(filtered_dist.keys())
    sizes = list(filtered_dist.values())
    
    # Color palette matching modern dark mode
    COLORS = {
        "Arrays": "#58a6ff",             # Blue
        "Strings": "#bc8cff",            # Purple
        "Trees": "#3fb950",              # Green
        "Graphs": "#1f6feb",             # Dark Blue
        "DynamicProgramming": "#ff7b72", # Red/Pink
        "LinkedList": "#d29922",         # Yellow/Gold
        "Stack": "#f0883e",              # Orange
        "Queue": "#7ee787",              # Light Green
        "HashMap": "#db61a2"             # Magenta
    }
    
    colors = [COLORS.get(label, "#8b949e") for label in labels]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6.5), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    # Explode the largest slice slightly for style
    max_idx = sizes.index(max(sizes))
    explode = [0.05 if i == max_idx else 0 for i in range(len(sizes))]
    
    # Draw pie chart
    wedges, texts, autotexts = ax.pie(
        sizes, 
        explode=explode, 
        labels=labels, 
        colors=colors,
        autopct='%1.1f%%',
        pctdistance=0.75,
        startangle=140,
        wedgeprops={
            'edgecolor': '#0d1117', 
            'linewidth': 2.5,
            'antialiased': True
        },
        textprops={
            'color': '#c9d1d9',
            'weight': 'bold',
            'fontsize': 11
        }
    )
    
    # Style percentages inside wedges
    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
        
    # Draw center circle to make it a donut chart (very modern)
    centre_circle = plt.Circle((0,0), 0.50, fc='#0d1117', edgecolor='#30363d', linewidth=1)
    fig.gca().add_artist(centre_circle)
    
    # Add title with total count
    plt.title(
        f"LeetCode Topic Distribution\n(Total Solved: {stats_data['total_solved']})", 
        color='#f0f6fc', 
        fontsize=16, 
        weight='bold', 
        pad=20
    )
    
    # Legend displaying counts
    legend_labels = [f"{label} ({filtered_dist[label]})" for label in labels]
    legend = ax.legend(
        wedges, 
        legend_labels,
        title="Topics",
        loc="center left",
        bbox_to_anchor=(0.95, 0.5),
        facecolor='#161b22',
        edgecolor='#30363d'
    )
    plt.setp(legend.get_title(), color='#f0f6fc', weight='bold')
    for text in legend.get_texts():
        text.set_color('#c9d1d9')
        
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
    plt.close()
    print(f"Topic pie chart saved to {output_path}")
    return True

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    print("Analyzing repository solved problems...")
    stats = generate_stats_data(repo_root)
    
    # Save stats.json
    stats_json_path = os.path.join(repo_root, "stats.json")
    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Stats written to {stats_json_path}")
    
    # Save pie chart
    chart_path = os.path.join(repo_root, "leetcode_stats.png")
    generate_pie_chart(stats, chart_path)
