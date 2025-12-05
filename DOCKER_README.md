# E-CMS Docker Deployment Guide

## Quick Start (Development)

1. **Clone and navigate to the project:**
   \`\`\`bash
   cd scripts/e_cms
   \`\`\`

2. **Start with SQLite (development):**
   \`\`\`bash
   docker-compose -f docker-compose.dev.yml up --build
   \`\`\`

3. **Access the application:**
   - Homepage: http://localhost:8000
   - Wagtail Admin: http://localhost:8000/cms-admin/
   - Django Admin: http://localhost:8000/admin/

## Production Deployment

1. **Copy and configure environment variables:**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your production values
   \`\`\`

2. **Start all services:**
   \`\`\`bash
   docker-compose up -d --build
   \`\`\`

3. **Run migrations and create superuser:**
   \`\`\`bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   \`\`\`

## Default Credentials

- **Email:** admin@example.com
- **Password:** admin123

**Important:** Change these credentials immediately in production!

## Useful Commands

\`\`\`bash
# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
\`\`\`

## Architecture

- **web**: Django/Wagtail application (Gunicorn)
- **db**: PostgreSQL 15 database
- **nginx**: Reverse proxy for static files and SSL termination

## Volumes

- `postgres_data`: PostgreSQL database files
- `static_volume`: Collected static files
- `media_volume`: User-uploaded media files

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | False |
| SECRET_KEY | Django secret key | Required |
| DB_PASSWORD | PostgreSQL password | postgres |
| WAGTAIL_BASE_URL | Public URL | http://localhost:8000 |

## Color Customization

Colors can be customized in the Wagtail admin under **Settings > Configuration de la mairie**:

- **Couleur primaire**: Main brand color
- **Couleur secondaire**: Secondary accent color  
- **Couleur d'accent**: Highlight color for CTAs

These colors are automatically applied to all generated websites.
