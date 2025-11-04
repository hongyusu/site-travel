# Secrets Management Guide

Comprehensive guide for managing secrets, API keys, and sensitive configuration in the FindTravelMate application.

## Table of Contents

1. [Overview](#overview)
2. [Environment-Specific Configuration](#environment-specific-configuration)
3. [Secret Types](#secret-types)
4. [Generation Best Practices](#generation-best-practices)
5. [Storage Solutions](#storage-solutions)
6. [Docker Secrets](#docker-secrets)
7. [Rotation Strategy](#rotation-strategy)
8. [Security Checklist](#security-checklist)

## Overview

**Critical**: Never commit secrets to version control. All sensitive data must be managed through environment variables or secure secret management systems.

### What are Secrets?

- Database passwords
- API keys (Stripe, AWS, OAuth)
- JWT signing keys
- Encryption keys
- SMTP passwords
- Service credentials

## Environment-Specific Configuration

### Local Development

```bash
# Copy example file
cp .env.production.example .env

# Generate secure SECRET_KEY
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# Set other required values
nano .env
```

**Development .env:**
```bash
DATABASE_URL=postgresql://postgres:dev_password@localhost:5432/findtravelmate
SECRET_KEY=<generated-key>
POSTGRES_PASSWORD=dev_password
CORS_ORIGINS='["http://localhost:3000"]'
```

### Staging Environment

```bash
# Use stronger passwords
DATABASE_URL=postgresql://postgres:<strong-password>@staging-db:5432/findtravelmate
SECRET_KEY=<production-grade-key>
```

### Production Environment

**Never use default values in production!**

```bash
# All secrets must be unique and strong
DATABASE_URL=postgresql://postgres:<RANDOM-64-CHAR-PASSWORD>@prod-db:5432/findtravelmate
SECRET_KEY=<RANDOM-64-CHAR-KEY>
POSTGRES_PASSWORD=<RANDOM-64-CHAR-PASSWORD>
```

## Secret Types

### 1. Database Credentials

**Required:**
- `DATABASE_URL`: Full connection string
- `POSTGRES_PASSWORD`: Database password

**Generation:**
```bash
# Generate 64-character password
openssl rand -base64 48
```

**Security:**
- Minimum 32 characters
- Mix of alphanumeric and special characters
- Rotate every 90 days
- Different passwords per environment

### 2. Application Secrets

**Required:**
- `SECRET_KEY`: JWT signing key
- `ALGORITHM`: HS256 (recommended)

**Generation:**
```bash
# Generate SECRET_KEY (64 hex characters)
openssl rand -hex 32
```

**Security:**
- Minimum 64 characters (32 bytes in hex)
- Never reuse across environments
- Rotate every 180 days
- If compromised, rotate immediately

### 3. Third-Party API Keys

**Optional (Future):**
- `STRIPE_SECRET_KEY`: Payment processing
- `AWS_ACCESS_KEY_ID`: Cloud storage
- `GOOGLE_OAUTH_CLIENT_SECRET`: Social login
- `SMTP_PASSWORD`: Email service

**Security:**
- Use service-specific IAM roles when possible
- Restrict API key permissions
- Monitor API usage for anomalies
- Rotate every 90 days

## Generation Best Practices

### Strong Password Generation

```bash
# Method 1: OpenSSL (recommended)
openssl rand -base64 48

# Method 2: Python
python3 -c "import secrets; print(secrets.token_urlsafe(48))"

# Method 3: Password manager
# Use 1Password, Bitwarden, or LastPass with 64+ character length
```

### Secret Validation

```bash
# Check secret strength
if [ ${#SECRET_KEY} -lt 32 ]; then
    echo "ERROR: SECRET_KEY too short"
fi

# Verify no default values
if [[ "$SECRET_KEY" == *"changeme"* ]]; then
    echo "ERROR: Using default SECRET_KEY"
fi
```

## Storage Solutions

### Option 1: Environment Variables (Basic)

**Pros:**
- Simple to implement
- Works with Docker Compose
- No additional infrastructure

**Cons:**
- Visible in process lists
- Manual rotation
- No audit trail

**Setup:**
```bash
# Create .env file (never commit!)
touch .env
chmod 600 .env  # Restrict permissions

# Add to .gitignore
echo ".env" >> .gitignore
```

### Option 2: Docker Secrets (Recommended for Production)

**Pros:**
- Encrypted at rest
- Only available to specified services
- Better security than environment variables

**Cons:**
- Only works with Docker Swarm
- More complex setup

**Setup:**
```bash
# Create secrets
echo "mySecretPassword" | docker secret create db_password -
echo "myJWTSecret" | docker secret create jwt_secret -

# Use in docker-compose.yml
services:
  backend:
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    external: true
  jwt_secret:
    external: true
```

### Option 3: AWS Secrets Manager (Enterprise)

**Pros:**
- Centralized secret management
- Automatic rotation
- Full audit trail
- Fine-grained access control

**Cons:**
- Additional cost ($0.40/secret/month)
- AWS dependency
- More complex integration

**Setup:**
```bash
# Store secret
aws secretsmanager create-secret \
    --name findtravelmate/production/db_password \
    --secret-string "mySecretPassword"

# Retrieve in application
aws secretsmanager get-secret-value \
    --secret-id findtravelmate/production/db_password \
    --query SecretString \
    --output text
```

**Python Integration:**
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Use in settings
secret = get_secret('findtravelmate/production/db_password')
DATABASE_URL = f"postgresql://postgres:{secret['password']}@db:5432/findtravelmate"
```

### Option 4: HashiCorp Vault (Enterprise)

**Pros:**
- Platform-agnostic
- Dynamic secrets
- Comprehensive audit logs
- Encryption as a service

**Cons:**
- Self-hosted infrastructure
- Operational complexity
- Learning curve

## Docker Secrets

### Using Docker Compose Secrets

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  backend:
    environment:
      # Read from secret files
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
      SECRET_KEY_FILE: /run/secrets/jwt_secret
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

**Application code to read secrets:**
```python
def get_secret_from_file(secret_name: str) -> str:
    secret_file = os.getenv(f"{secret_name}_FILE")
    if secret_file and os.path.exists(secret_file):
        with open(secret_file, 'r') as f:
            return f.read().strip()
    return os.getenv(secret_name, "")

# Usage
DATABASE_PASSWORD = get_secret_from_file("DATABASE_PASSWORD")
SECRET_KEY = get_secret_from_file("SECRET_KEY")
```

## Rotation Strategy

### Rotation Schedule

| Secret Type | Rotation Frequency | Priority |
|-------------|-------------------|----------|
| Database passwords | 90 days | High |
| JWT signing keys | 180 days | High |
| API keys (3rd party) | 90 days | Medium |
| OAuth secrets | 365 days | Medium |
| Encryption keys | 365 days | High |

### Rotation Process

**1. Database Password Rotation:**
```bash
# Step 1: Create new password
NEW_PASSWORD=$(openssl rand -base64 48)

# Step 2: Update database
docker exec findtravelmate_db psql -U postgres -c \
    "ALTER USER postgres WITH PASSWORD '$NEW_PASSWORD';"

# Step 3: Update .env
sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$NEW_PASSWORD/" .env

# Step 4: Restart services
docker-compose -f docker-compose.prod.yml restart backend

# Step 5: Verify
docker-compose -f docker-compose.prod.yml exec backend \
    python -c "from app.database import SessionLocal; db = SessionLocal(); db.close(); print('OK')"
```

**2. JWT Secret Rotation (Zero-Downtime):**

```python
# Support multiple keys during rotation
SECRET_KEYS = [
    os.getenv("SECRET_KEY_NEW"),  # New key for signing
    os.getenv("SECRET_KEY_OLD"),  # Old key for verification
]

def verify_token(token: str):
    for secret_key in SECRET_KEYS:
        try:
            return jwt.decode(token, secret_key, algorithms=["HS256"])
        except JWTError:
            continue
    raise JWTError("Invalid token")
```

**Process:**
1. Generate new SECRET_KEY
2. Add as SECRET_KEY_NEW, keep old as SECRET_KEY_OLD
3. Deploy (both keys work)
4. Wait for all tokens to expire (7 days for refresh tokens)
5. Remove SECRET_KEY_OLD
6. Rename SECRET_KEY_NEW to SECRET_KEY

## Security Checklist

### Pre-Deployment

- [ ] All secrets generated with cryptographically secure methods
- [ ] No default passwords in use
- [ ] `.env` file permissions set to 600
- [ ] `.env` added to `.gitignore`
- [ ] Secrets validated (minimum length, complexity)
- [ ] Different secrets for each environment
- [ ] CORS_ORIGINS configured for production domain
- [ ] Database password meets complexity requirements (32+ chars)
- [ ] SECRET_KEY is at least 64 characters

### Post-Deployment

- [ ] Verify no secrets in Docker image layers (`docker history <image>`)
- [ ] Check environment variables not logged
- [ ] Confirm secrets not in error messages
- [ ] Test secret rotation procedure
- [ ] Document all secrets in team password manager
- [ ] Set up monitoring for secret access
- [ ] Configure alerts for authentication failures
- [ ] Schedule first rotation (90 days)

### Ongoing

- [ ] Monthly: Review secret access logs
- [ ] Quarterly: Rotate database passwords and API keys
- [ ] Bi-annually: Rotate JWT signing keys
- [ ] Annually: Full security audit
- [ ] After incident: Immediate rotation of affected secrets

## Emergency Procedures

### Compromised Secret

1. **Immediate Actions:**
```bash
# 1. Generate new secret
NEW_SECRET=$(openssl rand -hex 32)

# 2. Update production immediately
echo "SECRET_KEY=$NEW_SECRET" >> .env

# 3. Restart services
docker-compose -f docker-compose.prod.yml restart backend

# 4. Force all users to re-authenticate
docker exec findtravelmate_backend python -c \
    "from app.database import SessionLocal; from app.models import User; \
     db = SessionLocal(); db.query(User).update({'last_password_reset': datetime.now()}); \
     db.commit()"
```

2. **Investigation:**
   - Check access logs for unauthorized access
   - Review git history for accidental commits
   - Scan public repositories for leaked secrets
   - Document timeline and impact

3. **Prevention:**
   - Update procedures to prevent recurrence
   - Add pre-commit hooks to detect secrets
   - Implement secret scanning in CI/CD

### Pre-commit Hook (Prevent Secret Commits)

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for potential secrets
if git diff --cached | grep -i -E "(password|secret|key|token).*=.*['\"]([^'\"]{20,})['\"]"; then
    echo "ERROR: Potential secret detected in commit"
    echo "Please review and use environment variables instead"
    exit 1
fi
```

## Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetsproject.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)

## Support

For questions about secrets management:
1. Review this documentation
2. Check team password manager for current secrets
3. Contact DevOps team for production access
4. Never share secrets via email, Slack, or other insecure channels
