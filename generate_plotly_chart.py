import os
import json
import pandas as pd
import plotly.express as px

def main():
    # Find stats.json path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stats_json_path = os.path.join(current_dir, "stats.json")
    
    if os.path.exists(stats_json_path):
        print(f"Reading stats from {stats_json_path}...")
        with open(stats_json_path, 'r', encoding='utf-8') as f:
            stats = json.load(f)
        distribution = stats["topic_distribution"]
        total_solved = stats["total_solved"]
    else:
        print("stats.json not found. Using default mock stats...")
        # Fallback fallback stats
        distribution = {
            "Arrays": 20,
            "Strings": 2,
            "Trees": 0,
            "Graphs": 0,
            "DynamicProgramming": 3,
            "LinkedList": 0,
            "Stack": 2,
            "Queue": 1,
            "HashMap": 0
        }
        total_solved = sum(distribution.values())

    # Filter out categories with 0 solved problems
    filtered_dist = {k: v for k, v in distribution.items() if v > 0}
    
    if not filtered_dist:
        print("No problems solved in any category yet.")
        return

    # Convert distribution to pandas DataFrame
    df = pd.DataFrame({
        "Topic": list(filtered_dist.keys()),
        "Solved Count": list(filtered_dist.values())
    })
    
    # Modern color palette for Plotly pie chart
    colors = {
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

    # Generate interactive Plotly Pie Chart
    fig = px.pie(
        df, 
        values="Solved Count", 
        names="Topic", 
        title=f"LeetCode Topic Distribution (Total Solved: {total_solved})",
        color="Topic",
        color_discrete_map=colors
    )
    
    # Customize layout to look dark and modern
    fig.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        hole=0.4, # Makes it a donut chart
        marker=dict(line=dict(color='#0d1117', width=2))
    )
    
    fig.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        font_color='#c9d1d9',
        title_font_size=20,
        title_font_color='#f0f6fc',
        title_x=0.5, # Center title
        legend=dict(
            font=dict(color='#c9d1d9'),
            bgcolor='#161b22',
            bordercolor='#30363d',
            borderwidth=1
        )
    )
    
    # Show interactive chart in browser
    fig.show()

if __name__ == "__main__":
    main()
