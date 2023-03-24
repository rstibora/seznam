import type { PageLoad } from "./$types"

import { browser } from "$app/environment"


export const load = (async({ params }) => {
    const video = await (await fetch(`http://${browser ? 'localhost' : 'django'}:8000/api/${params.id}`)).json()
    return video
}) satisfies PageLoad
