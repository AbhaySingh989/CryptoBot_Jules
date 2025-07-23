import asyncio
import os
import sys
from unittest.mock import patch

async def main():
    # Run the bot as a subprocess
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-m', 'trading_bot',
        '--api-key', 'test',
        '--api-secret', 'test',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Send commands to the bot
    proc.stdin.write(b'balance\n')
    await proc.stdin.drain()
    proc.stdin.write(b'positions\n')
    await proc.stdin.drain()
    proc.stdin.write(b'stop\n')
    await proc.stdin.drain()

    # Wait for the process to finish
    stdout, stderr = await proc.communicate()

    # Print the output
    print(f"Stdout: {stdout.decode()}")
    print(f"Stderr: {stderr.decode()}")

if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.insert(0, '.')
    asyncio.run(main())
