## Andrey Osipov

**Python backend developer** — Moscow. Building [VendorFind](https://vendorfind.ru),
founder of ZanityVPN.

I work mostly on the backend of production systems: FastAPI and Django services,
PostgreSQL, async task queues, and the Docker/CI infrastructure that ships them.
Portfolio and CV at **[aosipov.dev](https://aosipov.dev)**.

### What I've built

| Project | What it is |
| --- | --- |
| **[vendors-platform](https://github.com/haku4130/vendors-platform)** | Marketplace matching companies with IT contractors. FastAPI + SQLModel + PostgreSQL, Nuxt 3 frontend, Traefik, 7 CI workflows, deployed to production and staging. Live at [vendorfind.ru](https://vendorfind.ru). |
| **[ml-malware-detector](https://github.com/haku4130/ml-malware-detector)** | Detects malicious Python source by semantic similarity to a malware corpus — CodeGen embeddings and KMeans clustering instead of hash matching. Bachelor's thesis. |
| **[vpn-bot](https://github.com/haku4130/vpn-bot)** | Telegram bot managing VPN configs across multiple servers. Django + aiogram + Celery, gRPC to the Xray API, WireGuard config generation over SSH. |
| **[devops-bot](https://github.com/haku4130/devops-bot)** | Kubernetes infrastructure for deploying, monitoring and logging a Python service — the full delivery pipeline rather than the app. |
| **[ter-s-gallery-website](https://github.com/haku4130/ter-s-gallery-website)** | Commercial multi-page site for a premium furniture brand. Django REST Framework backend, Nuxt 3 SSR, Docker, automated deploys. Live at [ters.gallery](https://ters.gallery). |
| **[hyperos-accessibility-guard](https://github.com/haku4130/hyperos-accessibility-guard)** | Kotlin service that keeps an accessibility service alive on Xiaomi HyperOS, which silently kills it. No root, no Shizuku. |

### Stack

**Language** · Python 3.12, TypeScript, Kotlin

**Backend** · FastAPI · Django · SQLModel · SQLAlchemy · Pydantic · aiogram · Celery · gRPC · pytest

**Data** · PostgreSQL · Alembic · Redis

**Infrastructure** · Docker · Docker Compose · Traefik · Kubernetes · GitHub Actions · Nginx · Prometheus · Grafana · Sentry

**Frontend** · Nuxt 3/4 · Vue 3 · Tailwind CSS

### Open source

Active contributor to the [Remnawave](https://github.com/BEDOLAGA-DEV) ecosystem —
Python subscription-management tooling used by real deployments:

- [remnawave-bedolaga-telegram-bot#3194](https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot/pull/3194) — retry queue for outgoing email
- [remnawave-bedolaga-telegram-bot#3193](https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot/pull/3193) — system error log with delivery status
- [remnawave-bedolaga-telegram-bot#3190](https://github.com/BEDOLAGA-DEV/remnawave-bedolaga-telegram-bot/pull/3190) — deliver support replies by email to users without Telegram
- [bedolaga-cabinet#565](https://github.com/BEDOLAGA-DEV/bedolaga-cabinet/pull/565) — system errors admin page
- [bedolaga-cabinet#558](https://github.com/BEDOLAGA-DEV/bedolaga-cabinet/pull/558) — merged

### Contact

[aosipov.dev](https://aosipov.dev) · [a.osipov.code@gmail.com](mailto:a.osipov.code@gmail.com)
