import bpy
import os
import sys

def process_video(video_path, aston_band_path, output_path):
    # Define paths
    video_path = "G:\\TruAd\\Aston Band\\server\\instance\\video.mp4"
    aston_band_path = "G:\\TruAd\\Aston Band\\server\\instance\\aston_band.png"
    output_path = "G:\\TruAd\\Aston Band\\server\\instance\\output.mp4"

# Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Clear existing scene
    bpy.ops.sequencer.select_all(action='SELECT')
    bpy.ops.sequencer.delete()

    # Add video strip
    video_strip = bpy.context.scene.sequence_editor.sequences.new_movie(
        name="Video",
        filepath=video_path,
        channel=1,
        frame_start=1
    )

    # Get video dimensions
    video_width = video_strip.elements[0].orig_width
    video_height = video_strip.elements[0].orig_height

    # Add Aston band image strip
    aston_band_strip = bpy.context.scene.sequence_editor.sequences.new_image(
        name="AstonBand",
        filepath=aston_band_path,
        channel=2,
        frame_start=1
    )

    # Calculate scaling factor to match the video width
    aston_band_width = aston_band_strip.elements[0].orig_width
    scale_factor = video_width / aston_band_width

    # Apply scaling
    aston_band_strip.transform.scale_x = scale_factor
    aston_band_strip.transform.scale_y = scale_factor

    # Calculate position to place the Aston band at the bottom
    aston_band_height = aston_band_strip.elements[0].orig_height * scale_factor
    aston_band_strip.transform.offset_x = 0
    aston_band_strip.transform.offset_y = -(video_height / 2 - aston_band_height / 2)

    # Set the duration of the Aston band to match the video
    aston_band_strip.frame_final_duration = video_strip.frame_final_duration

    # Set render settings
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'

# Render the video
    try:
        bpy.ops.render.render(animation=True)
        print(f"Rendering completed successfully. Output saved at {output_path}")
    except RuntimeError as e:
        print(f"Error during rendering: {e}")

if __name__ == "__main__":
    video_path = sys.argv[1]
    aston_band_path = sys.argv[2]
    output_path = sys.argv[3]
    process_video(video_path, aston_band_path, output_path)