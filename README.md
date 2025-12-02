# 🎯 Task Priority Scorer

An intelligent Python algorithm that scores and ranks tasks based on multiple factors including urgency, importance, deadline proximity, and effort efficiency. Perfect for productivity optimization and demonstrating algorithmic problem-solving skills.

## 📸 Screenshot

![Task Priority Scorer Output](./screenshots/task-scorer-output.png)

## ✨ Features

**Core Functionality**
- 📊 **Multi-Factor Scoring** - Weighs urgency (40%), importance (30%), deadline (20%), and effort (10%)
- 📅 **Deadline Intelligence** - Automatically calculates urgency based on days until deadline
- ⚡ **Efficiency Optimization** - Prioritizes "quick wins" (low effort, high impact)
- 🔄 **JSON I/O** - Load tasks from JSON, export scored results
- 📈 **Statistics Dashboard** - View summary stats about your task list
- 🎨 **Color-Coded Display** - Visual indicators for priority levels and deadlines

**Algorithm Highlights**
- Intelligent deadline scoring (overdue tasks = max priority)
- Effort efficiency calculation (rewards quick wins)
- Weighted scoring formula balancing multiple factors
- Data-driven decision making

## 🛠️ Tech Stack

- **Python 3.11+** - Modern Python features
- **Standard Library Only** - No external dependencies required
- **Dataclasses** - Clean data modeling
- **Type Hints** - Production-quality code
- **JSON** - Easy data interchange format

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- No additional packages required (uses Python standard library)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GodzillaEatsZombies/task-priority-scorer.git
   cd task-priority-scorer
   ```

2. **Verify Python version**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

3. **Run the scorer**
   ```bash
   python priority_scorer.py
   ```

That's it! No pip install needed.

## 📊 Usage

### Basic Usage

Simply run the script with the provided sample data:

```bash
python priority_scorer.py
```

This will:
1. Load tasks from `sample_tasks.json`
2. Calculate priority scores for each task
3. Display ranked results with color-coded indicators
4. Export scored tasks to `scored_tasks.json`
5. Show summary statistics

### Understanding the Output

**Score Indicators:**
- 🔴 High Priority (score ≥ 8.0)
- 🟠 Medium-High Priority (score 6.0 - 7.9)
- 🟡 Medium Priority (score 4.0 - 5.9)
- 🟢 Low Priority (score < 4.0)

**Deadline Indicators:**
- ⚠️ OVERDUE - Past deadline
- 🔴 TODAY - Due today
- 🟠 Tomorrow - Due tomorrow
- 🟡 2-3 days - Due soon
- 🟢 4-7 days - Due this week

### Custom Task Data

Modify `sample_tasks.json` with your own tasks:

```json
{
  "tasks": [
    {
      "name": "Your task name",
      "urgency": 8,
      "importance": 7,
      "effort": 3,
      "deadline": "2025-12-15",
      "status": "todo",
      "priority": "high"
    }
  ]
}
```

**Field Descriptions:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `name` | string | - | Task description |
| `urgency` | int | 1-10 | How time-sensitive is this task? |
| `importance` | int | 1-10 | How impactful is this task? |
| `effort` | int | 1-10 | How many hours will this take? |
| `deadline` | string | YYYY-MM-DD | When is this due? |
| `status` | string | todo/in_progress/completed | Current status |
| `priority` | string | low/medium/high | Manual priority label |

## 🧮 Scoring Algorithm

The algorithm uses a weighted formula to calculate priority scores:

```
score = (urgency × 0.4) + (importance × 0.3) + (deadline_factor × 0.2) + (effort_efficiency × 0.1)
```

### Weight Breakdown

| Factor | Weight | Rationale |
|--------|--------|-----------|
| **Urgency** | 40% | Time-sensitive tasks need immediate attention |
| **Importance** | 30% | High-impact tasks create the most value |
| **Deadline** | 20% | Approaching deadlines increase priority |
| **Effort** | 10% | Quick wins provide momentum |

### Deadline Scoring Logic

The deadline factor automatically adjusts based on proximity:

| Time Until Deadline | Score |
|---------------------|-------|
| Overdue | 10.0 |
| Today | 10.0 |
| Tomorrow | 9.0 |
| Within 3 days | 8.0 |
| Within 1 week | 6.0 |
| Within 2 weeks | 4.0 |
| Within 1 month | 2.0 |
| Later | 1.0 |

### Effort Efficiency

Lower effort tasks receive higher efficiency scores, encouraging "quick wins":

```
efficiency_score = 10 - effort
```

This means a 2-hour task scores higher than an 8-hour task (all else equal).

## 📁 Project Structure

```
TaskPriorityScorer/
├── screenshots/
│   └── task-scorer-output.png
├── priority_scorer.py      # Main algorithm implementation
├── sample_tasks.json       # Example task dataset
├── requirements.txt        # Dependencies (none required)
├── README.md              # This file
└── scored_tasks.json      # Generated output (after running)
```

## 🎯 Skills Demonstrated

**Algorithm Design**
- ✅ Multi-factor weighted scoring system
- ✅ Intelligent deadline proximity calculation
- ✅ Effort optimization logic
- ✅ Data-driven decision making

**Python Best Practices**
- ✅ Type hints throughout
- ✅ Dataclasses for clean data modeling
- ✅ Enums for constants
- ✅ Docstrings and comments
- ✅ Error handling
- ✅ Modular, object-oriented design

**Data Handling**
- ✅ JSON parsing and serialization
- ✅ Date/time calculations
- ✅ File I/O operations
- ✅ Data transformation

**Professional Skills**
- ✅ Clean, readable code
- ✅ Production-ready structure
- ✅ Comprehensive documentation
- ✅ User-friendly terminal output

## 🌟 Future Enhancements

Potential additions to expand this project:

- [ ] Data visualization with matplotlib
- [ ] CSV import/export support
- [ ] Interactive CLI menu
- [ ] Task dependencies handling
- [ ] Team assignment features
- [ ] Time tracking integration
- [ ] Web dashboard (Flask/FastAPI)
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] RESTful API wrapper

## 💼 Use Cases

This scoring algorithm is useful for:

- 📋 **Personal Productivity** - Prioritize your daily tasks
- 👥 **Team Management** - Rank team workload
- 🎯 **Project Planning** - Identify critical path items
- 🚀 **Sprint Planning** - Select highest-value work
- 📊 **Resource Allocation** - Optimize team capacity

## 📝 Example Scenarios

### Scenario 1: Bug vs. Feature

**Bug Fix:**
- Urgency: 10, Importance: 9, Effort: 3, Deadline: Tomorrow
- **Score: 9.0** ✅ Do this first!

**New Feature:**
- Urgency: 5, Importance: 8, Effort: 8, Deadline: Next month
- **Score: 5.2** → Do after the bug

### Scenario 2: Quick Wins

**Easy Task:**
- Urgency: 6, Importance: 6, Effort: 1, Deadline: This week
- **Score: 6.9** ✅ Quick win!

**Complex Task:**
- Urgency: 6, Importance: 6, Effort: 9, Deadline: This week
- **Score: 5.3** → Save for later

## 📄 License

This is a portfolio project for demonstration purposes. Free to use and modify.

## 👨‍💻 Author

Built by **Raymond** as part of a freelance developer portfolio.

**Skills Demonstrated:**
- Algorithm Design
- Python Programming
- Data Structures
- Problem Solving
- Clean Code Practices
- Technical Documentation

---

**Portfolio Project #4** | Built with 💪 by an AI-Native Developer