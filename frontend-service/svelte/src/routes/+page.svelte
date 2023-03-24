<script lang="ts">
    import type { PageData } from "./$types"

    import { enhance } from "$app/forms"
    import { page } from "$app/stores"


    export let data: PageData
</script>

<svelte:head>
    <title>Seznam | Videos</title>
</svelte:head>

<div class="bg-slate-200 p-4 min-h-screen">
    <div class="sticky max-w-[100em] max-h-48 flex flex-row mx-auto top-4 mb-4 bg-white rounded drop-shadow z-10 p-2">
        <form class="flex flex-row w-full" use:enhance>
            <fieldset class="flex flex-col flex-wrap border-solid border-r-2 border-slate-200 px-2">
                <div class="flex flex-row">
                    <input id="is_featured_checkbox" name="is_featured" type="checkbox" checked={$page.url.searchParams.get("is_featured") == "on"}>
                    <label for="is_featured_checkbox" class="ml-1">Featured</label>

                    <input type="text" name="search" class="mx-2" placeholder="Search name" value={$page.url.searchParams.get("search")}>
                </div>
            </fieldset>

            <!-- <fieldset class="flex flex-col flex-wrap border-solid border-r-2 border-slate-200 px-2">
                {% for drm in all_drms %}
                    <div class="flex flex-row">
                        <input id="is_drm_"{{ drm }} name="filter_drm_{{ drm }}" type="checkbox">
                        <label for="is_drm_"{{ drm }} class="ml-1">{{ drm }}</label>
                    </div>
                {% endfor %}
            </fieldset>

            <fieldset class="flex flex-col flex-wrap grow w-fit border-solid border-r-2 border-slate-200 px-2">
                {% for feature in all_features %}
                    <div class="flex flex-row">
                        <input id="is_feature_"{{ feature }} name="filter_feature_{{ feature }}" type="checkbox">
                        <label for="is_feature_"{{ feature }} class="ml-1">{{ feature }}</label>
                    </div>
                {% endfor %}
            </fieldset>
            <textarea
                name="json_search"
                class="w-80 w-fit border-solid border-r-2 border-slate-200 px-2"
                placeholder="Full json search, use Django JSONField query syntax with json values after '=' (e.g. 'isFeatured=true')"
            ></textarea> -->
            <button class="px-2 font-bold">Submit</button>
        </form>
    </div>
    <div class="max-w-[100em] mx-auto bg-white p-4 rounded drop-shadow">
        <table class="w-full">
            <!-- <tr class="bg-slate-700 text-slate-200 p-2">
                <th />
                <th class="max-w-2">
                    Short Name
                    <a href="{% url 'index' %}?order_by=short_name&order=asc"> &uarr;</a>
                    <a href="{% url 'index' %}?order_by=short_name&order=desc"> &darr;</a>
                </th>
                <th>
                    Name
                    <a href="{% url 'index' %}?order_by=name&order=asc"> &uarr;</a>
                    <a href="{% url 'index' %}?order_by=name&order=desc"> &darr;</a>
                </th>
                <th>
                    Featured
                    <a href="{% url 'index' %}?order_by=is_featured&order=asc"> &uarr;</a>
                    <a href="{% url 'index' %}?order_by=is_featured&order=desc"> &darr;</a>
                </th>
                <th>
                    DRM
                    <a href="{% url 'index' %}?order_by=drms&order=asc"> &uarr;</a>
                    <a href="{% url 'index' %}?order_by=drms&order=desc"> &darr;</a>
                </th>
                <th>
                    Features
                    <a href="{% url 'index' %}?order_by=features&order=asc"> &uarr;</a>
                    <a href="{% url 'index' %}?order_by=features&order=desc"> &darr;</a>
                </th>
                <th />
            </tr> -->

            {#each data.videos as video}
                <tr class="bg-white odd:bg-slate-100 p-2 hover:bg-slate-700 hover:text-slate-200">
                    <td><img class="max-h-16" src={ video.icon_uri }></td>
                    <td>{ video.short_name ?? "" }</td>
                    <td>{ video.name }</td>
                    <td>{ video.is_featured }</td>
                    <!-- <td>{% for drm in video.drms.all %}{{ drm.name }}{% if not forloop.last %}, {% endif %}{% endfor %}</td> -->
                    <!-- <td>{% for feature in video.features.all %}{{ feature.name }}{% if not forloop.last %}, {% endif %}{% endfor %}</td> -->
                    <td><a class="font-bold"href={`/${video.id}`}>Details</a></td>
                </tr>
            {/each}
        </table>
    </div>
</div>
