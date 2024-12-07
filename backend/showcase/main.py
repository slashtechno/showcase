import importlib
from pathlib import Path
import uvicorn
from fastapi import FastAPI

app = FastAPI()


# Annotated
# https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#better-with-annotated
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#declare-more-metadata


# Dynamically import all routers
routers_dir = Path(__file__).parent / "routers"
for path in routers_dir.glob("*.py"):
    if path.name != "__init__.py":
        module_name = f"showcase.routers.{path.stem}"
        module = importlib.import_module(module_name)
        # If the module has a router attribute, include it in the app
        if hasattr(module, "router"):
            app.include_router(getattr(module, "router"))

if __name__ == "__main__":
    # Go to http://localhost:8000/docs to see the Swagger UI
    uvicorn.run(app, host="0.0.0.0", port=8000)
