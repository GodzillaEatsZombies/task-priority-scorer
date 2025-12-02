"""
Task Priority Scorer
A Python algorithm that intelligently scores and ranks tasks based on multiple factors.

Author: Raymond
Portfolio Project #4
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    """Task status options"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """Task data model"""
    name: str
    urgency: int  # 1-10 scale
    importance: int  # 1-10 scale
    effort: int  # 1-10 scale (hours estimated)
    deadline: str  # ISO format: "YYYY-MM-DD"
    status: str = "todo"
    priority: str = "medium"
    score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return asdict(self)


class TaskPriorityScorer:
    """
    Intelligent task scoring algorithm that considers multiple factors:
    - Urgency (40% weight)
    - Importance (30% weight)
    - Deadline proximity (20% weight)
    - Effort efficiency (10% weight)
    """
    
    # Scoring weights
    URGENCY_WEIGHT = 0.4
    IMPORTANCE_WEIGHT = 0.3
    DEADLINE_WEIGHT = 0.2
    EFFORT_WEIGHT = 0.1
    
    # Display settings
    TABLE_WIDTH = 100
    NAME_WIDTH = 32
    
    def __init__(self):
        self.tasks: List[Task] = []
    
    def load_tasks_from_json(self, filepath: str) -> None:
        """Load tasks from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.tasks = [Task(**task) for task in data.get('tasks', [])]
            print(f"  ✅ Loaded {len(self.tasks)} tasks from {filepath}")
        except FileNotFoundError:
            print(f"  ❌ Error: File '{filepath}' not found")
        except json.JSONDecodeError:
            print(f"  ❌ Error: Invalid JSON in '{filepath}'")
    
    def add_task(self, task: Task) -> None:
        """Add a single task to the scorer"""
        self.tasks.append(task)
    
    def calculate_deadline_factor(self, deadline_str: str) -> float:
        """
        Calculate urgency factor based on deadline proximity.
        Returns a score from 0-10 based on days until deadline.
        """
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            today = datetime.now()
            days_until = (deadline - today).days
            
            # Scoring logic
            if days_until < 0:
                return 10.0  # Overdue - maximum urgency
            elif days_until == 0:
                return 10.0  # Due today
            elif days_until == 1:
                return 9.0   # Due tomorrow
            elif days_until <= 3:
                return 8.0   # Due within 3 days
            elif days_until <= 7:
                return 6.0   # Due within a week
            elif days_until <= 14:
                return 4.0   # Due within 2 weeks
            elif days_until <= 30:
                return 2.0   # Due within a month
            else:
                return 1.0   # Due later than a month
                
        except ValueError:
            print(f"  ⚠️  Warning: Invalid deadline format '{deadline_str}', using default factor")
            return 5.0  # Default middle value
    
    def calculate_effort_efficiency(self, effort: int) -> float:
        """
        Calculate efficiency score based on effort required.
        Lower effort = higher efficiency score (quick wins are valuable)
        """
        # Invert the effort scale (10 - effort) to reward lower effort
        return 10 - effort
    
    def calculate_task_score(self, task: Task) -> float:
        """
        Calculate overall priority score for a task.
        
        Formula:
        score = (urgency * 0.4) + (importance * 0.3) + 
                (deadline_factor * 0.2) + (effort_efficiency * 0.1)
        """
        deadline_factor = self.calculate_deadline_factor(task.deadline)
        effort_efficiency = self.calculate_effort_efficiency(task.effort)
        
        score = (
            (task.urgency * self.URGENCY_WEIGHT) +
            (task.importance * self.IMPORTANCE_WEIGHT) +
            (deadline_factor * self.DEADLINE_WEIGHT) +
            (effort_efficiency * self.EFFORT_WEIGHT)
        )
        
        return round(score, 2)
    
    def score_all_tasks(self) -> None:
        """Calculate scores for all tasks"""
        for task in self.tasks:
            task.score = self.calculate_task_score(task)
        print(f"  ✅ Scored {len(self.tasks)} tasks")
    
    def get_sorted_tasks(self, reverse: bool = True) -> List[Task]:
        """
        Get tasks sorted by score.
        
        Args:
            reverse: If True, highest scores first (default)
        """
        return sorted(self.tasks, key=lambda t: t.score, reverse=reverse)
    
    def _truncate_name(self, name: str) -> str:
        """Truncate task name to fit display width"""
        if len(name) > self.NAME_WIDTH:
            return name[:self.NAME_WIDTH - 3] + "..."
        return name
    
    def _get_deadline_display(self, deadline_str: str) -> str:
        """Get formatted deadline display string"""
        try:
            deadline_obj = datetime.strptime(deadline_str, "%Y-%m-%d")
            days_until = (deadline_obj - datetime.now()).days
            
            if days_until < 0:
                return "⚠️  OVERDUE"
            elif days_until == 0:
                return "🔴 TODAY"
            elif days_until == 1:
                return "🟠 Tomorrow"
            elif days_until <= 3:
                return f"🟡 {days_until} days"
            elif days_until <= 7:
                return f"🟢 {days_until} days"
            else:
                return f"   {days_until} days"
        except ValueError:
            return "   Unknown"
    
    def _get_score_indicator(self, score: float) -> str:
        """Get visual indicator based on score"""
        if score >= 8.0:
            return "🔴"
        elif score >= 6.0:
            return "🟠"
        elif score >= 4.0:
            return "🟡"
        else:
            return "🟢"
    
    def display_results(self, top_n: Optional[int] = None) -> None:
        """
        Display scored and sorted tasks in a formatted table.
        
        Args:
            top_n: If provided, only show top N tasks
        """
        sorted_tasks = self.get_sorted_tasks()
        
        if top_n:
            sorted_tasks = sorted_tasks[:top_n]
        
        # Section header
        print()
        print("─" * self.TABLE_WIDTH)
        if top_n:
            print(f"  🎯 TOP {top_n} PRIORITY TASKS")
        else:
            print(f"  📊 ALL TASKS (SORTED BY PRIORITY)")
        print("─" * self.TABLE_WIDTH)
        print()
        
        # Table header
        print(f"  {'Rank':<6}{'Score':<10}{'Task Name':<35}{'Urgency':<10}{'Importance':<12}{'Deadline':<15}")
        print(f"  {'─'*6}{'─'*10}{'─'*35}{'─'*10}{'─'*12}{'─'*15}")
        
        # Task rows
        for idx, task in enumerate(sorted_tasks, 1):
            task_name = self._truncate_name(task.name)
            deadline_display = self._get_deadline_display(task.deadline)
            score_indicator = self._get_score_indicator(task.score)
            
            print(f"  #{idx:<5}{score_indicator} {task.score:<7}{task_name:<35}{task.urgency:<10}{task.importance:<12}{deadline_display:<15}")
        
        print()
    
    def display_statistics(self) -> None:
        """Display summary statistics in a formatted box"""
        stats = self.get_statistics()
        
        if "error" in stats:
            print(f"  ❌ {stats['error']}")
            return
        
        print("─" * self.TABLE_WIDTH)
        print("  📈 STATISTICS")
        print("─" * self.TABLE_WIDTH)
        print()
        
        # Two-column layout for stats
        print(f"  {'Total Tasks:':<25}{stats['total_tasks']:<15}{'High Priority (≥7.0):':<25}{stats['high_priority_tasks']}")
        print(f"  {'Average Score:':<25}{stats['average_score']:<15}{'Medium Priority (4-7):':<25}{stats['medium_priority_tasks']}")
        print(f"  {'Highest Score:':<25}{stats['highest_score']:<15}{'Low Priority (<4.0):':<25}{stats['low_priority_tasks']}")
        print(f"  {'Lowest Score:':<25}{stats['lowest_score']:<15}{'Average Urgency:':<25}{stats['average_urgency']}")
        print()
    
    def export_results(self, filepath: str) -> None:
        """Export scored tasks to JSON file"""
        sorted_tasks = self.get_sorted_tasks()
        
        output = {
            "scored_at": datetime.now().isoformat(),
            "total_tasks": len(sorted_tasks),
            "algorithm": {
                "urgency_weight": self.URGENCY_WEIGHT,
                "importance_weight": self.IMPORTANCE_WEIGHT,
                "deadline_weight": self.DEADLINE_WEIGHT,
                "effort_weight": self.EFFORT_WEIGHT
            },
            "tasks": [task.to_dict() for task in sorted_tasks]
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"  ✅ Results exported to {filepath}")
        except Exception as e:
            print(f"  ❌ Error exporting results: {e}")
    
    def get_statistics(self) -> Dict:
        """Get summary statistics about the task list"""
        if not self.tasks:
            return {"error": "No tasks to analyze"}
        
        scores = [task.score for task in self.tasks]
        urgencies = [task.urgency for task in self.tasks]
        
        return {
            "total_tasks": len(self.tasks),
            "average_score": round(sum(scores) / len(scores), 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "average_urgency": round(sum(urgencies) / len(urgencies), 2),
            "high_priority_tasks": len([t for t in self.tasks if t.score >= 7.0]),
            "medium_priority_tasks": len([t for t in self.tasks if 4.0 <= t.score < 7.0]),
            "low_priority_tasks": len([t for t in self.tasks if t.score < 4.0]),
        }


def main():
    """Main execution function"""
    # Header
    print()
    print("╔" + "═" * 98 + "╗")
    print("║" + " " * 30 + "🎯 TASK PRIORITY SCORER" + " " * 45 + "║")
    print("║" + " " * 28 + "AI-Enhanced Productivity Tool" + " " * 40 + "║")
    print("╚" + "═" * 98 + "╝")
    print()
    
    # Initialize scorer
    scorer = TaskPriorityScorer()
    
    # Load tasks from JSON
    scorer.load_tasks_from_json('sample_tasks.json')
    
    # Score all tasks
    scorer.score_all_tasks()
    
    # Display results
    scorer.display_results()
    
    # Show statistics
    scorer.display_statistics()
    
    # Export results
    print("─" * 100)
    print("  💾 EXPORT")
    print("─" * 100)
    print()
    scorer.export_results('scored_tasks.json')
    print()
    
    # Footer
    print("═" * 100)
    print("  ✅ Task scoring complete!")
    print()
    print("  💡 TIP: Modify 'sample_tasks.json' to score your own tasks!")
    print("  📖 See README.md for algorithm details and customization options.")
    print("═" * 100)
    print()


if __name__ == "__main__":
    main()