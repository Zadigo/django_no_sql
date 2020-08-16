import asyncio

class Database:
    def load_database(self):
        return "Awesome"

class AsyncDatabase(Database):
    async def load(self):
        value = await self.load_database()
        return value

    def main(self):
        return asyncio.run(self.load())

database = AsyncDatabase()
print(database.main())