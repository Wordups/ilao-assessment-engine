# Architecture Diagram

```mermaid
flowchart LR
    User["Assessment Analyst"] --> UI["React Frontend<br/>Wizard + Dashboard"]
    UI --> Auth["Supabase Auth"]
    UI --> API["FastAPI REST API"]
    API --> App["Application Use Cases"]
    App --> Domain["Domain Services<br/>Summary + Opportunity Analysis"]
    App --> Repo["Repository Port"]
    Repo --> SQL["SQLAlchemy Repository"]
    SQL --> DB["PostgreSQL"]
    App --> PDF["PDF Reporting Service"]
    App -. future .-> AI["AI Analysis Provider Port"]
```

## Notes

- The React frontend owns data entry, authentication experience, and export actions.
- FastAPI exposes REST endpoints and OpenAPI docs.
- The application layer coordinates persistence, analysis generation, JSON export, and PDF output.
- The domain layer holds rule-based logic today and can be extended with AI-driven analysis later.
