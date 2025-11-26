from app.main import app
import sys

with open("routes_out.txt", "w", encoding="utf-8") as f:
    f.write("Registered Routes:\n")
    for route in app.routes:
        f.write(f"{route.path} {route.methods}\n")
