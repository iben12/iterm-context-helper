import asyncio

import iterm2


async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='docker context',
        detailed_description='The currently configured Docker context for docker cli',
        exemplar='🐳 default',
        update_cadence=2,
        identifier='engineering.iben.iterm-components.docker-context',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def docker_context_coroutine(knobs):
        proc = await asyncio.create_subprocess_shell(
            '/usr/local/bin/docker context ls --format \'{{json .}}\' | jq -r \'select(.Current) .Name\'',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return f'🐳 {stdout.decode().strip()}' if not stderr else '🐳 can\'t find docker!'

    await component.async_register(connection, docker_context_coroutine)

iterm2.run_forever(main)
