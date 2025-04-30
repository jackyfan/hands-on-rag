import asyncio,time

async def hello_world():
    now = time.time()
    await asyncio.sleep(1)
    print("Hello, world!")
    print(time.time() - now)

async def async_hello_world():
    now = time.time()
    await asyncio.sleep(1)
    print(time.time() - now)
    print("Hello, world!")
    await asyncio.sleep(1)
    print(time.time() - now)

async def main():
    await asyncio.gather(async_hello_world(), async_hello_world(), async_hello_world())

now = time.time()
# run 3 async_hello_world() coroutine concurrently
asyncio.run(main())

print(f"Total time for running 3 coroutine: {time.time() - now}")

print("End")