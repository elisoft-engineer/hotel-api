import os
import secrets


def generate_unique_filename(filename: str) -> str:
    unique_suffix = secrets.token_urlsafe(8)
    name, ext = os.path.splitext(filename)
    return f"{name}_{unique_suffix}{ext}"