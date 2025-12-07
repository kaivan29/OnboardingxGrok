# Codebase Analysis Configuration
# 
# List of repositories to analyze periodically for onboarding knowledge base

# Repository URLs to analyze
ANALYSIS_REPOS = [
    # Example repositories (mock data for now)
    "https://github.com/facebook/rocksdb",
    "https://github.com/pallets/flask",
    "https://github.com/tiangolo/fastapi",
]

# Analysis schedule (cron format)
# Default: Daily at 2 AM
ANALYSIS_SCHEDULE = {
    "hour": 2,
    "minute": 0
}

# Analysis settings
ANALYSIS_CONFIG = {
    "include_patterns": ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx"],
    "exclude_patterns": ["**/node_modules/**", "**/__pycache__/**", "**/.git/**"],
    "max_file_size": 100000,  # 100KB
}
