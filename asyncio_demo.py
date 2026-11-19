
import asyncio
import time


async def maintenance_task(task_number):
    print(f"Задача {task_number}: начата")

    await asyncio.sleep(2)

    print(f"Задача {task_number}: завершена")


async def run_async_tasks():
    print("\nАсинхронное выполнение")
    start_time = time.perf_counter()

    tasks = [
        maintenance_task(i)
        for i in range(1, 6)
    ]

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    print(
        f"Асинхронное выполнение заняло: "
        f"{end_time - start_time:.2f} секунд"
    )


def run_sync_tasks():
    print("\nПоследовательное выполнение")
    start_time = time.perf_counter()

    for i in range(1, 6):
        print(f"Задача {i}: начата")
        time.sleep(2)
        print(f"Задача {i}: завершена")

    end_time = time.perf_counter()

    print(
        f"Последовательное выполнение заняло: "
        f"{end_time - start_time:.2f} секунд"
    )


if __name__ == "__main__":
    run_sync_tasks()
    asyncio.run(run_async_tasks())
