import type { PageLoad } from "./$types"

import { browser } from "$app/environment"


export const load = (async({}) => {
    const videos = await (await fetch(`http://${browser ? 'localhost' : 'django'}:8000/api/`)).json()
    return { videos }
}) satisfies PageLoad
