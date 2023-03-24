import type { PageLoad } from "./$types"

import { browser } from "$app/environment"


export const load = (async({ url }) => {
    const videos = await (await fetch(`http://${browser ? 'localhost' : 'django'}:8000/api/${url.search}`)).json()
    return { videos }
}) satisfies PageLoad
