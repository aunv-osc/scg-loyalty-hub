import asyncio
import uvicorn
# from common.db.populate import create_tables
from common.db.session import engine
from common.app import create_app

application = create_app()

if __name__ == "__main__":
    # print("Populating database...")
    # asyncio.run(create_tables(engine))
    # print("Database populated.")

    print("Starting server...")
    uvicorn.run("main:application", host='localhost', port=8000, reload=True)
