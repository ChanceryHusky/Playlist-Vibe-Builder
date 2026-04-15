import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import time

def create_bar_plot(songs, key):
    """Helper to create the visualization bar chart."""
    fig, ax = plt.subplots(figsize=(10, 5))
    titles = [s['title'] for s in songs]
    values = [s[key] for s in songs]
    ax.bar(titles, values, color='hotpink')
    ax.set_title(f'Merge Sort Visualization - Sorting by {key.capitalize()}')
    ax.set_xlabel('Songs')
    ax.set_ylabel(key.capitalize())
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def merge_sort_visual_generator(songs, key="energy"):
    arr = [s.copy() for s in songs]

    def _merge_sort(low, high):
        if low >= high:
            fig = create_bar_plot(arr, key)
            yield fig, f"Base case: single song at position {low}", pd.DataFrame(arr)
            time.sleep(0.6)
            return

        mid = (low + high) // 2

        fig = create_bar_plot(arr, key)
        yield fig, f"Dividing playlist into left [{low}:{mid}] and right [{mid+1}:{high}]", pd.DataFrame(arr)
        time.sleep(0.6)

        yield from _merge_sort(low, mid)
        yield from _merge_sort(mid + 1, high)

        temp = []
        i, j = low, mid + 1

        while i <= mid and j <= high:
            fig = create_bar_plot(arr, key)
            yield fig, f"Comparing '{arr[i]['title']}' ({arr[i][key]}) vs '{arr[j]['title']}' ({arr[j][key]})", pd.DataFrame(arr)
            time.sleep(0.6)

            if arr[i][key] <= arr[j][key]:
                temp.append(arr[i].copy())
                i += 1
            else:
                temp.append(arr[j].copy())
                j += 1

        while i <= mid:
            temp.append(arr[i].copy())
            i += 1
        while j <= high:
            temp.append(arr[j].copy())
            j += 1

        for k in range(len(temp)):
            arr[low + k] = temp[k]
            fig = create_bar_plot(arr, key)
            yield fig, f"Placed '{temp[k]['title']}' at position {low + k}", pd.DataFrame(arr)
            time.sleep(0.6)

        fig = create_bar_plot(arr, key)
        yield fig, f"✅ Merged sublist from index {low} to {high}", pd.DataFrame(arr)
        time.sleep(0.6)

    yield from _merge_sort(0, len(arr) - 1)

def visualize_sort(df, key):
    """This wrapper fixes the 'not enough output values' error"""
    songs = df.to_dict("records")
    for plot, description, final_df in merge_sort_visual_generator(songs, key):
        yield plot, description, final_df

with gr.Blocks(title="Playlist Vibe Builder - Merge Sort", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎵 Playlist Vibe Builder – Merge Sort
    Sort your playlist by **energy** or **duration** and watch every step of Merge Sort!
    """)

    with gr.Row():
        with gr.Column(scale=2):
            playlist_input = gr.DataFrame(
                value=pd.DataFrame({
                    "title": ["Just a boy-Japanse Rap", "Fire Burning-Sean Kingston", "Otonoke-Creepy Nuts", 
                              "Zoo-Shakira", "I like to move it move it-Madagascar", "Nidone-Creepy Nuts", 
                              "Mamacita-Jason Derula", "Love Not War-Jason Derula", "Iko Iko-Wellington"],
                    "energy": [95, 92, 91, 88, 88, 85, 79, 78, 70],
                    "duration": [315, 406, 310, 313, 356, 357, 426, 335, 321]
                }),
                label="✏️ Your Playlist (add/remove rows & edit values)",
                interactive=True,
                max_height=300
            )
        
        with gr.Column(scale=1):
            gr.Markdown("### Controls")
            sort_key = gr.Dropdown(
                choices=["energy", "duration"],
                value="energy",
                label="Sort by",
                interactive=True
            )
            visualize_btn = gr.Button("🚀 Visualize Merge Sort Steps", variant="primary", size="large")

    gr.Markdown("### Live Animation")
    plot_output = gr.Plot(label="Current state of playlist")
    step_output = gr.Markdown("**Step description will appear here...**")
    final_output = gr.DataFrame(label="✅ Final Sorted Playlist")

    visualize_btn.click(
        fn=visualize_sort,
        inputs=[playlist_input, sort_key],
        outputs=[plot_output, step_output, final_output]
    )

    gr.Markdown("""
    **How to use:**
    - Edit the table (add new songs with the + button at the bottom)
    - Choose energy or duration
    - Click the big button and watch the algorithm!
    """)

if __name__ == "__main__":
    demo.launch()