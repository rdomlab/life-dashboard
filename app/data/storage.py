import sqlite3
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Database file
DB_FILE = "app/data/dashboard.db"

def init_storage():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP,
            priority TEXT DEFAULT 'medium'
        )
    ''')

    # Create calendar events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calendar_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT DEFAULT 'personal'
        )
    ''')

    # Create health logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            steps INTEGER,
            calories INTEGER,
            sleep_hours REAL,
            mood TEXT,
            notes TEXT
        )
    ''')

    # Create github activity table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS github_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            repo TEXT,
            action TEXT,
            description TEXT,
            commits INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

def get_tasks() -> List[Dict[str, Any]]:
    """Get all tasks"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries
    return [
        {
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "completed": task[3],
            "created_at": task[4],
            "due_date": task[5],
            "priority": task[6]
        }
        for task in tasks
    ]

def get_calendar_events() -> List[Dict[str, Any]]:
    """Get calendar events"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM calendar_events ORDER BY start_time ASC')
    events = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries
    return [
        {
            "id": event[0],
            "title": event[1],
            "description": event[2],
            "start_time": event[3],
            "end_time": event[4],
            "created_at": event[5],
            "category": event[6]
        }
        for event in events
    ]

def get_health_logs() -> List[Dict[str, Any]]:
    """Get health logs"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM health_logs ORDER BY date DESC')
    logs = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries
    return [
        {
            "id": log[0],
            "date": log[1],
            "steps": log[2],
            "calories": log[3],
            "sleep_hours": log[4],
            "mood": log[5],
            "notes": log[6]
        }
        for log in logs
    ]

def get_github_activity() -> List[Dict[str, Any]]:
    """Get GitHub activity"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM github_activity ORDER BY date DESC')
    activity = cursor.fetchall()
    conn.close()

    # Convert to list of dictionaries
    return [
        {
            "id": activity[0],
            "date": activity[1],
            "repo": activity[2],
            "action": activity[3],
            "description": activity[4],
            "commits": activity[5]
        }
        for activity in activity
    ]

def get_fake_data():
    """Generate fake data for initial development"""
    # Generate fake tasks
    tasks = [
        {"title": "Complete dashboard project", "description": "Finish the Life Dashboard implementation", "completed": False, "due_date": (datetime.now() + timedelta(days=1)).isoformat(), "priority": "high"},
        {"title": "Review Ollama integration", "description": "Test Ollama AI features", "completed": True, "due_date": (datetime.now() - timedelta(days=1)).isoformat(), "priority": "medium"},
        {"title": "Setup Proxmox container", "description": "Configure LXC container for deployment", "completed": False, "due_date": (datetime.now() + timedelta(days=3)).isoformat(), "priority": "low"},
    ]

    # Generate fake calendar events
    events = [
        {"title": "Team meeting", "description": "Weekly team sync", "start_time": (datetime.now() + timedelta(hours=2)).isoformat(), "end_time": (datetime.now() + timedelta(hours=3)).isoformat(), "category": "work"},
        {"title": "Lunch with Sarah", "description": "Catch up over lunch", "start_time": (datetime.now() + timedelta(hours=12)).isoformat(), "end_time": (datetime.now() + timedelta(hours=13)).isoformat(), "category": "personal"},
    ]

    # Generate fake health logs
    logs = [
        {"date": (datetime.now() - timedelta(days=1)).isoformat(), "steps": 8500, "calories": 2100, "sleep_hours": 7.5, "mood": "happy", "notes": "Good day, feeling productive"},
        {"date": datetime.now().isoformat(), "steps": 10200, "calories": 2400, "sleep_hours": 8.0, "mood": "excited", "notes": "Great morning workout"},
    ]

    # Generate fake GitHub activity
    activity = [
        {"repo": "life-dashboard", "action": "commit", "description": "Implement Ollama integration", "commits": 1},
        {"repo": "personal-website", "action": "push", "description": "Update documentation", "commits": 3},
    ]

    return {
        "tasks": tasks,
        "calendar_events": events,
        "health_logs": logs,
        "github_activity": activity
    }

def seed_database():
    """Seed the database with fake data for initial development"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if tables are empty
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        # Insert fake tasks
        for task in get_fake_data()["tasks"]:
            cursor.execute('''
                INSERT INTO tasks (title, description, completed, due_date, priority)
                VALUES (?, ?, ?, ?, ?)
            ''', (task["title"], task["description"], task["completed"], task["due_date"], task["priority"]))

    cursor.execute('SELECT COUNT(*) FROM calendar_events')
    if cursor.fetchone()[0] == 0:
        # Insert fake calendar events
        for event in get_fake_data()["calendar_events"]:
            cursor.execute('''
                INSERT INTO calendar_events (title, description, start_time, end_time, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (event["title"], event["description"], event["start_time"], event["end_time"], event["category"]))

    cursor.execute('SELECT COUNT(*) FROM health_logs')
    if cursor.fetchone()[0] == 0:
        # Insert fake health logs
        for log in get_fake_data()["health_logs"]:
            cursor.execute('''
                INSERT INTO health_logs (date, steps, calories, sleep_hours, mood, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (log["date"], log["steps"], log["calories"], log["sleep_hours"], log["mood"], log["notes"]))

    cursor.execute('SELECT COUNT(*) FROM github_activity')
    if cursor.fetchone()[0] == 0:
        # Insert fake GitHub activity
        for activity in get_fake_data()["github_activity"]:
            cursor.execute('''
                INSERT INTO github_activity (repo, action, description, commits)
                VALUES (?, ?, ?, ?)
            ''', (activity["repo"], activity["action"], activity["description"], activity["commits"]))

    conn.commit()
    conn.close()