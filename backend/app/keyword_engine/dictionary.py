from typing import Dict, List, Tuple

# Mapping of raw term / alias -> (Canonical Keyword Name, Category)
TECH_KEYWORD_DICTIONARY: Dict[str, Tuple[str, str]] = {
    # Programming Languages
    "python": ("Python", "programming_language"),
    "javascript": ("JavaScript", "programming_language"),
    "js": ("JavaScript", "programming_language"),
    "typescript": ("TypeScript", "programming_language"),
    "ts": ("TypeScript", "programming_language"),
    "golang": ("Go", "programming_language"),
    "go": ("Go", "programming_language"),
    "java": ("Java", "programming_language"),
    "c++": ("C++", "programming_language"),
    "cpp": ("C++", "programming_language"),
    "c#": ("C#", "programming_language"),
    "rust": ("Rust", "programming_language"),
    "ruby": ("Ruby", "programming_language"),
    "php": ("PHP", "programming_language"),
    "scala": ("Scala", "programming_language"),
    "kotlin": ("Kotlin", "programming_language"),
    "swift": ("Swift", "programming_language"),

    # Web & Application Frameworks
    "fastapi": ("FastAPI", "framework"),
    "django": ("Django", "framework"),
    "flask": ("Flask", "framework"),
    "react": ("React", "framework"),
    "reactjs": ("React", "framework"),
    "react.js": ("React", "framework"),
    "vue": ("Vue.js", "framework"),
    "vuejs": ("Vue.js", "framework"),
    "angular": ("Angular", "framework"),
    "next.js": ("Next.js", "framework"),
    "nextjs": ("Next.js", "framework"),
    "express": ("Express.js", "framework"),
    "express.js": ("Express.js", "framework"),
    "spring": ("Spring Boot", "framework"),
    "spring boot": ("Spring Boot", "framework"),
    "node.js": ("Node.js", "framework"),
    "nodejs": ("Node.js", "framework"),

    # Databases
    "postgresql": ("PostgreSQL", "database"),
    "postgres": ("PostgreSQL", "database"),
    "mysql": ("MySQL", "database"),
    "mongodb": ("MongoDB", "database"),
    "mongo": ("MongoDB", "database"),
    "redis": ("Redis", "database"),
    "sqlite": ("SQLite", "database"),
    "elasticsearch": ("Elasticsearch", "database"),
    "cassandra": ("Cassandra", "database"),
    "dynamodb": ("DynamoDB", "database"),

    # Cloud & Infrastructure
    "aws": ("AWS", "cloud"),
    "amazon web services": ("AWS", "cloud"),
    "azure": ("Azure", "cloud"),
    "gcp": ("GCP", "cloud"),
    "google cloud": ("GCP", "cloud"),
    "terraform": ("Terraform", "devops"),
    "docker": ("Docker", "devops"),
    "kubernetes": ("Kubernetes", "devops"),
    "k8s": ("Kubernetes", "devops"),
    "ansible": ("Ansible", "devops"),
    "jenkins": ("Jenkins", "devops"),

    # Event Streaming & Middleware
    "kafka": ("Apache Kafka", "messaging"),
    "apache kafka": ("Apache Kafka", "messaging"),
    "rabbitmq": ("RabbitMQ", "messaging"),

    # AI & Multi-Agent Frameworks
    "langgraph": ("LangGraph", "ai_agent_framework"),
    "langchain": ("LangChain", "ai_agent_framework"),
    "playwright": ("Playwright", "automation_framework"),
    "pytest": ("Pytest", "testing"),
    "latex": ("LaTeX", "rendering_engine"),
}
