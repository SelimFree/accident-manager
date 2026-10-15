import asyncio
import os
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.features.users.models import User, UserRole
import app.models


async def main():
    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not email or "@" not in email or len(password) < 12:
        raise SystemExit("Set ADMIN_EMAIL and ADMIN_PASSWORD (12+ characters) before running")
    async with AsyncSessionLocal() as db:
        user = await db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(name=email.split("@", 1)[0][:80] or "Admin",
                        email=email, password_hash=hash_password(password), role=UserRole.admin)
            db.add(user)
        else:
            user.password_hash = hash_password(password)
            user.role = UserRole.admin
            user.is_active = True
        await db.commit()
    print("Administrator account created/updated")


if __name__ == "__main__":
    asyncio.run(main())
