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
                problem_url = match.group(2)
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

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))
    
    print("Analyzing repository solved problems...")
    stats = generate_stats_data(repo_root)
    
    # Save stats.json
    stats_json_path = os.path.join(repo_root, "stats.json")
    with open(stats_json_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Stats written to {stats_json_path}")
