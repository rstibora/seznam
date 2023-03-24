<script lang="ts">
    import type { PageData } from "./$types"


    export let data: PageData
</script>

<svelte:head>
    <title>{`Seznam | ${data.name}`}</title>
</svelte:head>


<div class="bg-slate-200 p-4 min-h-screen">
    <div class="flex flex-col max-w-[100em] mx-auto bg-white p-4 rounded drop-shadow">
        <div>
            <video class="w-full" id="videoPlayer" controls></video>
        </div>
        <script src="http://cdn.dashjs.org/latest/dash.all.min.js"></script>
        <script>
            (function(){
                var player = dashjs.MediaPlayer().create();
                player.initialize(document.querySelector("#videoPlayer"), url, true);
            })();
        </script>
        <div class="bg-slate-700 rounded text-slate-200 p-2 mt-4">
            <code>
                { data.complete_json }
            </code>
        </div>
    </div>
</div>