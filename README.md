# octopus-stack
# 🧰 Python Backend Service Kit

This repository contains a reusable structure and set of tools I use when building Python backend services.  
It includes common integrations and helpers for:

- ✅ Project settings & environment configs
- 🗃️ SQL (via SQLAlchemy)
- 🍃 MongoDB
- 🚀 Redis Cache
- 🐇 RabbitMQ
- And more...

## 📦 What's Inside

- `settings/` – project-wide configuration using Pydantic
- `db/sql/` – SQL database utilities and models
- `db/mongo/` – MongoDB connectors
- `cache/redis/` – Redis cache setup
- `messaging/rabbitmq/` – RabbitMQ publisher/subscriber logic
- `utils/` – common helper functions and base classes

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
